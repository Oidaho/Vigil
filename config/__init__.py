# ./VK-Vigil/config/__init__.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from .database import DatabaseSettings
from .bot import BotSettings
from .webpanel import WebpanelSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="VIGIL_")

    # Подгруппы
    database: DatabaseSettings
    bot: BotSettings
    web: WebpanelSettings

    # Опциональные переменные
    DEBUG_MODE: bool = False
    PROJECT_NAME: str = "Vigil"


configs = Settings()


__all__ = ("configs",)
