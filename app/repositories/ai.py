import os
from aiohttp import ClientSession
from pydantic import ValidationError
from loguru import logger

from app.schemas.ai import AITaskCreateRequestSchema, AITaskCreateResponseSchema
from app.schemas.ai import AITaskStatusResponseSchema


class AIRepository:
    base_url = 'https://api.topmediai.com'
    token = os.getenv("X_API_KEY", "invalid")

    async def _post_request(self, path: str, json: dict) -> dict:
        async with ClientSession(self.base_url) as session:
            async with session.post(path, json=json, headers={'x-api-key': self.token}) as response:
                assert response.status // 100 == 2, await response.text()
                return await response.json()

    async def _get_request(self, path: str, params: dict) -> dict:
        async with ClientSession(self.base_url) as session:
            async with session.get(path, params=params, headers={'x-api-key': self.token}) as response:
                assert response.status // 100 == 2, await response.text()
                return await response.json()

    async def submit(self, schema: AITaskCreateRequestSchema) -> AITaskCreateResponseSchema:
        response = await self._post_request('/v2/submit', schema.model_dump())
        try:
            return AITaskCreateResponseSchema.model_validate(response)
        except ValidationError as e:
            logger.error("Invalid submit response: " + str(response))

    async def query(self, song_id: str) -> AITaskStatusResponseSchema:
        response = await self._get_request('/v2/query', {'song_id': song_id})
        return AITaskStatusResponseSchema.model_validate(response)

