from pydantic import BaseModel, HttpUrl, root_validator
from uuid import UUID


class SongTaskSchema(BaseModel):
    id: str
    is_finished: bool
    is_invalid: bool = False
    api_id: str | None = None
    audio_url: HttpUrl | None = None

    @root_validator(pre=True)
    @classmethod
    def translate_empty_to_none(cls, values) -> HttpUrl | None:
        if not isinstance(values, dict):
            return {}
        audio_url = values.get("audio_url")
        if isinstance(audio_url, str) and not audio_url:
            values["audio_url"] = None
        api_id = values.get("api_id")
        if isinstance(api_id, str) and not api_id:
            values["api_id"] = None
        return values


class SongTaskCreateSchema(BaseModel):
    prompt: str
    with_voice: bool

