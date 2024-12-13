# ./VK-Vigil/config/__init__.py

from pydantic_settings import BaseSettings
from .database import DatabaseSettings
from .chache import CacheSettings
from .bot import BotSettings


class Settings(BaseSettings):
    database: DatabaseSettings = DatabaseSettings()
    cahce: CacheSettings = CacheSettings()
    bot: BotSettings = BotSettings()
    debug_mode: bool = False
    project_name: str = "Vigil"


configs = Settings()


__all__ = ("configs",)
