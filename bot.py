from pyrogram import Client as Bot, filters
from pyrogram.types import Message

import vcpb
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
    await message.delete()


@bot.on_message(
    filters.command("pause")
    & filters.group
    & ~ filters.edited
)
async def pause(bot: Bot, message: Message):
    await vcpb.pause(message.chat.id)
    await message.delete()


@bot.on_message(
    filters.command("resume")
    & filters.group
    & ~ filters.edited
)
async def resume(bot: Bot, message: Message):
    await vcpb.resume(message.chat.id)
    await message.delete()


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
    else:
        message = await message.reply_text("Downloading...")
        file_path = (await vcpb.youtube(url))[1]
        message = await message.edit_text("Joining...")

        await vcpb.join(message.chat.id, file_path)
        await message.edit_text(f"`[{file_path}] Playing...`")


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


@bot.on_message(
    filters.command(["playtg", "play_tg"])
    & filters.group
    & ~ filters.edited
)
async def playtg(bot: Bot, message: Message):
    #if not message.audio:
        #await message.reply_text(f"`Reply to a Audio-File!`")
        #return
    res, name, out = await vcpb.tgfile(message)
    if not res:
        await message.reply_text(f"`{out}`")
        return
    
    await vcpb.join(message.chat.id, f"{message.chat.id}.raw")
    await message.reply_text(f"`Now playing: TG-File`")

bot.run()
