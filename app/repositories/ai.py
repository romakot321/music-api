import os
import hashlib
import asyncio
from aiohttp import ClientSession, MultipartWriter, ClientTimeout
from pydantic import ValidationError
from loguru import logger
from uuid import uuid4

from app.schemas.ai import AITaskCreateRequestSchema, AITaskCreateResponseSchema
from app.schemas.ai import AITaskStatusResponseSchema, AISongSchema

token = os.getenv("API_TOKEN")
member_id = os.getenv("API_MEMBER_ID")


def _pack_generate_schema(**data):
    a = """-----------------------------406336764539455136491136147690
Content-Disposition: form-data; name="mv"

v4.0
-----------------------------406336764539455136491136147690
Content-Disposition: form-data; name="lyrics"

{lyrics}
-----------------------------406336764539455136491136147690
Content-Disposition: form-data; name="gender"

random
-----------------------------406336764539455136491136147690
Content-Disposition: form-data; name="instrumental"

{instrumental}
-----------------------------406336764539455136491136147690
Content-Disposition: form-data; name="g_num"

2
-----------------------------406336764539455136491136147690
Content-Disposition: form-data; name="is_public"

0
-----------------------------406336764539455136491136147690
Content-Disposition: form-data; name="is_auto"

0
-----------------------------406336764539455136491136147690
Content-Disposition: form-data; name="prompt"

{prompt}
-----------------------------406336764539455136491136147690
Content-Disposition: form-data; name="token"

{token}
-----------------------------406336764539455136491136147690--"""
    return a.format(**data)


class AIRepositoryMocked:
    async def generate(self, schema: AITaskCreateRequestSchema) -> AITaskCreateResponseSchema:
        await asyncio.sleep(1)  # Simulating request sending
        return AITaskCreateResponseSchema(
            status=200,
            message="Success",
            data=[
                AISongSchema(
                    id=100000,
                    is_public=0,
                    music=[
                        {"audio_duration": "Infinite", "audio_file": "http://example.com",
                        "image_file": "http://example.com", "item_uuid": str(uuid4()),
                        "lyric": schema.lyrics, "tags": schema.prompt, "title": "title"}
                    ],
                    part=1,
                    uuid=str(uuid4())
                )
            ]
        )

    async def query(self, song_id: str) -> AITaskStatusResponseSchema:
        await asyncio.sleep(1)  # Simulating request sending
        return AITaskStatusResponseSchema(
            status=200,
            message="Success",
            data=[
                AITaskStatusData(
                    status=0,
                    uuid=song_id,
                    info=[{"audio_duration": 100, "audio_file": "asdfa", "image_file": "safdda"}]
                )
            ]
        )

    def make_audio_url(self, song: AISongSchema) -> str:
        return "https://google.com"

    @classmethod
    async def login(cls):
        pass


