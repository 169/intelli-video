import subprocess
from pathlib import Path
from typing import Generator

from loguru import logger

from config import (
    BI_FORCE_STYLE,
    DEBUG,
    EN_FORCE_STYLE,
    FFMPEG_BIN,
    FFMPEG_FORMAT_OPTS,
    FFMPEG_PREFIX_OPTS,
    ZH_FORCE_STYLE,
)

STYLE_MAP = {
    "zh": ZH_FORCE_STYLE,
    "en": EN_FORCE_STYLE,
    "bilingual": BI_FORCE_STYLE,
}


def generate_video(
    video: str | Path, vtts: list[list[str]], output_dir: str
) -> Generator:
    if not isinstance(video, Path):
        video = Path(video)

    suffix = video.suffix
    if suffix == ".webm":
        suffix = ".mp4"

    for vtt, language in vtts:
        output = f"{output_dir}/{video.parts[-1].removesuffix(video.suffix)}.{language}{suffix}"
        logger.info(f"Transcoding: {output}")
        style = STYLE_MAP.get(language, STYLE_MAP["en"])
        cmd = f"""{FFMPEG_BIN} {FFMPEG_PREFIX_OPTS} -i '{video.as_posix()}' {FFMPEG_FORMAT_OPTS} -vf "subtitles='{vtt}':fontsdir=./src/fonts/:force_style='{style}'" '{output}'"""
        if DEBUG:
            logger.debug(f"CMD: {cmd}")
        subprocess.check_call(cmd, shell=True)
        logger.info(f"Video generated: {output}")
        yield output
