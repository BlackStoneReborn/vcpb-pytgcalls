from pyrogram import Client as TelegramClient
from pytgcalls import PyTgCalls
from os import remove
from config import SESSION_NAME, API_ID, API_HASH

telegram_client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
pytgcalls = PyTgCalls()
open("server.env", "w+").write(
    "\n".join(
        f"{k}={v!r}" for k, v in {"HOST": pytgcalls._host, "PORT": pytgcalls._port, "SESSION_ID": pytgcalls._session_id}.items()
    )
)


@pytgcalls.on_stream_end()
def onend(chats: str):
    chat = str(chats)
    pytgcalls.leave_group_call(chat)
    remove(f'{chat.replace("-", "")}.raw')


pytgcalls.run(telegram_client)
