import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    path = os.path.join(os.path.dirname(__file__), 'env.env')
    load_dotenv(path)
    DB_DSN: PostgresDsn = os.getenv('DATABASE_URL')

    CORS_ALLOW_ORIGINS: list[str] = ['*']
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ['*']
    CORS_ALLOW_HEADERS: list[str] = ['*']

    class Config:
        """Pydantic BaseSettings config"""

        case_sensitive = True
        env_file = "env.env"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
