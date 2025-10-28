import os
from urllib.parse import urlparse

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class WatchdogSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=None,
        extra="ignore",
    )
    is_running: bool = Field(default=False)
    """运行中"""
    restart_count: int = Field(default=0)
    """重启次数"""
    max_restart_count: int = Field(default=5)
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
    bot_workdir: str = Field(default="sessions")
    debug: bool = Field(default=False)

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


bs = BotSettings()  # type: ignore
ws = WatchdogSettings()  # type: ignore
