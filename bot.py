import asyncio
import sys

from pyrogram import Client
from pyrogram.handlers import ConnectHandler, DisconnectHandler

from core.config import bs, ws
from core.watchdog import on_connect, on_disconnect
from log import logger, logger_format
from utils.optimized_event_loop import setup_optimized_event_loop

logger.remove()

if bs.debug:
    logger.add(sys.stderr, level="DEBUG", format=logger_format)
    logger.debug("调试模式已启用")
else:
    logger.add(sys.stderr, level="INFO", format=logger_format)
logger.add(
    "logs/bot.log",
    rotation="10 MB",
    level="INFO",
    format=logger_format,
    # serialize=True,
    enqueue=True,
)

setup_optimized_event_loop()
loop = asyncio.new_event_loop()


class Bot(Client):
    def __init__(self):
        super().__init__(
            bs.bot_seesion_name,
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

    async def stop(self, *args):
        ws.exit_flag = True
        await super().stop()

    def init_watchdog(self):
        self.add_handler(ConnectHandler(on_connect))
        self.add_handler(DisconnectHandler(on_disconnect))


if __name__ == "__main__":
    bot = Bot()
    bot.run()
