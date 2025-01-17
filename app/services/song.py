from fastapi import Depends, HTTPException
from uuid import UUID
from loguru import logger
import asyncio

from app.repositories.ai import AIRepository
from app.repositories.song import SongRepository
from app.schemas.song import SongTaskCreateSchema, SongTaskSchema
from app.schemas.ai import AITaskCreateRequestSchema, AITaskCreateResponseSchema
from app.schemas.ai import AITaskStatusResponseSchema, AITaskStatus
from app.db.base import get_session


class SongService:
    def __init__(
            self,
            ai_repository: AIRepository = Depends(),
            song_repository: SongRepository = Depends()
    ):
        self.ai_repository = ai_repository
        self.song_repository = song_repository

    async def create(self) -> SongTaskSchema:
        return await self.song_repository.create()

    async def send(self, schema: SongTaskCreateSchema, song_id: UUID) -> SongTaskSchema:
        request = AITaskCreateRequestSchema(
            prompt=schema.prompt,
            lyrics=(schema.prompt if schema.with_voice else "[Instrumental]"),
            instrumental=int(not schema.with_voice)
        )

        logger.debug("Sending submit request to AI: " + str(request.model_dump()))
        response = await self.ai_repository.generate(request)
        logger.debug("Received response: " + str(response.model_dump()))

        if not response.data or not response.data[0].music:  # Error occurs, set song to invalid
            schema = SongTaskSchema(
                id=str(song_id),
                api_id=None,
                is_finished=0,
                is_invalid=True,
                audio_url=None
            )
            await self.song_repository.update(schema)
            return schema
        song = response.data[0]

        schema = SongTaskSchema(
            id=str(song_id),
            api_id=song.uuid,
            is_finished=0,
            audio_url=self.ai_repository.make_audio_url(song)
        )
        await self.song_repository.update(schema)
        return schema

    async def get(self, song_id: UUID) -> SongTaskSchema:
        song = await self.song_repository.get(str(song_id))
        if song is None:
            raise HTTPException(404)
        return song

    async def _check(self, song: SongTaskSchema) -> SongTaskSchema | None:
        response = await self.ai_repository.query(song.api_id)
        if not response.data:
            return None
        task = response.data[0]

        schema = SongTaskSchema(
            id=song_id,
            api_id=song.api_id,
            is_finished=task.status == AITaskStatus.finished,
            audio_url=song.audio_url
        )
        await self.song_repository.update(schema)
        return schema

    @classmethod
    async def update_songs_status(cls):
        session_getter = get_session()
        db_session = next(session_getter)
        self = cls(ai_repository=AIRepository(), song_repository=SongRepository(session=db_session))

        songs = await self.song_repository.list_in_progress()
        check_tasks = [self._check(song.id) for song in songs]
        await asyncio.gather(*check_tasks)

