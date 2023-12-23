# TODO:
# 1. auto save
import mimetypes
import os.path

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
from core.utils import _write_vtt, parse_vtt
from core.video import generate_video

if "subtitle_path" not in st.session_state:
    st.session_state.update(
        {
            "segments": [],
            "replaced_segments": [],
            "current_seg_index": 0,
            "current_time": 0,
            "vtt_content": "",
            "subtitle_path": "",
            "widget_values": {},
            "video": {
                "mimetype": "video/mp4",
                "path": "",
                "track": "",
                "current_time": 0,
            },
        }
    )


def make_recording_widget(f):
    def wrapper(label, *args, **kwargs):
        widget_value = f(*args, **kwargs)
        st.session_state.widget_values[label] = widget_value
        return widget_value

    return wrapper


with st.sidebar:
    st.info("🎈Configure")

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
subtitle_path = st.text_input("VTT Path or URL", value=st.session_state.subtitle_path)

if subtitle_path and not st.session_state.segments:
    with open(subtitle_path) as f:
        content = f.read()
        st.session_state.vtt_content = content
        if not st.session_state.segments:
            st.session_state.segments = parse_vtt(content)
            st.session_state.replaced_segments = parse_vtt(content)


def get_current_vtt_content() -> str:
    values = st.session_state["widget_values"]
    if not values:
        return ""
    if not values["video_component"]:
        return ""
    current_time = values["video_component"]["current_time"]
    for index, seg in enumerate(st.session_state.segments):
        if seg.start <= current_time <= seg.end:
            st.session_state["current_seg_index"] = index
            return seg.text
    return ""


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


def save_callback() -> None:
    if not subtitle_path:
        st.error("Subtitle is required.")
    else:
        _write_vtt(st.session_state.replaced_segments, subtitle_path)
        st.session_state.segments = st.session_state.replaced_segments


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
            current_time="",
        )


def generate_callback() -> None:
    if not video_path:
        st.error("Video Path or URL is required.")
    elif not subtitle_path:
        st.error("Subtitle is required.")
    else:
        vtts = [[subtitle_path, language]]
        for video in generate_video(video_path, vtts, output_dir):
            st.success(f"Video Generated: {video}")


col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.button("Preview", on_click=preview_callback)

with col2:
    st.button(
        "Generate VTT",
        on_click=subtitle_callback,
        args=(video_path,),
    )

with col3:
    st.button(
        "Save VTT",
        on_click=save_callback,
    )
with col4:
    st.download_button(
        "Download VTT", st.session_state.vtt_content, os.path.basename(subtitle_path)
    )

with col5:
    st.button("Generate", on_click=generate_callback)

make_recording_widget(streamlit_component_video)(
    label="video_component",
    path=st.session_state["video"]["path"],
    mimetype=st.session_state["video"]["mimetype"],
    track=st.session_state["video"]["track"],
    current_time=st.session_state["current_time"],
)

current_vtt = st.text_input("Subtitle", value=get_current_vtt_content())
if st.session_state.segments and current_vtt:
    st.session_state.replaced_segments[st.session_state.current_seg_index].text = current_vtt
