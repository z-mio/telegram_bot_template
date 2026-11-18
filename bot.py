from typing import Any

from pyrogram import Client
from pyrogram.types import BotCommand

from core.config import bs
from log import logger, setup_logging

setup_logging(debug=bs.debug)

COMMANDS = {
    "start": "开始",
    "help": "帮助",
}


class Bot(Client):
    def __init__(self) -> None:
        super().__init__(
            bs.bot_session_name,
            api_id=bs.api_id,
            api_hash=bs.api_hash,
            bot_token=bs.bot_token,
            plugins={"root": "plugins"},
            proxy=bs.bot_proxy,
            workdir=bs.bot_workdir,
        )

    async def start(self, **kwargs: Any) -> Client:
        await super().start(**kwargs)
        await self.set_menu()
        return self

    async def set_menu(self) -> None:
        commands = await self.get_bot_commands()
        if len(commands) == len(COMMANDS) and all(c.description in str(COMMANDS.values()) for c in commands):
            logger.debug("菜单无变化, 跳过设置")
            return
        await self.set_bot_commands([BotCommand(command=k, description=v) for k, v in COMMANDS.items()])
        logger.debug(f"菜单已设置: {COMMANDS}")


if __name__ == "__main__":
    bot = Bot()
    bot.run()
