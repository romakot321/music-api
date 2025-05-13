from fastapi import Depends, HTTPException
from uuid import UUID
from loguru import logger
import asyncio
import datetime as dt

from app.repositories.ai import AIRepository
from app.repositories.external import ExternalRepository
from app.repositories.song import SongRepository
from app.schemas.song import (
    SongLyricsGenerateSchema,
    SongLyricsSchema,
    SongTaskCreateSchema,
    SongTaskSchema,
)
from app.schemas.external import (
    ExternalTaskCreateRequestSchema,
    ExternalTaskCreateResponseSchema,
)
from app.schemas.external import ExternalTaskStatusResponseSchema, ExternalTaskStatus
from app.db.base import get_session
from app.db.tables import Song


class SongService:
    GENERATE_TIMEOUT = 10 * 60

    def __init__(
        self,
        external_repository: ExternalRepository = Depends(),
        song_repository: SongRepository = Depends(),
    ):
        self.external_repository = external_repository
        self.song_repository = song_repository

    async def create(self, schema: SongTaskCreateSchema) -> SongTaskSchema:
        return await self.song_repository.create(
            user_id=schema.user_id,
            app_bundle=schema.app_bundle,
            prompt=schema.prompt,
            with_voice=schema.with_voice,
            lyrics=schema.lyrics,
        )

    async def generate_lyrics(
        self, schema: SongLyricsGenerateSchema
    ) -> SongLyricsSchema:
        logger.debug(schema)
        lyrics = await self.external_repository.generate_lyrics(schema.prompt)
        return SongLyricsSchema(lyrics=lyrics)

    async def _send(self, schema: SongTaskCreateSchema, song_id: UUID):
        await self.song_repository.update(str(song_id), comment="sending")
        request = ExternalTaskCreateRequestSchema(
            prompt=schema.prompt,
            lyrics=schema.lyrics,
            instrumental=int(not schema.with_voice),
        )

        logger.debug("Sending submit request to AI: " + str(request.model_dump()))
        try:
            response = await self.external_repository.generate(request)
            logger.debug("Received response: " + str(response.model_dump()))
        except TimeoutError:
            await self.song_repository.update(
                str(song_id), is_finished=False, is_invalid=True, comment="Timeout"
            )
            return schema
        except Exception as e:
            logger.exception(e)
            await self.song_repository.update(
                str(song_id), is_finished=False, is_invalid=True, comment=str(e)
            )
            return schema

        if not response.data:  # Error occurs, set song to invalid
            await self.song_repository.update(
                str(song_id), is_finished=False, is_invalid=True
            )
            return schema
        song = response.data[0]

        await self.song_repository.update(
            str(song_id),
            api_id=song.song_id,
            is_finished=False,
            audio_url=song.audio,
            image_url=song.image,
            comment=None,
        )

    async def get(self, song_id: UUID) -> SongTaskSchema:
        return await self.song_repository.get(str(song_id))

    async def _check(self, song: Song):
        if not song.api_id or song.updated_at is None:
            return
        if (dt.datetime.now() - song.updated_at).seconds >= self.GENERATE_TIMEOUT:
            await self.song_repository.update(
                str(song.id), is_invalid=True, comment="Timeout"
            )
            return
        response = await self.external_repository.query(song.api_id)
        if not response.data:
            return
        task = response.data[0]

        await self.song_repository.update(
            str(song.id),
            api_id=song.api_id,
            is_finished=task.status == ExternalTaskStatus.finished,
            is_invalid=task.status == ExternalTaskStatus.error,
            audio_url=task.audio,
            image_url=task.image,
            comment=None,
        )

    @classmethod
    async def process_songs_queue(cls):
        session_getter = get_session()
        db_session = await anext(session_getter)
        self = cls(
            external_repository=ExternalRepository(),
            song_repository=SongRepository(session=db_session),
        )

        if await self.song_repository.is_any_song_generating():
            return
        songs = await self.song_repository.list_unsended()
        if not songs:
            return
        for song in songs[:3]:
            schema = SongTaskCreateSchema.model_validate(song)
            await self._send(schema, song.id)

        try:
            await anext(session_getter)
        except StopAsyncIteration:
            pass

    @classmethod
    async def update_songs_status(cls):
        session_getter = get_session()
        db_session = await anext(session_getter)
        self = cls(
            external_repository=ExternalRepository(),
            song_repository=SongRepository(session=db_session),
        )

        songs = await self.song_repository.list_in_progress()
        check_tasks = [self._check(song) for song in songs]
        await asyncio.gather(*check_tasks)
        try:
            await anext(session_getter)
        except StopAsyncIteration:
            pass
