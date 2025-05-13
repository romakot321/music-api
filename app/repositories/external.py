from aiohttp import ClientSession, MultipartWriter, ClientTimeout
from loguru import logger
import os

from app.schemas.external import ExternalTaskCreateRequestSchema, ExternalTaskCreateResponseSchema
from app.schemas.external import ExternalTaskStatusResponseSchema


class ExternalRepository:
    REQUEST_TIMEOUT = 5 * 60
    base_url = 'https://api.topmediai.com'
    token = os.getenv("API_TOKEN")

    async def _do_request(self, method, url: str, json: dict = None, headers = None, params: dict = None, data=None):
        session_timeout = ClientTimeout(total=None, sock_connect=self.REQUEST_TIMEOUT, sock_read=self.REQUEST_TIMEOUT)
        async with ClientSession(timeout=session_timeout, base_url=self.base_url, headers={"x-api-key": self.token}) as session:
            async with session.request(method, url, json=json, headers=headers, params=params, data=data) as resp:
                assert resp.status // 100 == 2, await resp.text()
                return await resp.json()

    async def generate(self, schema: ExternalTaskCreateRequestSchema) -> ExternalTaskCreateResponseSchema:
        session_timeout = ClientTimeout(total=None, sock_connect=self.REQUEST_TIMEOUT, sock_read=self.REQUEST_TIMEOUT)
        async with ClientSession(timeout=session_timeout) as session:
            resp = await self._do_request(
                "POST",
                "/v2/submit",
                json=schema.model_dump(exclude_none=True),
            )
            logger.debug("Generate response: " + str(resp))
            return ExternalTaskCreateResponseSchema.model_validate(resp)

    async def generate_lyrics(self, prompt: str) -> str:
        response = await self._do_request(
            "POST",
            "/v1/lyrics",
            json={"prompt": prompt}
        )
        logger.debug("Lyrics response: " + str(response))
        return response["data"]["text"]

    async def query(self, song_id: str) -> ExternalTaskStatusResponseSchema:
        response = await self._do_request(
            "GET",
            "/v2/query",
            params={"song_id": song_id},
        )
        logger.debug("Query response: " + str(response))
        return ExternalTaskStatusResponseSchema.model_validate(response)
