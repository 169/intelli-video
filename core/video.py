import subprocess
from pathlib import Path

from config import FFMPEG_BIN, FFMPEG_OPTS, OUTPUT_DIR, FORCE_STYLE


def generate_video(video: str|Path, srt: list[str]) -> str:
    if not isinstance(video, Path):
        video = Path(video)

    output = f"{OUTPUT_DIR}/{video.parts[-1]}"

    subprocess.check_call(f"""{FFMPEG_BIN} {FFMPEG_OPTS} -i '{video.as_posix()}' -vf "subtitles='{srt}':force_style='{FORCE_STYLE}'" '{output}'""", shell=True)
    return output
