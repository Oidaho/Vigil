# ./VK-Vigil/config/web.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class JWTSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="jwt_")

    secret: str = "secret"
    algorithm: str = "HS512"
    access_token_lifetime: int = 120  # minutes
    refresh_token_lifetime: int = 7  # days


class WebpanelSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="web_")

    jwt: JWTSettings = JWTSettings()
    admin_id: int = 1
    password: str = "password"
