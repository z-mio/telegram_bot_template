from pathlib import Path
from typing import Annotated, Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class WatchdogSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=None,
        extra="ignore",
        env_prefix="WD_",
    )
    exit_flag: bool = Field(default=False)
    """退出标志"""
    reconnect_grace_seconds: int = Field(default=120)
    """主连接断开后等待自动重连的时间(秒), 超时仍未恢复则结束进程交给容器重启"""


class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    admins: Annotated[list[int], NoDecode]
    """管理员 ID 列表"""
    bot_token: str
    api_id: str
    api_hash: str
    bot_proxy: str | None = Field(default=None)
    bot_workdir: Path = Field(default=Path("sessions"))
    debug: bool = Field(default=False)

    def model_post_init(self, __context: Any) -> None:
        """模型初始化后的操作"""
        self.bot_workdir.mkdir(parents=True, exist_ok=True)

    @field_validator("admins", mode="before")
    @classmethod
    def parse_admins(cls, v: Any) -> list[int]:
        if isinstance(v, list):
            return [int(x) if not isinstance(x, int) else x for x in v]
        if isinstance(v, int):
            return [v]
        if isinstance(v, str):
            return [int(x.strip()) for x in v.replace(" ", "").split(",") if x.strip()]
        raise ValueError("Invalid admins format")

    @property
    def bot_session_name(self) -> str:
        return f"bot_{self.bot_token.split(':')[0]}"


bs = BotSettings()  # type: ignore
ws = WatchdogSettings()
