# ./VK-Vigil/config/web.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class JWTSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="jwt_")

    secret: str = "secret"
    algorithm: str = "HS512"
    access_token_lifetime: int = 30 # minutes
    refresh_token_lifetime: int = 7 # days
    

class WebpanelSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="web_")


    jwt: JWTSettings = JWTSettings()
    admi_id: str = 1
    password: str = "password"
