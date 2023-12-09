from pathlib import Path

HERE = Path(__file__).parent.absolute()
DOWNLOAD_DIR = HERE / ".download"
OUTPUT_DIR = HERE / "output"
WHISPER_MODEL_NAME = "small"
FFMPEG_BIN = "ffmpeg"
FFMPEG_OPTS = "-hide_banner -loglevel error -y"
# use fontsdir
FORCE_STYLE = "Fontname=Futura,PrimaryColour=&HFF00,Fontsize=20"