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
EN_FONT_NAME = "Playpen Sans"
BI_FONT_NAME = "Songti SC"
ZH_FONT_SIZE = 15
EN_FONT_SIZE = 20
BI_FONT_SIZE = 12
# https://wamingo.net/rgbbgr/
FONT_COLOR = "&H00FFFFFF"
OUTLINE_COLOR = "&H00504eff"
MISMATCH_LIMIT = 5
TEXT_LIMIT = 20

OPENAI_API_KEY = ""
OPENAI_MODEL = "gpt-3.5-turbo-1106"

ZH_FORCE_STYLE = f"Fontname={ZH_FONT_NAME},PrimaryColour={FONT_COLOR},OutlineColour={OUTLINE_COLOR},BorderStyle=3,Fontsize={ZH_FONT_SIZE}"
EN_FORCE_STYLE = f"Fontname={EN_FONT_NAME},PrimaryColour={FONT_COLOR},OutlineColour={OUTLINE_COLOR},BorderStyle=3,Fontsize={EN_FONT_SIZE}"
BI_FORCE_STYLE = f"Fontname={EN_FONT_NAME},PrimaryColour={FONT_COLOR},OutlineColour={OUTLINE_COLOR},BorderStyle=3,Fontsize={BI_FONT_SIZE}"


STYLE_MAP = {
    "zh": ZH_FORCE_STYLE,
    "en": EN_FORCE_STYLE,
    "bilingual": BI_FORCE_STYLE,
}

try:
    from local_settings import *  # noqa: F403
except ImportError:
    ...
