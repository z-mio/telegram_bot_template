import asyncio

from pyrogram import Client
from pyrogram.handlers import ConnectHandler, DisconnectHandler
from pyrogram.types import BotCommand

from core.config import bs, ws
from core.watchdog import on_connect, on_disconnect
from log import logger, setup_logging
from utils.event_loop import setup_optimized_event_loop

setup_logging(debug=bs.debug)

setup_optimized_event_loop()
loop = asyncio.new_event_loop()


class Bot(Client):
    def __init__(self):
        super().__init__(
            bs.bot_session_name,
            api_id=bs.api_id,
            api_hash=bs.api_hash,
            bot_token=bs.bot_token,
            plugins={"root": "plugins"},
            proxy=bs.bot_proxy,
            loop=loop,
            workdir=bs.bot_workdir,
        )

    async def start(self, **kwargs):
        self.init_watchdog()
        await super().start()
        await self.set_menu()

    async def stop(self, *args):
        ws.exit_flag = True
        await super().stop()

    def init_watchdog(self):
        self.add_handler(ConnectHandler(on_connect))
        self.add_handler(DisconnectHandler(on_disconnect))

    async def set_menu(self):
        commands = {
            "start": "开始",
            "help": "帮助",
        }
        await self.set_bot_commands([BotCommand(command=k, description=v) for k, v in commands.items()])
        logger.debug(f"菜单已设置: {commands}")


if __name__ == "__main__":
    bot = Bot()
    bot.run()
