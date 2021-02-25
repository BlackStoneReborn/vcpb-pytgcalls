from os import getenv
import asyncio
import json
from random import choice

import httpx
from dotenv import load_dotenv

from helpers import random_string

load_dotenv("server.env")

URL = f'http://{getenv("HOST")}:{getenv("PORT")}/api_internal'
SESSION_ID = getenv("SESSION_ID")

httpx_client = httpx.AsyncClient()


async def join(chat_id: int, file_path: str, bitrate: int = 48000) -> httpx.Response:
    return await httpx_client.post(
        URL,
        content=json.dumps(
            {
                "action": "join_call",
                "chat_id": chat_id,
                "file_path": file_path,
                "bitrate": bitrate,
                "session_id": SESSION_ID
            }
        )
    )


async def change(chat_id: int, file_path: str) -> httpx.Response:
    return await httpx_client.post(
        URL,
        content=json.dumps(
            {
                "action": "change_stream",
                "chat_id": chat_id,
                "file_path": file_path,
                "session_id": SESSION_ID
            }
        )
    )


async def leave(chat_id: int, leave_type: str = "requested") -> httpx.Response:
    return await httpx_client.post(
        URL,
        content=json.dumps(
            {
                "action": "leave_call",
                "chat_id": chat_id,
                "type": leave_type,
                "session_id": SESSION_ID
            }
        )
    )


async def pause(chat_id: int) -> httpx.Response:
    return await httpx_client.post(
        URL,
        content=json.dumps(
            {
                "action": "pause",
                "chat_id": chat_id,
                "session_id": SESSION_ID
            }
        )
    )


async def resume(chat_id: int) -> httpx.Response:
    return await httpx_client.post(
        URL,
        content=json.dumps(
            {
                "action": "resume",
                "chat_id": chat_id,
                "session_id": SESSION_ID
            }
        )
    )


async def youtube(url: str, cids: str):
    cid = str(cids)
    file_name = f'{cid.replace("-", "")}.raw'

    proc = await asyncio.create_subprocess_shell(
        'ffmpeg -i "$(python3 -m youtube_dl -x -g "url")" -f s16le -ac 1 -ar 48000 -acodec pcm_s16le output'.replace(
            "url",
            url
        ).replace("output", file_name),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()

    result = stdout or stderr

    if proc.returncode == 0:
        return True, file_name, result

    return False, file_name, result
