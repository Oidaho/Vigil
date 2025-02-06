# ./VK-Vigil/config/database.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_")

    # Обязательные переменные
    POSGRES_PASSWORD: str
    POSGRES_HOST: str

    # Опциональные переменные
    POSGRES_USER: str = "vigil"
    POSGRES_NAME: str = "bot"
    POSGRES_PORT: int = 5432
