from pyrogram import Client as Bot, filters
from pyrogram.types import Message
from pyrogram.errors import InviteHashExpired, InviteHashInvalid, UserAlreadyParticipant
import asyncio
import vcpb
import json
import os.path
from os import remove
from helpers import is_youtube
from config import API_ID, API_HASH, BOT_TOKEN

bot = Bot(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN
)

@bot.on_message(
    filters.command(["leave", "stop"])
    & filters.group
    & ~ filters.edited
)
async def leave(bot: Bot, message: Message):
    await vcpb.leave(message.chat.id)
    remove(f'{message.chat.id.replace("-", "")}.raw')
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
    file_path = (await vcpb.youtube(url, message.chat.id))[1]
    await message.edit_text("Joining...")
    await vcpb.join(message.chat.id, file_path)
    await message.edit_text(f"`[{file_path}] Playing...`")


@bot.on_message(
    filters.command(["tgfile", "tg_file"])
    & filters.group
    & ~ filters.edited
)
async def tgfile(bot: Bot, message: Message):
    file_input = f'./{str(message.chat.id).replace("-", "")}.mp3'
    file_path = f'{str(message.chat.id).replace("-", "")}.raw'
    if message.reply_to_message.media:
        await message.reply_to_message.download(file_name=file_input)
    proc = await asyncio.create_subprocess_shell(
        'ffmpeg -i puthh -f s16le -ac 1 -ar 48000 -acodec pcm_s16le output'.replace(
            "puthh",
            file_input
        ).replace("output", file_path),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    print(stdout or stderr)
    if not proc.returncode == 0:
        await message.reply_text("Something went wrong with this file!")
        return
    remove(file_input)
    await message.reply_text(f"NOW PLAYING\n\nTG-File")

bot.run()
