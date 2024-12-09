from pathlib import Path

DEBUG = False
HERE = Path(__file__).parent.absolute()
DOWNLOAD_DIR: str | Path = HERE / ".download"
OUTPUT_DIR: str | Path = HERE / "output"
WHISPER_MODEL = "large"
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
OPENAI_MODEL = "gpt-4o"
INITIAL_PROMPT_MAP = {
    "zh": "以下是普通话的句子，请以简体输出。",
}

ZH_FORCE_STYLE = f"Fontname={ZH_FONT_NAME},PrimaryColour={FONT_COLOR},OutlineColour={OUTLINE_COLOR},BorderStyle=3,Fontsize={ZH_FONT_SIZE}"
EN_FORCE_STYLE = f"Fontname={EN_FONT_NAME},PrimaryColour={FONT_COLOR},OutlineColour={OUTLINE_COLOR},BorderStyle=3,Fontsize={EN_FONT_SIZE}"
BI_FORCE_STYLE = f"Fontname={EN_FONT_NAME},PrimaryColour={FONT_COLOR},OutlineColour={OUTLINE_COLOR},BorderStyle=3,Fontsize={BI_FONT_SIZE}"

try:
    from local_settings import *  # noqa: F403
except ImportError:
    ...
