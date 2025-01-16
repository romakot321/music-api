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
            prompt=schema.prompt,
            lyrics=(schema.prompt if schema.with_voice else "[Instrumental]"),
            instrumental=int(not schema.with_voice)
        )

        logger.debug("Sending submit request to AI: " + str(request.model_dump()))
        response = await self.ai_repository.generate(request)
        logger.debug("Receive response: " + str(response.model_dump()))
        if not response.data or not response.data[0].music:
            raise HTTPException(400)
        song = response.data[0]

        schema = SongTaskSchema(
            id=song.uuid,
            is_finished=0,
            audio_url=self.ai_repository.make_audio_url(song)
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
            id=str(song_id),
            is_finished=task.status == AITaskStatus.finished,
            audio_url=(cached.audio_url if cached is not None else "")
        )
        await self.song_repository.store(schema)
        return schema

