import subprocess
from pathlib import Path

import whisper

from config import WHISPER_MODEL_NAME, DOWNLOAD_DIR, FFMPEG_BIN, FFMPEG_OPTS
from core.utils import write_srt

model = whisper.load_model(WHISPER_MODEL_NAME)

def generate_srt(audio: str) -> str:
    result = model.transcribe(audio)
    return write_srt(result["segments"], audio)


def generate_audio(video: str|Path, suffix=".mp3") -> str:
    if not isinstance(video, Path):
        video = Path(video)

    audio = f"{DOWNLOAD_DIR}/{video.parts[-1].removesuffix(video.suffix)}{suffix}"

    subprocess.check_call(f"{FFMPEG_BIN} {FFMPEG_OPTS} -i '{video.as_posix()}' -b:a 192K -vn '{audio}'", shell=True)
    return audio