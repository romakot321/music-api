from pydantic import BaseModel, HttpUrl
from uuid import UUID


class SongTaskSchema(BaseModel):
    id: UUID
    is_finished: bool
    audio_url: HttpUrl | None = None


class SongTaskCreateSchema(BaseModel):
    prompt: str
    with_voice: bool

