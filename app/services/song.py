from fastapi import Depends, HTTPException
from uuid import UUID
from loguru import logger

from app.repositories.ai import AIRepository
from app.repositories.song import SongRepository
from app.schemas.song import SongTaskCreateSchema, SongTaskSchema
from app.schemas.ai import AITaskCreateRequestSchema, AITaskCreateResponseSchema
from app.schemas.ai import AITaskStatusResponseSchema, AITaskStatus


class SongService:
    def __init__(
            self,
            ai_repository: AIRepository = Depends(),
            song_repository: SongRepository = Depends()
    ):
        self.ai_repository = ai_repository
        self.song_repository = song_repository

    async def create(self, schema: SongTaskCreateSchema) -> SongTaskSchema:
        request = AITaskCreateRequestSchema(
            is_auto=int(not schema.with_voice),
            prompt=schema.prompt,
            instrumental=int(schema.with_voice)
        )

        logger.debug("Sending submit request to AI: " + str(request.model_dump()))
        response = await self.ai_repository.submit(request)
        if response is None:
            raise HTTPException(500)
        logger.debug("Receive response: " + str(response.model_dump()))
        if not response.data:
            raise HTTPException(400)
        task = response.data[0]

        schema = SongTaskSchema(
            id=task.song_id,
            is_finished=task.status == AITaskStatus.finished,
            audio_url=(task.audio if task.status == AITaskStatus.finished else None)
        )
        await self.song_repository.store(schema)
        return schema

    async def get(self, song_id: UUID) -> SongTaskSchema:
        cached = await self.song_repository.get(str(song_id))
        if cached is not None and cached.is_finished:
            return cached

        response = await self.ai_repository.query(str(song_id))
        if not response.data:
            raise HTTPException(404)
        task = response.data[0]

        schema = SongTaskSchema(
            id=song_id,
            is_finished=task.status == AITaskStatus.finished,
            audio_url=(task.audio if task.status == AITaskStatus.finished else None)
        )
        await self.song_repository.store(schema)
        return schema

