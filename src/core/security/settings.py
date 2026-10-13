from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class Settings(BaseSettings):
    MAX_SESSIONS: int = 5
    PASSWORD_ENCODING: str = "utf-8"
    #
    # model_config = SettingsConfigDict(
    #     env_file=".env",
    #     env_file_encoding="utf-8",
    #     extra="ignore"
    # )

class JWTSettings(BaseSettings):
    JWT_REFRESH_TOKEN_NAME: str = "refresh_token"
    JWT_SECRET_KEY: str = "test_secret_key"
    JWT_REFRESH_SECRET_KEY: str = "test_refresh_secret_key"
    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_IN_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_IN_DAYS: int = 30

    COOKIE_SECURE: bool = False
    COOKIE_SAME_SITE: Literal["lax", "strict", "none"] | None = "lax"

    def get_refresh_token_expire_in_seconds(self) -> int:
        return self.REFRESH_TOKEN_EXPIRE_IN_DAYS * 24 * 60 * 60
    #
    # model_config = SettingsConfigDict(
    #     env_file= ".env",
    #     env_file_encoding= "utf-8",
    #     extra="ignore"
    # )

settings = Settings()
jwt_settings = JWTSettings()