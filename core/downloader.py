import os

import yt_dlp

from config import DOWNLOAD_DIR
from core.schema import DownloadMedia

ydl_opts = {
    'format': 'bv+ba/b',
    'paths': {"home": DOWNLOAD_DIR.as_posix()},
    'keepvideo': True,
    'postprocessors': [
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '0',
        }
    ]
}


def download(url: str) -> DownloadMedia:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        r = ydl.extract_info(url, download=True)
        requested_downloads = r['requested_downloads'][0]
        for file in requested_downloads.get('__files_to_merge', []):
            try:
                os.remove(file)
            except FileNotFoundError:
                ...
        return DownloadMedia(title=r['title'], video=requested_downloads['filename'],
                             audio=requested_downloads['filepath'])
