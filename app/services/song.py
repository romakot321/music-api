from fastapi import Depends, HTTPException
from uuid import UUID
from loguru import logger
import asyncio
import datetime as dt

from app.repositories.ai import AIRepository
from app.repositories.song import SongRepository
from app.schemas.song import SongLyricsGenerateSchema, SongLyricsSchema, SongTaskCreateSchema, SongTaskSchema
from app.schemas.ai import AITaskCreateRequestSchema, AITaskCreateResponseSchema
from app.schemas.ai import AITaskStatusResponseSchema, AITaskStatus
from app.db.base import get_session
from app.db.tables import Song


class SongService:
    GENERATE_TIMEOUT = 10 * 60

    def __init__(
            self,
            ai_repository: AIRepository = Depends(),
            song_repository: SongRepository = Depends()
    ):
        self.ai_repository = ai_repository
        self.song_repository = song_repository

    async def create(self, schema: SongTaskCreateSchema) -> SongTaskSchema:
        return await self.song_repository.create(
            user_id=schema.user_id,
            app_bundle=schema.app_bundle,
            prompt=schema.prompt,
            with_voice=schema.with_voice,
            lyrics=schema.lyrics
        )

    async def generate_lyrics(self, schema: SongLyricsGenerateSchema) -> SongLyricsSchema:
        lyrics = await self.ai_repository.generate_lyrics(schema.prompt)
        return SongLyricsSchema(lyrics=lyrics)

    async def _send(self, schema: SongTaskCreateSchema, song_id: UUID):
        await self.song_repository.update(str(song_id), comment="sending")
        request = AITaskCreateRequestSchema(
            prompt=schema.prompt,
            lyrics=(schema.lyrics if schema.with_voice else "[Instrumental]"),
            instrumental=int(not schema.with_voice)
        )

        logger.debug("Sending submit request to AI: " + str(request.model_dump()))
        try:
            response = await self.ai_repository.generate(request)
            logger.debug("Received response: " + str(response.model_dump()))
        except TimeoutError:
            await self.song_repository.update(
                str(song_id),
                is_finished=False,
                is_invalid=True,
                comment="Timeout"
            )
            return schema
        except Exception as e:
            logger.exception(e)
            await self.song_repository.update(
                str(song_id),
                is_finished=False,
                is_invalid=True,
                comment=str(e)
            )
            return schema

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
            comment=None
        )

    async def get(self, song_id: UUID) -> SongTaskSchema:
        return await self.song_repository.get(str(song_id))

    async def _check(self, song: Song):
        if not song.api_id:
            return
        if (dt.datetime.now() - song.updated_at).seconds >= self.GENERATE_TIMEOUT:
            await self.song_repository.update(
                song.id,
                is_invalid=True,
                comment="Timeout"
            )
            return
        response = await self.ai_repository.query(song.api_id)
        if not response.data:
            return
        task = response.data[0]

        await self.song_repository.update(
            song.id,
            api_id=song.api_id,
            is_finished=task.status == AITaskStatus.finished,
            is_invalid=task.status == AITaskStatus.error,
            audio_url=song.audio_url,
            image_url=song.image_url,
            comment=None
        )

    @classmethod
    async def process_songs_queue(cls):
        session_getter = get_session()
        db_session = await anext(session_getter)
        self = cls(ai_repository=AIRepository(), song_repository=SongRepository(session=db_session))

        if (await self.song_repository.is_any_song_generating()):
            return
        songs = await self.song_repository.list_unsended()
        if not songs:
            return
        schema = SongTaskCreateSchema.model_validate(songs[0])
        await self._send(schema, songs[0].id)

        try:
            await anext(session_getter)
        except StopAsyncIteration:
            pass

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

