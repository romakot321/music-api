from fastapi import APIRouter, Depends, Request, Header, HTTPException, Response
from fastapi import BackgroundTasks
from uuid import UUID
import os

from app.schemas.song import (
    SongLyricsGenerateSchema,
    SongLyricsSchema,
    SongTaskSchema,
    SongTaskCreateSchema,
)
from app.services.song import SongService

router = APIRouter(prefix="/song", tags=["Song"])
valid_access_token = os.getenv("ACCESS_TOKEN", "123")


@router.post(
    "",
    response_model=SongTaskSchema,
    description="""
        Endpoint for start a task for music generation.
        Music can be pure or with voice. Voice will be generated also from prompt.
        For do request you need to specify Access-Token header, ask me in telegram about it.
    """,
)
async def create_song_task(
    schema: SongTaskCreateSchema,
    access_token: str = Header(),
    service: SongService = Depends(),
):
    if access_token != valid_access_token:
        raise HTTPException(401)
    return await service.create(schema)


@router.post("/lyrics", response_model=SongLyricsSchema)
async def generate_lyrics_from_prompt(
    schema: SongLyricsGenerateSchema,
    access_token: str = Header(),
    service: SongService = Depends(),
):
    if access_token != valid_access_token:
        raise HTTPException(401)
    return await service.generate_lyrics(schema)


@router.get(
    "/{song_id}",
    response_model=SongTaskSchema,
    description="""
        Endpoint for check the task of music generation status.
        For do request you need to specify Access-Token header, ask me in telegram about it.
    """,
)
async def get_song_task(
    song_id: UUID,
    access_token: str = Header(),
    service: SongService = Depends(),
):
    if access_token != valid_access_token:
        raise HTTPException(401)
    return await service.get(song_id)
