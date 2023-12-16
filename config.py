from pathlib import Path

DEBUG = False
HERE = Path(__file__).parent.absolute()
DOWNLOAD_DIR = HERE / ".download"
OUTPUT_DIR = HERE / "output"
WHISPER_MODEL = "small"
FFMPEG_BIN = "ffmpeg"
FFMPEG_PREFIX_OPTS = "-hide_banner -loglevel error -y"
FFMPEG_FORMAT_OPTS = "-c:v libx264 -preset fast -qp 0 -c:a aac -vf format=yuv420p"
ZH_FONT_NAME = "Yuanti SC"
ZH_FONT_SIZE = 15
EN_FONT_SIZE = 20
EN_FONT_NAME = "Playpen Sans"
FONT_COLOR = "&H00FFFFFF"
OUTLINE_COLOR = "&H00504eff"

# https://wamingo.net/rgbbgr/
ZH_FORCE_STYLE = f"Fontname={ZH_FONT_NAME},PrimaryColour={FONT_COLOR},OutlineColour={OUTLINE_COLOR},BorderStyle=3,Fontsize={ZH_FONT_SIZE}"
EN_FORCE_STYLE = f"Fontname={EN_FONT_NAME},PrimaryColour={FONT_COLOR},OutlineColour={OUTLINE_COLOR},BorderStyle=3,Fontsize={EN_FONT_SIZE}"

try:
    from local_settings import *  # noqa: F403
except ImportError:
    ...
