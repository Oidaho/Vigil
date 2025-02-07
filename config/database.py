# ./VK-Vigil/config/database.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="VIGIL_DB_")

    # Обязательные переменные
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str

    # Опциональные переменные
    POSTGRES_USER: str = "vigil"
    POSTGRES_NAME: str = "bot"
    POSTGRES_PORT: int = 5432
