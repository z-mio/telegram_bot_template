from pathlib import Path
from typing import Annotated, Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


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

    @field_validator("bot_proxy", mode="before")
    @classmethod
    def empty_proxy_to_none(cls, v: Any) -> Any:
        return v or None

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
