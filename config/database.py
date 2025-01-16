# ./VK-Vigil/config/database.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="db_")

    user: str = "user"
    password: str = "password"
    hostname: str = "example.com"
    database: str = "db"
    port: int = 5432
