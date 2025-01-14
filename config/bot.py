# ./VK-Vigil/config/bot.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="bot_")

    group_id: int = 0
    acces_token: str = "token"
    api_version: str = "5.199"
    command_prefix: str = "/"
    max_warns: int = 5
