from pyrogram import filters
from pyrogram.types import Message

from core.config import bs


async def _is_admin(_, __, msg: Message):
    return msg.from_user.id in bs.admins


is_admin = filters.create(_is_admin)
