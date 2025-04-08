from pydantic import BaseModel, HttpUrl, Field
from uuid import UUID
from enum import Enum


class ExternalResponseSchema(BaseModel):
    status: int
    message: str
    data: BaseModel | list


class ExternalLyricsRequestSchema(BaseModel):
    prompt: str


class ExternalLyricsResponseSchema(ExternalResponseSchema):
    class LyricsData(BaseModel):
        text: str
        title: str

    data: LyricsData


class ExternalTaskCreateRequestSchema(BaseModel):
    prompt: str
    lyrics: str | None = None
    instrumental: int = Field(ge=0, le=1)  # 1 for pure music

    is_auto: int = 0
    model_version: str = 'v3.5'


class ExternalTaskStatus(int, Enum):
    running = "RUNNING"
    finished = "FINISHED"
    error = "ERROR"


class ExternalSongSchema(BaseModel):
    audio: str
    image: str
    audio_duration: int
    status: ExternalTaskStatus
    song_id: str


class ExternalTaskCreateResponseSchema(ExternalResponseSchema):
    data: list[ExternalSongSchema]


class ExternalTaskStatusResponseSchema(ExternalResponseSchema):
    data: list[ExternalSongSchema]
