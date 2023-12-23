from typing import Optional

from pydantic import BaseModel


class DownloadMedia(BaseModel):
    title: str
    video: str
    audio: str


class Segment(BaseModel):
    text: str
    timestamp: Optional[str]
    start: Optional[str | None] = None
    end: Optional[str | None] = None
    title: Optional[str | None] = None
    subtitle: Optional[str | None] = None
