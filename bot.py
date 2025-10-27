import asyncio
import sys

from pyrogram import Client
from pyrogram.handlers import ConnectHandler, DisconnectHandler

from config.config import bs, ws
from log import logger
from utils.optimized_event_loop import setup_optimized_event_loop
from watchdog import on_connect, on_disconnect

logger.remove()

if bs.debug:
    logger.add(sys.stderr, level="DEBUG")
    logger.debug("Debug 模式已启用")
else:
    logger.add("logs/bot.log", rotation="10 MB", level="INFO")
    logger.add(sys.stderr, level="INFO")

setup_optimized_event_loop()
loop = asyncio.new_event_loop()


class Bot(Client):
    def __init__(self):
        super().__init__(
            f"{bs.bot_token.split(':')[0]}_bot",
            api_id=bs.api_id,
            api_hash=bs.api_hash,
            bot_token=bs.bot_token,
            plugins={"root": "plugins"},
            proxy=bs.bot_proxy,
            loop=loop,
            workdir="session",
        )

    async def start(self, **kwargs):
        self.init_watchdog()
        await super().start()

    async def stop(self, *args):
        ws.exit_flag = True
        await super().stop()

    def init_watchdog(self):
        self.add_handler(ConnectHandler(on_connect))
        self.add_handler(DisconnectHandler(on_disconnect))


if __name__ == "__main__":
    bot = Bot()
    bot.run()
