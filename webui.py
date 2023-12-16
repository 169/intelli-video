import streamlit as st
import whisper

from config import (
    DOWNLOAD_DIR,
    EN_FONT_NAME,
    EN_FONT_SIZE,
    FONT_COLOR,
    OUTLINE_COLOR,
    OUTPUT_DIR,
    WHISPER_MODEL,
    ZH_FONT_NAME,
    ZH_FONT_SIZE,
)
from core.downloader import download

with st.sidebar:
    st.info("🎈 Configure")

    st.write("## File")
    download_dir = st.text_input("Download Dir", DOWNLOAD_DIR)
    output_dir = st.text_input("Output Dir", OUTPUT_DIR)

    st.write("## Audio")

    try:
        index = whisper.available_models().index(WHISPER_MODEL)
    except ValueError:
        index = 0

    model = st.selectbox(
        "Whisper model",
        whisper.available_models(),
        index=index,
    )

    st.write("## Subtitle")
    zh_font_name = st.text_input("ZH Font Name", ZH_FONT_NAME)
    en_font_name = st.text_input("ZH Font Name", EN_FONT_NAME)
    en_font_size = st.text_input("ZH Font Size", ZH_FONT_SIZE)
    zh_font_size = st.text_input("ZH Font Size", EN_FONT_SIZE)
    font_color = st.text_input("Font Color", FONT_COLOR)
    outline_color = st.text_input("ZH Font Name", OUTLINE_COLOR)

    st.write("## Video")

video = st.text_input("Video Path or URL")
if st.button("Submit"):
    if video.startswith("http"):
        media = download(video)
        with open(media.video, "rb") as f:
            video_bytes = f.read()
    else:
        with open(video, "rb") as f:
            video_bytes = f.read()
    v = st.video(video_bytes)
    print(v)
