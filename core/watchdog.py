import asyncio
import os
import sys

from pyrogram import Client

from log import logger

from .config import ws

logger = logger.bind(name="Watchdog")


async def reset_count_task():
    """重置重启次数任务"""
    logger.info(f"第 {ws.restart_count} 次重启成功, 稳定运行 10 分钟后重置重启次数")
    await asyncio.sleep(600)
    ws.reset_bot_restart_count()
    logger.info("已稳定运行 10 分钟, 重启次数已重置")


async def on_connect(_, __) -> None:
    """Bot 连接成功回调函数"""
    ws.is_running = True
    logger.info("Bot 开始运行...")

    if not ws.restart_count:
        return
    asyncio.create_task(reset_count_task())


async def on_disconnect(cli: Client, __) -> None:
    """Bot 断开连接回调函数"""
    if ws.exit_flag:
        ws.is_running = False

    # 正常退出
    if ws.exit_flag and not ws.is_running:
        logger.info("Bot 已结束运行")
        return

    # 启动失败
    if not ws.is_running and not ws.restart_count:
        exit("Bot 连接失败, 请检查设备网络和代理配置")

    # 断开连接
    if ws.restart_count >= ws.max_restart_count:
        exit(f"重启次数已达上限 ({ws.max_restart_count} 次), 结束进程")

    try:
        ws.update_bot_restart_count()
        logger.warning(f"Bot 已断开连接, 尝试重启... | {ws.restart_count}/{ws.max_restart_count}")

        if ws.restart_count == ws.remove_session_after_restart:
            await remove_session_file(cli)

        python = sys.executable
        os.execv(python, [python] + sys.argv)
    except Exception as e:
        logger.exception(e)
        exit("重启失败, 结束进程, 以上为错误信息")


async def remove_session_file(cli: Client) -> None:
    """删除会话文件"""
    logger.warning("尝试删除会话文件...")
    try:
        await cli.session.stop()
        await cli.storage.close()
        if (session := cli.workdir / f"{cli.name}.session") and session.exists():
            os.remove(session)
            logger.warning(f"会话文件已移除: {session}")
    except Exception as e:
        logger.error(f"移除会话文件失败: {e}")
