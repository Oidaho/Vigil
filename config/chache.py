# ./VK-Vigil/config/chahce.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class CacheSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="cahche_")

    host: str = "example.com"
    port: int = 6379
    db: int = 0
