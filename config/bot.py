# ./VK-Vigil/config/bot.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="bot_")

    group_id: int
    acces_token: str
    secret_key: str
    api_version: str = "5.199"
