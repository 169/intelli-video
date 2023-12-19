import subprocess
import warnings
from pathlib import Path

import openai
import tenacity
import whisper
from loguru import logger

from config import (
    DOWNLOAD_DIR,
    FFMPEG_BIN,
    FFMPEG_PREFIX_OPTS,
    TEXT_LIMIT,
    WHISPER_MODEL,
)
from core.client import Client
from core.prompts import render_translate_prompt
from core.utils import (
    assign_texts,
    batched,
    check_fallback_to_openai,
    parse_vtt,
    write_bilingual_vtt,
    write_vtt,
)

model = whisper.load_model(WHISPER_MODEL)


def transcribe(audio: str, language: str = "en") -> dict:
    logger.info(f"Transcribe: {audio} <Language: {language}>")
    result = model.transcribe(audio, language=language)
    logger.info(f"Transcribed: {audio} <Language: {language}>")
    return result


def generate_vtt_from_api(
    audio: str, title_language: str, other_language: str
) -> list[list[str]]:
    logger.info(f"Generate {title_language} vtt from OpenAI API: {audio}")
    client = Client()
    transcript = client.transcribe(audio)
    all_segments = [i.model_dump() for i in parse_vtt(transcript)]
    segments = []
    for lst in batched(all_segments, TEXT_LIMIT):
        texts = [seg["text"] for seg in lst]
        content = "\n".join(texts)
        text_map = client.translate(render_translate_prompt(content, other_language))
        text_map = assign_texts(text_map, texts)
        for seg in lst:
            text = seg["text"]
            trans = text_map.get(text.strip(), "")
            if title_language == "en":
                seg["title"] = f"<strong>{text}</strong>"
                seg["subtitle"] = trans
            else:
                seg["title"] = f"<strong>{trans}</strong>"
                seg["subtitle"] = text
            segments.append(seg)
    return [[write_bilingual_vtt(segments, audio), "bilingual"]]


def generate_vtt(audio: str, bilingual: str, subtitles: str) -> list[list[str]]:
    warnings.filterwarnings("ignore")
    result = transcribe(audio)
    source_language = result["language"]

    client = Client()

    srts = []

    if subtitles:
        subtitles = subtitles.split(",")
        if source_language in subtitles:
            srts.append(
                [write_vtt(result["segments"], audio, source_language), source_language]
            )
            logger.info(f"Generate {source_language} vtt: {srts[0][0]}")

        for dist_language in subtitles:
            if dist_language != source_language:
                result = transcribe(audio, language=dist_language)
                srts.append(
                    [write_vtt(result["segments"], audio, dist_language), dist_language]
                )
                logger.info(f"Generate {dist_language} vtt: {srts[-1][0]}")
    if bilingual:
        title_language, subtitle_language = bilingual.split(",")
        if source_language in (title_language, subtitle_language):
            if "en" in (title_language, subtitle_language):
                result = transcribe(audio, language="en")
                other_language = (
                    subtitle_language if title_language == "en" else title_language
                )
                segments = []
                for lst in batched(result["segments"], TEXT_LIMIT):
                    lst = list(lst)
                    texts = [seg["text"] for seg in lst]
                    content = "\n".join(texts)
                    text_map = client.translate(
                        render_translate_prompt(content, other_language)
                    )
                    need_use_api = check_fallback_to_openai(text_map, texts)
                    if need_use_api:
                        try:
                            return generate_vtt_from_api(
                                audio, title_language, other_language
                            )
                        except (openai.APIStatusError, tenacity.RetryError):
                            ...
                    text_map = assign_texts(text_map, texts)
                    for seg in lst:
                        text = seg["text"]
                        trans = text_map.get(text.strip(), "")
                        if title_language == "en":
                            seg["title"] = f"<strong>{text}</strong>"
                            seg["subtitle"] = trans
                        else:
                            seg["title"] = f"<strong>{trans}</strong>"
                            seg["subtitle"] = text
                        segments.append(seg)
                srts.append(
                    [write_bilingual_vtt(segments, audio), "bilingual"],
                )
                logger.info(f"Generate {bilingual} bilingual vtt: {srts[0][0]}")
        else:
            # TODO: support other languages
            ...

    warnings.filterwarnings("default")
    return srts


def generate_audio(video: str | Path, suffix=".mp3") -> str:
    if not isinstance(video, Path):
        video = Path(video)

    audio = f"{DOWNLOAD_DIR}/{video.parts[-1].removesuffix(video.suffix)}{suffix}"

    subprocess.check_call(
        f"{FFMPEG_BIN} {FFMPEG_PREFIX_OPTS} -i '{video.as_posix()}' -b:a 192K -vn '{audio}'",
        shell=True,
    )
    logger.info(f"Audio generated: {audio}")
    return audio
