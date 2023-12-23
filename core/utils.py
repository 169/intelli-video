import re
from itertools import islice
from typing import Generator

from config import MISMATCH_LIMIT, TEXT_LIMIT
from core.schema import Segment


def format_timestamp(
    seconds: float,
):
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


def write_vtt(
    transcript: list[dict | Segment], audio: str, language: str | None = None
) -> str:
    if language is not None:
        vtt_filename = f"{audio.removesuffix('.mp3')}.{language}.vtt"
    else:
        vtt_filename = f"{audio.removesuffix('.mp3')}.vtt"
    return _write_vtt(transcript, vtt_filename)


def _write_vtt(transcript: list[dict | Segment], vtt_filename: str) -> str:
    with open(vtt_filename, "w") as f:
        f.write("WEBVTT\n")
        for segment in transcript:
            if isinstance(segment, Segment):
                segment = segment.model_dump()
            print(segment, "segment")
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            f.write(f"\n{start} --> {end}\n{segment['text'].strip()}\n")

    return vtt_filename


def write_bilingual_vtt(transcript: list[dict], audio: str) -> str:
    srt_filename = f"{audio.removesuffix('.mp3')}.bilingual.vtt"

    with open(srt_filename, "w") as f:
        f.write("WEBVTT\n")
        for segment in transcript:
            if "start" in segment and segment["start"] is not None:
                start = format_timestamp(segment["start"])
                end = format_timestamp(segment["end"])
                timestamp = f"{start} --> {end}"
            else:
                timestamp = segment["timestamp"]
            title = segment["title"].strip()
            subtitle = segment["subtitle"].strip()
            f.write(f"\n{timestamp}\n{title}\n{subtitle}\n")

    return srt_filename


def batched(iterable, n) -> Generator:
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


def check_fallback_to_openai(text_map: dict, texts: list[str]) -> bool:
    texts = [text.strip() for text in texts]
    not_seen = {}
    for k, v in text_map.copy().items():
        k = k.strip()
        if k not in texts:
            try:
                not_seen[k] = v.strip()
            except AttributeError:
                print(f"AttributeError: {k}\t{v}")
                not_seen[k] = v[0].strip()
    return len(not_seen) > MISMATCH_LIMIT


def get_seconds(time_str: str) -> float:
    m, s = time_str.strip().split(":")
    return float(m) * 60 + float(s)


def parse_vtt(text: str) -> list[Segment]:
    texts = []
    for items in batched(text.splitlines()[2:], 3):
        try:
            timestamp, text, _ = list(items)
        except ValueError:
            timestamp, text = list(items)
        start, end = timestamp.split("-->")
        texts.append(
            Segment(
                timestamp=timestamp,
                start=get_seconds(start),
                end=get_seconds(end),
                text=text,
            )
        )
    return texts


def assign_texts(text_map: dict, texts: list[str]) -> dict:
    for _ in range(TEXT_LIMIT):
        for i in range(1, len(texts)):
            new_text = " ".join(texts[:i])
            if val := text_map.get(new_text):
                if i != 1:
                    sep = round(len(val) / i)
                    for index, text in enumerate(texts[:i]):
                        text_map[text] = val[index * sep : (index + 1) * sep]
                texts = texts[i:]
    for text in texts:
        combined_text = ""
        match = False
        for sentence in re.split(",|\.|\?", text):
            sentence = sentence.strip()
            for term in (sentence, f"{sentence},", f"{sentence}.", f"{sentence}?"):
                if val := text_map.get(term):
                    combined_text += f" {val}"
                    match = True
        if match:
            text_map[text] = combined_text
    return text_map