class AIRepository:
    base_url = 'https://api.topmediai.com'
    email = os.getenv("API_EMAIL")
    password = hashlib.md5(os.getenv("API_PASSWORD").encode()).hexdigest()
    REQUEST_TIMEOUT = 5 * 60

    def __init__(self):
        global token, member_id
        self.token = token
        self.member_id = member_id

    async def _do_request(self, method, url: str, json: dict = None, headers = None, params: dict = None, data=None):
        session_timeout = ClientTimeout(total=None, sock_connect=self.REQUEST_TIMEOUT, sock_read=self.REQUEST_TIMEOUT)
        async with ClientSession(timeout=session_timeout) as session:
            async with session.request(method, url, json=json, headers=headers, params=params, data=data) as resp:
                assert resp.status // 100 == 2, await resp.text()
                return await resp.json()

    async def _get_balance(self) -> int:
        if self.token is None:
            raise ValueError("Try to do request while not logged in")
        response = await self._do_request(
            "GET",
            "https://tp-gateway-api.topmediai.com/tp_member/permission/info",
            params={"product_id": 12, "token": self.token},
            headers={"Authorization": self.token, "Token": self.token}
        )
        return response["data"]["music"]["left"]

    async def _login(self) -> dict:
        global token, member_id
        response = await self._do_request(
            "POST",
            "https://account-api.topmediai.com/account/login",
            params={
                "email": self.email,
                "password": self.password,
                "information_sources": "https://account.topmediai.com",
                "source_site": "www.topmediai.com"
            }
        )
        logger.debug("Login response: " + str(response))
        if not response["data"]:
            raise ValueError("Invalid api credentials")
        self.member_id = response["data"]["member_id"]
        self.token = response["data"]["token"]
        token = self.token
        member_id = self.member_id

    async def generate(self, schema: AITaskCreateRequestSchema) -> AITaskCreateResponseSchema:
        session_timeout = ClientTimeout(total=None, sock_connect=self.REQUEST_TIMEOUT, sock_read=self.REQUEST_TIMEOUT)
        async with ClientSession(timeout=session_timeout) as session:
            resp = await session.post(
                "https://aimusic-api.topmediai.com/generate/music",
                data=_pack_generate_schema(**(schema.model_dump() | {"token": self.token})),
                headers={"Authorization": self.token, "Token": self.token, "Content-Type": "multipart/form-data; boundary=---------------------------406336764539455136491136147690"},
            )
            assert resp.status // 100 == 2, await resp.text()
            data = await resp.json()
            logger.debug("Generate response: " + str(data))
            if isinstance(data["data"], dict) and (data["data"].get('code') == -2 or data.get("message") == "Unauthorized"):
                await self._login()
                return await self.generate(schema)
            return AITaskCreateResponseSchema.model_validate(data)

    async def generate_lyrics(self, prompt: str) -> str:
        if self.token is None:
            raise ValueError("Try to do request while not logged in")
        response = await self._do_request(
            "GET",
            "https://aimusic-api.topmediai.com/v2/prompt-to-lyrics",
            params={"prompt": prompt, "token": self.token},
            headers={"Authorization": self.token, "Token": self.token}
        )
        logger.debug("Lyrics response: " + str(response))
        if isinstance(response["data"], dict) and (response["data"].get('code') == -2 or response.get("message") == "Unauthorized"):
            await self._login()
            return await self.generate_lyrics(prompt)

        return response["data"]["lyrics"]

    async def query(self, song_id: str) -> AITaskStatusResponseSchema:
        if self.token is None:
            raise ValueError("Try to do request while not logged in")
        response = await self._do_request(
            "GET",
            "https://aimusic-api.topmediai.com/generate/query",
            params={"uuid": song_id, "token": self.token},
            headers={"Authorization": self.token, "Token": self.token}
        )
        logger.debug("Query response: " + str(response))
        if isinstance(response["data"], dict) and (response["data"].get('code') == -2 or response.get("message") == "Unauthorized"):
            await self._login()
            return await self.query(song_id)
        return AITaskStatusResponseSchema.model_validate(response)

    def make_audio_url(self, song: AISongSchema) -> str:
        # return "https://files.topmediai.com/aimusic/{m}/{i}-audio.mp3".format(m=self.member_id, i=song.music[0].item_uuid)
        return "https://files.topmediai.com/aimusic/{i}/{t}.mp3".format(t=song.music[0].title, i=song.music[0].item_uuid)

    def make_image_url(self, song: AISongSchema) -> str:
        # return "https://files.topmediai.com/aimusic/{m}/{i}-image.png".format(m=self.member_id, i=song.music[0].item_uuid)
        return "https://files.topmediai.com/aimusic/app/{i}/{t}.jpeg".format(t=song.music[0].title, i=song.music[0].item_uuid)

    @classmethod
    async def login(cls):
        global token
        if token is None:
            self = cls()
            await self._login()
            logger.debug("Left balance: " + str(await self._get_balance()))


if int(os.getenv("USE_MOCK", 0)):
    AIRepository = AIRepositoryMocked
