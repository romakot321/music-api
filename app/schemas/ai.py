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
    prompt: str
    lyrics: str
    instrumental: int = Field(ge=0, le=1)  # 1 for pure music

    is_auto: int = 0
    mv: str = 'v4.0'
    g_num: int = 2
    is_public: int = 0
    gender: str = "random"


class AITaskStatus(int, Enum):
    error = 3
    running = 2
    finished = 0


class AISongSchema(BaseModel):
    class Music(BaseModel):
        audio_duration: int | str
        audio_file: str
        image_file: str
        item_uuid: str
        lyric: str
        tags: str
        title: str

    id: int
    is_public: int
    music: list[Music]
    part: int
    uuid: str


class AITaskCreateResponseSchema(AIResponseSchema):
    data: list[AISongSchema]


class AITaskStatusData(BaseModel):
    class Info(BaseModel):
        audio_duration: int | str
        audio_file: str
        image_file: str

    info: list[Info]
    status: AITaskStatus  # 0 for finished, 2 for in progress
    uuid: str


class AITaskStatusResponseSchema(AIResponseSchema):
    data: list[AITaskStatusData]
