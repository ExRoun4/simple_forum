from pydantic_settings import BaseSettings, SettingsConfigDict

class JWTSettings(BaseSettings):
    REFRESH_TOKEN_NAME: str = "refresh_token"
    SECRET_KEY: str = "test_secret_key"
    REFRESH_SECRET_KEY: str = "test_refresh_secret_key"
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_IN_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_IN_DAYS: int = 30

    def get_refresh_token_expire_in_seconds(self) -> int:
        return self.REFRESH_TOKEN_EXPIRE_IN_DAYS * 24 * 60 * 60

    model_config = SettingsConfigDict(
        env_file= ".env",
        env_file_encoding= "utf-8",
        env_prefix="JWT_",
        extra="ignore"
    )

jwt_settings = JWTSettings()