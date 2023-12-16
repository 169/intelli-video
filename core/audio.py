import subprocess
import warnings
from pathlib import Path

import whisper
from loguru import logger

from config import DOWNLOAD_DIR, FFMPEG_BIN, FFMPEG_PREFIX_OPTS, WHISPER_MODEL
from core.client import translate
from core.prompts import render_translate_prompt
from core.utils import batched, write_bilingual_vtt, write_vtt

model = whisper.load_model(WHISPER_MODEL)
LIMIT = 30


def generate_vtt(audio: str, bilingual: str, subtitles: str) -> list[list[str]]:
    warnings.filterwarnings("ignore")
    result = model.transcribe(audio)
    source_language = result["language"]

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
                result = model.transcribe(audio, language=dist_language)
                srts.append(
                    [write_vtt(result["segments"], audio, dist_language), dist_language]
                )
                logger.info(f"Generate {dist_language} vtt: {srts[-1][0]}")
    if bilingual:
        title_language, subtitle_language = bilingual.split(",")
        if source_language in (title_language, subtitle_language):
            if "en" in (title_language, subtitle_language):
                result = model.transcribe(audio, language="en")
                other_language = (
                    subtitle_language if title_language == "en" else title_language
                )
                segments = []
                for lst in batched(result["segments"], LIMIT):
                    lst = list(lst)
                    content = "\n".join(seg["text"] for seg in lst)
                    new_texts = translate(render_translate_prompt(content, other_language))
                    text_map = {}
                    for item in batched(new_texts, 2):
                        try:
                            k, v = item
                        except ValueError:
                            logger.error(f"Error: unpack fail:{item}")
                            continue
                        text_map[k.strip()] = v
                    for index, seg in enumerate(lst):
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
