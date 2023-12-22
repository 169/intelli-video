import mimetypes

import streamlit as st
import whisper
from streamlit_component_video import streamlit_component_video
from whisper.tokenizer import LANGUAGES

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
from core.audio import generate_audio, generate_subtitle
from core.downloader import download

if "subtitle_path" not in st.session_state:
    st.session_state.update(
        {
            "subtitle_path": "",
            "video": {
                "mimetype": "video/mp4",
                "path": "",
                "track": "",
            },
        }
    )

with st.sidebar:
    st.info("🎈 Configure")

    st.write("## File")
    mimetype = st.selectbox(
        "Video MIMETYPE",
        [v for k, v in mimetypes.types_map.items() if "video" in v],
        index=2,
    )

    download_dir: str = st.text_input("Download Dir", DOWNLOAD_DIR) or ""
    output_dir: str = st.text_input("Output Dir", OUTPUT_DIR) or ""

    st.write("## Audio")

    try:
        index = whisper.available_models().index(WHISPER_MODEL)
    except ValueError:
        index = 0

    model: str = (
        st.selectbox(
            "Whisper model",
            whisper.available_models(),
            index=index,
        )
        or ""
    )

    st.write("## Subtitle")
    language: str = (
        st.selectbox(
            "Language",
            LANGUAGES.keys(),
            index=0,
        )
        or ""
    )
    method: str = (
        st.selectbox(
            "Method",
            ["whisper", "openai_api"],
            index=0,
        )
        or ""
    )
    zh_font_name = st.text_input("ZH Font Name", ZH_FONT_NAME)
    en_font_name = st.text_input("ZH Font Name", EN_FONT_NAME)
    en_font_size = st.text_input("ZH Font Size", ZH_FONT_SIZE)
    zh_font_size = st.text_input("ZH Font Size", EN_FONT_SIZE)
    font_color = st.text_input("Font Color", FONT_COLOR)
    outline_color = st.text_input("ZH Font Name", OUTLINE_COLOR)

    st.write("## Video")

video_path = st.text_input("Video Path or URL")
subtitle_path = st.text_input("Subtitle Path or URL", value=st.session_state.subtitle_path)

def subtitle_callback(path: str) -> None:
    if not path:
        st.error("Video Path or URL is required.")
        return
    with st.status("Generate subtitle..."):
        if path.startswith("http"):
            st.write("Download video...")
            media = download(path)
            audio = media.audio
        else:
            st.write("Generating audio...")
            audio = generate_audio(path)
        st.write("Generating subtitle...")
        st.session_state.subtitle_path = generate_subtitle(
            audio, method, language, "vtt", output_dir, model_name=model
        )


def preview_callback() -> None:
    track = subtitle_path or st.session_state.subtitle_path
    if not track:
        st.error("Subtitle is required.")
    elif not video_path:
        st.error("Video Path or URL is required.")
    else:
        st.session_state["video"] = dict(
            path=video_path,
            mimetype="video/mp4",
            track=track,
        )


col1, col2 = st.columns(2)

with col2:
    st.button(
        "Generate Subtitle",
        on_click=subtitle_callback,
        args=(video_path,),
    )
with col1:
    st.button("Preview", on_click=preview_callback)

streamlit_component_video(
    video=st.session_state["video"]["path"],
    mimetype=st.session_state["video"]["mimetype"],
    track=st.session_state["video"]["track"],
)
