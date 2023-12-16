from itertools import islice


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

    hours_marker = f"{hours:02d}:"
    return f"{hours_marker}{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def write_srt(transcript: list[dict], audio: str, language: str) -> str:
    srt_filename = f"{audio.removesuffix('.mp3')}.{language}.srt"

    with open(srt_filename, "w") as f:
        for i, segment in enumerate(transcript, start=1):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            f.write(f"{i}\n{start} --> {end}\n{segment['text'].strip()}\n")

    return srt_filename


def write_bilingual_srt(transcript: list[dict], audio: str) -> str:
    srt_filename = f"{audio.removesuffix('.mp3')}.bilingual.srt"

    with open(srt_filename, "w") as f:
        for i, segment in enumerate(transcript, start=1):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            title = segment["title"].strip()
            subtitle = segment["subtitle"].strip()
            f.write(f"{i}\n{start} --> {end}\n{title}\n{subtitle}\n")

    return srt_filename


def batched(iterable, n):
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch
