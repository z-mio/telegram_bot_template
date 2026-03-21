from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command(["start", "help"]))
async def start(_, msg: Message):
    await msg.reply_text("呀哈喽!")


@Client.on_message(filters.command("ping"))
async def ping(_, msg: Message):
    await msg.reply_text("Pong!")
