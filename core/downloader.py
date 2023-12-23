import os
from pathlib import Path

import yt_dlp
from loguru import logger

from config import DOWNLOAD_DIR
from core.schema import DownloadMedia

if isinstance(DOWNLOAD_DIR, Path):
    DOWNLOAD_DIR = DOWNLOAD_DIR.as_posix()

ydl_opts = {
    "quiet": True,
    "format": "bv+ba/b",
    "paths": {"home": DOWNLOAD_DIR},
    "keepvideo": True,
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "0",
        }
    ],
}


def download(url: str) -> DownloadMedia:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        logger.info(f"Downloading: {url}")
        r = ydl.extract_info(url, download=True)
        requested_downloads = r["requested_downloads"][0]
        for file in requested_downloads.get("__files_to_merge", []):
            try:
                os.remove(file)
            except FileNotFoundError:
                ...
        logger.info(f"Downloaded: {requested_downloads['filename']}")
        return DownloadMedia(
            title=r["title"],
            video=requested_downloads["filename"],
            audio=requested_downloads["filepath"],
        )
