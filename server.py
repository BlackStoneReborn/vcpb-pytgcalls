from pyrogram import Client as TelegramClient
from pytgcalls import PyTgCalls

from config import SESSION_NAME, API_ID, API_HASH

telegram_client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
pytgcalls = PyTgCalls()
open("server.env", "w+").write(
    "\n".join(
        f"{k}={v!r}" for k, v in {"HOST": pytgcalls._host, "PORT": pytgcalls._port, "SESSION_ID": pytgcalls._session_id}.items()
    )
)
pytgcalls.run(telegram_client)
