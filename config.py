from pathlib import Path

HERE = Path(__file__).parent.absolute()
DOWNLOAD_DIR = HERE / ".download"
OUTPUT_DIR = HERE / "output"
WHISPER_MODEL_NAME = "small"
FFMPEG_BIN = "ffmpeg"
FFMPEG_OPTS = "-hide_banner -loglevel error -y"

# https://wamingo.net/rgbbgr/
ZH_FORCE_STYLE = "fontsdir=./src/fonts/:Fontname=Ma Shan Zheng Regular,PrimaryColour=&HFF00,OutlineColour=&H80504eff,BorderStyle=3,Fontsize=20"
EN_FORCE_STYLE = "fontsdir=./src/fonts/:Fontname=Playpen Sans,PrimaryColour=&HFF00,OutlineColour=&H80504eff,BorderStyle=3,Fontsize=20"