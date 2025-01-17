from fastapi import FastAPI
from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_utils.tasks import repeat_every
from pydantic_settings import BaseSettings
from loguru import logger
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager

from app.repositories.ai import AIRepository
from app.services.song import SongService


class ProjectSettings(BaseSettings):
    LOCAL_MODE: bool = False


def register_exception(application):
    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
        # or logger.error(f'{exc}')
        logger.debug(f'{exc}')
        content = {'status_code': 422, 'message': exc_str, 'data': None}
        return JSONResponse(
            content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    application.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


def register_cors(application):
    application.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

@repeat_every(seconds=15)
async def songs_update_task():
    try:
        await SongService.update_songs_status()
    except Exception as e:
        logger.exception(e)


@asynccontextmanager
async def lifespan(app):
    await songs_update_task()
    await AIRepository.login()
    yield


def init_web_application():
    project_settings = ProjectSettings()
    application = FastAPI(
        openapi_url='/openapi.json',
        docs_url='/docs',
        redoc_url='/redoc',
        lifespan=lifespan
    )

    if project_settings.LOCAL_MODE:
        register_exception(application)
        register_cors(application)

    from app.routes.song import router as song_router

    application.include_router(song_router)

    return application


def run() -> FastAPI:
    application = init_web_application()
    return application


fastapi_app = run()
