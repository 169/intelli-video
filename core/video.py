import subprocess
from pathlib import Path
from typing import Generator

from loguru import logger

from config import (
    DEBUG,
    STYLE_MAP,
    FFMPEG_BIN,
    FFMPEG_FORMAT_OPTS,
    FFMPEG_PREFIX_OPTS,
    OUTPUT_DIR,
)


def generate_video(video: str | Path, vtts: list[list[str]]) -> Generator:
    if not isinstance(video, Path):
        video = Path(video)

    suffix = video.suffix
    if suffix == ".webm":
        suffix = ".mp4"

    for vtt, language in vtts:
        output = f"{OUTPUT_DIR}/{video.parts[-1].removesuffix(video.suffix)}.{language}{suffix}"
        logger.info(f"Transcoding: {output}")
        style = STYLE_MAP.get(language, STYLE_MAP["en"])
        cmd = f"""{FFMPEG_BIN} {FFMPEG_PREFIX_OPTS} -i '{video.as_posix()}' {FFMPEG_FORMAT_OPTS} -vf "subtitles='{vtt}':fontsdir=./src/fonts/:force_style='{style}'" '{output}'"""
        if DEBUG:
            logger.debug(f"CMD: {cmd}")
        subprocess.check_call(cmd, shell=True)
        logger.info(f"Video generated: {output}")
        yield output
