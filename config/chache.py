# ./VK-Vigil/config/chahce.py

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class CacheSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="cahche_")

    host: Optional[str]
    port: Optional[int] = 6379
    db: Optional[int] = 0
