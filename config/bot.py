# ./VK-Vigil/config/bot.py

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="bot_")

    group_id: Optional[int]
    acces_token: Optional[str]
    secret_key: Optional[str]
    api_version: Optional[str] = "5.199"
