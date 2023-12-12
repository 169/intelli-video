from pathlib import Path

DEBUG = False
HERE = Path(__file__).parent.absolute()
DOWNLOAD_DIR = HERE / ".download"
OUTPUT_DIR = HERE / "output"
WHISPER_MODEL_NAME = "small"
FFMPEG_BIN = "ffmpeg"
FFMPEG_PREFIX_OPTS = "-hide_banner -loglevel error -y"
FFMPEG_FORMAT_OPTS = "-c:v libx264 -preset fast -qp 0 -c:a aac -vf format=yuv420p"

# https://wamingo.net/rgbbgr/
ZH_FORCE_STYLE = "Fontname=Yuanti SC,PrimaryColour=&H00FFFFFF,OutlineColour=&H00504eff,BorderStyle=3,Fontsize=15"
EN_FORCE_STYLE = "Fontname=Playpen Sans,PrimaryColour=&H00FFFFFF,OutlineColour=&H00504eff,BorderStyle=3,Fontsize=20"

try:
    from local_settings import *  # noqa: F403
except ImportError:
    ...
