import os
from pathlib import Path
from urllib.parse import urlparse

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class WatchdogSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=None,
        extra="ignore",
        env_prefix="WD_",
    )
    is_running: bool = Field(default=False)
    """运行中"""
    restart_count: int = Field(default=0)
    """重启次数"""
    remove_session_after_restart: int = Field(default=3)
    """重启失败几次后删除会话文件"""
    max_restart_count: int = Field(default=6)
    """意外断开连接时，最大重启次数"""
    exit_flag: bool = Field(default=False)
    """退出标志"""

    def update_bot_restart_count(self):
        self.restart_count += 1
        os.environ["RESTART_COUNT"] = str(self.restart_count)

    def reset_bot_restart_count(self):
        self.restart_count = 0
        os.environ["RESTART_COUNT"] = "0"


class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    admins: list[int] = Field(...)
    """管理员 ID 列表"""
    bot_token: str = Field(...)
    api_id: str = Field(...)
    api_hash: str = Field(...)
    bot_proxy: dict | None = Field(default=None)
    bot_workdir: Path = Field(default=Path("sessions"))
    debug: bool = Field(default=False)

    def model_post_init(self, __context) -> None:
        """模型初始化后的操作"""
        self.bot_workdir.mkdir(parents=True, exist_ok=True)

    @field_validator("admins", mode="before")
    @classmethod
    def parse_admins(cls, v):
        if isinstance(v, list):
            return [int(x) if not isinstance(x, int) else x for x in v]
        if isinstance(v, int):
            return [v]
        if isinstance(v, str):
            return [int(x.strip()) for x in v.replace(" ", "").split(",") if x.strip()]
        return v

    @field_validator("bot_proxy", mode="before")
    @classmethod
    def proxy_config(cls, v: str | None = None) -> dict | None:
        url = urlparse(v) if v else None
        if not url:
            return None
        return {
            "scheme": url.scheme,
            "hostname": url.hostname,
            "port": url.port,
            "username": url.username,
            "password": url.password,
        }

    @property
    def bot_seesion_name(self) -> str:
        return f"bot_{self.bot_token.split(':')[0]}"


bs = BotSettings()  # type: ignore
ws = WatchdogSettings()  # type: ignore
