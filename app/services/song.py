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

    async def create(self, schema: SongTaskCreateSchema) -> SongTaskSchema:
        return await self.song_repository.create(user_id=schema.user_id, app_bundle=schema.app_bundle)

    async def send(self, schema: SongTaskCreateSchema, song_id: UUID):
        request = AITaskCreateRequestSchema(
            prompt=schema.prompt,
            lyrics=(schema.prompt if schema.with_voice else "[Instrumental]"),
            instrumental=int(not schema.with_voice)
        )

        logger.debug("Sending submit request to AI: " + str(request.model_dump()))
        response = await self.ai_repository.generate(request)
        logger.debug("Received response: " + str(response.model_dump()))

        if not response.data or not response.data[0].music:  # Error occurs, set song to invalid
            await self.song_repository.update(str(song_id), is_finished=False, is_invalid=True)
            return schema
        song = response.data[0]

        await self.song_repository.update(
            str(song_id),
            api_id=song.uuid,
            is_finished=False,
            audio_url=self.ai_repository.make_audio_url(song),
            image_url=self.ai_repository.make_image_url(song),
        )

    async def get(self, song_id: UUID) -> SongTaskSchema:
        return await self.song_repository.get(str(song_id))

    async def _check(self, song: SongTaskSchema):
        if not song.api_id:
            return
        response = await self.ai_repository.query(song.api_id)
        if not response.data:
            return
        task = response.data[0]

        await self.song_repository.update(
            song.id,
            api_id=song.api_id,
            is_finished=task.status == AITaskStatus.finished,
            audio_url=song.audio_url,
            image_url=song.image_url
        )

    @classmethod
    async def update_songs_status(cls):
        session_getter = get_session()
        db_session = await anext(session_getter)
        self = cls(ai_repository=AIRepository(), song_repository=SongRepository(session=db_session))

        songs = await self.song_repository.list_in_progress()
        check_tasks = [self._check(song) for song in songs]
        await asyncio.gather(*check_tasks)
        try:
            await anext(session_getter)
        except StopAsyncIteration:
            pass

