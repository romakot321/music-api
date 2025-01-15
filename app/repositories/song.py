from fastapi import Depends
from loguru import logger

from app.db.base import get_session
from app.schemas.song import SongTaskSchema


class SongRepository:
    def __init__(self, session=Depends(get_session)):
        self.session = session

    async def store(self, schema: SongTaskSchema):
        await self.session.hset(str(schema.id), mapping={
            "id": str(schema.id),
            "is_finished": int(schema.is_finished),
            "audio_url": str(schema.audio_url)
        })

    async def get(self, song_id: str) -> SongTaskSchema | None:
        data = await self.session.hgetall(song_id)
        if not data:
            return None
        return SongTaskSchema.model_validate(data)
