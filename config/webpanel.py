# ./VK-Vigil/config/web.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class WebpanelSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="web_")

    admi_id: str = 1
    password: str = "password"
    jwt_secret: str = "secret"
