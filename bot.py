from pyrogram import Client as Bot, filters
from pyrogram.types import Message
from pyrogram.errors import InviteHashExpired, InviteHashInvalid, UserAlreadyParticipant
from asyncio import sleep
import vcpb
import json
import os.path
from helpers import is_youtube
from config import API_ID, API_HASH, BOT_TOKEN
from database import DB, save_data, load_data


bot = Bot(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN
)


PLAYING_MSG_MSG_ID = await load_data(DB.PLAYING_MSG_ID)
CURR_PLAYING_MSG_ID = await load_data(DB.CURR_PLAYING_MSG_ID)


@bot.on_message(
    filters.command(["leave", "stop"])
    & filters.group
    & ~ filters.edited
)
async def leave(bot: Bot, message: Message):
    await vcpb.leave(message.chat.id)
    await message.reply_text("Left.")

@bot.on_message(
    filters.command("pause")
    & filters.group
    & ~ filters.edited
)
async def pause(bot: Bot, message: Message):
    await vcpb.pause(message.chat.id)
    await message.reply_text("Paused.")


@bot.on_message(
    filters.command("resume")
    & filters.group
    & ~ filters.edited
)
async def resume(bot: Bot, message: Message):
    await vcpb.resume(message.chat.id)
    await message.reply_text("Resumed.")


@bot.on_message(
    filters.command(["play", "youtube"])
    & filters.group
    & ~ filters.edited
)
async def youtube(bot: Bot, message: Message):
    url = ""
    try:
        url = message.command[1]
    except IndexError:
        url = message.reply_to_message.text

    if not is_youtube(url):
        await message.reply_text("Give me a YouTube link.")
        return
    if not message.chat.username:
        await message.reply_text("This chat is not public! Please set it a username to use me.")
        return
    message = await message.reply_text("Downloading...")
    file_path = (await vcpb.youtube(url))[1]
    await message.edit_text("Joining...")
    await vcpb.join(message.chat.id, file_path)
    await message.edit_text(f"`[{file_path}] Playing...`")
    if not CURR_PLAYING_MSG_ID.get(str(chat_id)):
        CURR_PLAYING_MSG_ID[str(chat_id)] = {}
    CURR_PLAYING_MSG_ID[str(chat_id)] = message.message_id
    await save_data(DB.CURR_PLAYING_MSG_ID, json.dumps(CURR_PLAYING_MSG_ID))

    if not PLAYING_MSG_MSG_ID.get(str(chat_id)):
        PLAYING_MSG_MSG_ID[str(chat_id)] = {}
    PLAYING_MSG_MSG_ID[str(chat_id)]['file'] = file_path
    await save_data(DB.PLAYING_MSG_ID, json.dumps(PLAYING_MSG_MSG_ID))


@bot.on_message(
    filters.command(["playfile", "play_file"])
    & filters.group
    & ~ filters.edited
)
async def playfile(bot: Bot, message: Message):
    file_path = ""

    try:
        file_path = message.command[1]
    except IndexError:
        file_path = message.reply_to_message.text

    if "[" in file_path:
        file_path = file_path.split()[0][:-1][1:]

    if not file_path:
        await message.reply_text("Give me a file.")
    else:
        await vcpb.join(message.chat.id, file_path)
        await message.reply_text(f"`[{file_path}] Playing...`")

bot.run()
