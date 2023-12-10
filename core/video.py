import subprocess
from pathlib import Path
from typing import Generator

from loguru import logger

from config import EN_FORCE_STYLE, FFMPEG_BIN, FFMPEG_OPTS, FFMPEG_PREFIX_OPTS, OUTPUT_DIR, ZH_FORCE_STYLE


def generate_video(video: str | Path, srts: list[list[str]]) -> Generator:
    if not isinstance(video, Path):
        video = Path(video)

    suffix = video.suffix
    if suffix == ".webm":
        suffix = ".mp4"

    for srt, language in srts:
        output = f"{OUTPUT_DIR}/{video.parts[-1].removesuffix(video.suffix)}.{language}{suffix}"
        logger.info(f"Transcoding: {output}")
        style = EN_FORCE_STYLE if language == "en" else ZH_FORCE_STYLE
        cmd = f"""{FFMPEG_BIN} {FFMPEG_PREFIX_OPTS} -i '{video.as_posix()}' {FFMPEG_OPTS} -vf "subtitles='{srt}':fontsdir=./src/fonts/:force_style='{style}'" '{output}'"""
        logger.debug(f"CMD: {cmd}")
        subprocess.check_call(cmd, shell=True)
        logger.info(f"Video generated: {output}")
        yield output
