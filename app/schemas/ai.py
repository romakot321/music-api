from pydantic import BaseModel, HttpUrl, Field
from uuid import UUID
from enum import Enum


class AIResponseSchema(BaseModel):
    status: int
    message: str
    data: dict


class AILyricsRequestSchema(BaseModel):
    prompt: str


class AILyricsResponseSchema(AIResponseSchema):
    class LyricsData(BaseModel):
        text: str
        title: str

    data: LyricsData


class AITaskCreateRequestSchema(BaseModel):
    is_auto: int = Field(ge=0, le=1)  # when 1, instrumental ignored
    prompt: str
    model_version: str = 'v3.5'
    instrumental: int = Field(ge=0, le=1)  # 1 for pure music


class AITaskStatus(str, Enum):
    running = "RUNNING"
    finished = "FINISHED"


class AISongSchema(BaseModel):
    audio: HttpUrl
    audio_duration: int
    image: HttpUrl
    lyric: str
    song_id: UUID
    status: AITaskStatus = AITaskStatus.running
    tags: str  # Separeted by ,
    title: str


class AITaskCreateResponseSchema(AIResponseSchema):
    data: list[AISongSchema]


class AITaskStatusResponseSchema(AIResponseSchema):
    data: list[AISongSchema]
