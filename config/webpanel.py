# ./VK-Vigil/config/web.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class JWTSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="JWT_")

    # Обязательные переменные
    SECRET: str

    # Опциональные переменные
    ALGORITHM: str = "HS512"
    TOKEN_LIFETIME: int = 120


class WebpanelSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="WEB_")

    # Подгруппы
    jwt: JWTSettings = JWTSettings()

    # Обязательные переменные
    ADMIN_ID: int
    ADMIN_PASSWORD: str
