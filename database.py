import json
from typing import Dict

from bot import bot
from pyrogram.errors import MessageNotModified


class DB:
    CHANNEL_ID = -1001206543486
    PLAYING_MSG_ID = 2
    CURR_PLAYING_MSG_ID = 4


async def load_data(msg_id: int) -> Dict:
    msg = await bot.get_messages(DB.CHANNEL_ID, msg_id)
    if msg:
        return json.loads(msg.text)
    return {}


async def save_data(msg_id: int, text: str) -> None:
    try:
        await bot.edit_message_text(
            DB.CHANNEL_ID,
            msg_id,
            f"`{text}`",
            disable_web_page_preview=True
        )
    except MessageNotModified:
        pass
