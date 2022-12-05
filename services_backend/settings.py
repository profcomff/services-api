import os
from dotenv import load_dotenv

from pydantic import BaseSettings, PostgresDsn
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    DB_DSN: PostgresDsn = os.getenv('DATABASE_URL')

    CORS_ALLOW_ORIGINS: list[str] = ['*']
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ['*']
    CORS_ALLOW_HEADERS: list[str] = ['*']

    class Config:
        """Pydantic BaseSettings config"""

        case_sensitive = True
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
