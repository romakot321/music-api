from fastapi import Depends
from loguru import logger
from uuid import uuid4

from app.db.base import get_session
from app.schemas.song import SongTaskSchema


class SongRepository:
    def __init__(self, session=Depends(get_session)):
        self.session = session

    def _generate_id(self) -> str:
        return str(uuid4())

    async def create(self) -> SongTaskSchema:
        data = {
            "id": self._generate_id(),
            "is_finished": 0,
            "is_invalid": 0,
            "api_id": "",
            "audio_url": ""
        }
        await self.session.hset(data["id"], mapping=data)
        return SongTaskSchema(**data)

    async def update(self, schema: SongTaskSchema):
        data = schema.model_dump()
        data["is_finished"] = int(data["is_finished"])
        data["is_invalid"] = int(data["is_invalid"])
        await self.session.hset(schema.id, mapping=data)

    async def get(self, song_id: str) -> SongTaskSchema | None:
        data = await self.session.hgetall(song_id)
        if not data:
            return None
        return SongTaskSchema.model_validate(data)

    async def list_in_progress(self) -> list[SongTaskSchema]:
        resp = []
        cursor = b'0'

        while cursor:
            cursor, keys = await self.session.scan(cursor)
            for key in keys:
                data = await self.session.hgetall(key)
                if not data:
                    continue
                if not (data["is_finished"] + data["is_invalid"]):
                    resp.append(SongTaskSchema(**data))

        return resp

