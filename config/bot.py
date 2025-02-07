# ./VK-Vigil/config/bot.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="VIGIL_BOT_")

    # Обязательные переменные
    GROUP_ID: int
    GROUP_TOKEN: str

    # Опциональные переменные
    API_VERSION: str = "5.199"
    COMMAND_PREFIX: str = "/"
    MAX_SANCTION_POINTS: int = 5
