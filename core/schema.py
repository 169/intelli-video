from pydantic import BaseModel


class DownloadMedia(BaseModel):
    title: str
    video: str
    audio: str