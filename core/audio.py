import whisper

from config import WHISPER_MODEL_NAME
from core.utils import write_srt

model = whisper.load_model(WHISPER_MODEL_NAME)

def generate_srt(audio: str) -> str:
    result = model.transcribe(audio)
    return write_srt(result["segments"], audio)


def overwrite_subtitile():
    return
