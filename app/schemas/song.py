from pydantic import BaseModel, HttpUrl, root_validator, ConfigDict, model_validator
from enum import Enum
from uuid import UUID
import datetime as dt


class SongLyricsGenerateSchema(BaseModel):
    prompt: str


class SongLyricsSchema(BaseModel):
    lyrics: str


class SongTaskSchema(BaseModel):
    id: UUID
    user_id: UUID
    is_finished: bool
    is_invalid: bool = False
    api_id: str | None = None
    audio_url: HttpUrl | None = None
    image_url: HttpUrl | None = None
    comment: str | None = None

    @model_validator(mode='before')
    @classmethod
    def translate_status(cls, state):
        if not isinstance(state, dict):
            state = state.__dict__
        if state.get('status') and isinstance(state["status"], Enum):
            state["is_finished"] = state["status"].value == "finished"
            state["is_invalid"] = state["status"].value == "error"
        elif state.get('status') is None:
            state["is_finished"] = False
            state["is_invalid"] = False
        return state

    model_config = ConfigDict(from_attributes=True)


class SongTaskCreateSchema(BaseModel):
    prompt: str
    with_voice: bool
    user_id: UUID
    app_bundle: str
    lyrics: str

    model_config = ConfigDict(from_attributes=True)

