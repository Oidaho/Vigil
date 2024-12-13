# ./VK-Vigil/config/database.py

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="db_")

    dialect: Optional[str] = "sqlite"
    user: Optional[str]
    password: Optional[str]
    hostname: Optional[str]
