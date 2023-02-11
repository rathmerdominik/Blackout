from typing import List, Optional
from pydantic import BaseModel


class FeedbackToken(BaseModel):
    add: str
    remove: str


class Album(BaseModel):
    name: str
    id: str


class Artist(BaseModel):
    name: str
    id: str


class Thumbnail(BaseModel):
    url: str
    width: int
    height: int


class Suggestion(BaseModel):
    videoId: str
    title: str
    artists: List[Artist]
    album: List[Album]
    likeStatus: str
    thumbnails: List[Thumbnail]
    isAvailable: bool
    isExplicit: bool
    duration: str
    duration_seconds: int
    setVideoId: str


class Related(BaseModel):
    title: str
    playlistId: str
    thumbnails: List[Thumbnail]
    description: str


class Track(BaseModel):
    videoId: str
    title: str
    artists: List[Artist]
    album: Optional[Album]
    duration: str
    thumbnails: List[Thumbnail]
    isAvailable: bool
    isExplicit: bool
    videoType: str
    feedbackTokens: Optional[FeedbackToken]


class Playlist(BaseModel):
    id: str
    privacy: str
    title: str
    thumbnails: List[Thumbnail]
    description: str
    author: Optional[str]
    year: Optional[str]
    duration: Optional[str]
    duration_seconds: int
    trackCount: int
    suggestions: Optional[List[Suggestion]]
    related: Optional[List[Related]]
    tracks: List[Track]
