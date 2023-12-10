import subprocess
from pathlib import Path

from config import FFMPEG_BIN, FFMPEG_OPTS, OUTPUT_DIR, ZH_FORCE_STYLE, EN_FORCE_STYLE

def generate_video(video: str|Path, srts: list[str]) -> str:
    if not isinstance(video, Path):
        video = Path(video)

    for srt, language in srts:
        output = f"{OUTPUT_DIR}/{video.parts[-1].removesuffix(video.suffix)}.{language}{video.suffix}"
        style = EN_FORCE_STYLE if language == "en" else ZH_FORCE_STYLE
        subprocess.check_call(f"""{FFMPEG_BIN} {FFMPEG_OPTS} -i '{video.as_posix()}' -vf "subtitles='{srt}':force_style='{style}'" '{output}'""", shell=True)
        yield output
