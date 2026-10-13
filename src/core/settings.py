from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    HOST: str = "localhost"
    PORT: int = 8000

    POSTGRES_DB_USER: str = "user"
    POSTGRES_DB_PASSWORD: str = "password"
    POSTGRES_DB_NAME: str = "forum_data"
    POSTGRES_DB_HOST: str = "localhost"
    POSTGRES_DB_PORT: int = 5432

    REDIS_NAME: str = "forum_data"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
