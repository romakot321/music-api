from fastapi import APIRouter, Depends, Request, Header, HTTPException, Response
from fastapi import BackgroundTasks
from uuid import UUID
import os

from app.schemas.song import SongTaskSchema, SongTaskCreateSchema
from app.services.song import SongService
from slowapi.util import get_remote_address
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/song", tags=["Song"])
valid_access_token = os.getenv("ACCESS_TOKEN", "123")


@router.post(
    '',
    response_model=SongTaskSchema,
    description="""
        Endpoint for start a task for music generation.
        Music can be pure or with voice. Voice will be generated also from prompt.
        For do request you need to specify Access-Token header, ask me in telegram about it.

        This endpoint rate-limited to 4 requests per minute.
    """
)
@limiter.limit("4/minute")
async def create_song_task(
        schema: SongTaskCreateSchema,
        request: Request,
        background_tasks: BackgroundTasks,
        access_token: str = Header(),
        service: SongService = Depends()
):
    if access_token != valid_access_token:
        raise HTTPException(401)
    response = await service.create()
    print(response)
    background_tasks.add_task(service.send, schema, response.id)
    return response

@router.get(
    '/{song_id}',
    response_model=SongTaskSchema,
    description="""
        Endpoint for check the task of music generation status.
        For do request you need to specify Access-Token header, ask me in telegram about it.

        This endpoint rate-limited to 10 requests per minute.
    """
)
@limiter.limit("10/minute")
async def get_song_task(
        song_id: UUID,
        request: Request,
        access_token: str = Header(),
        service: SongService = Depends()
):
    if access_token != valid_access_token:
        raise HTTPException(401)
    return await service.get(song_id)

