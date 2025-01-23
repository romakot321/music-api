from fastapi import Depends
from loguru import logger
from uuid import uuid4

from app.schemas.song import SongTaskSchema
from app.db.tables import Song, SongStatus
from .base import BaseRepository


class SongRepository(BaseRepository):
    base_table = Song

    async def create(self, user_id: str, app_bundle: str) -> SongTaskSchema:
        model = Song(user_id=user_id, app_bundle=app_bundle)
        model = await self._create(model)
        return SongTaskSchema.model_validate(model)

    async def update(self, song_id: str, **fields):
        data = {k: v for k, v in fields.items() if v is not None}

        if "is_invalid" in data and data.pop("is_invalid"):
            data['status'] = SongStatus.error
        elif "is_finished" in data and data.pop("is_finished"):
            data['status'] = SongStatus.finished

        return SongTaskSchema.model_validate(await self._update(song_id, **data))

    async def get(self, song_id: str) -> SongTaskSchema:
        model = await self._get_one(id=song_id)
        return SongTaskSchema.model_validate(model)

    async def list_in_progress(self) -> list[SongTaskSchema]:
        return list(await self._get_many(count=1000000, status=SongStatus.queued))

