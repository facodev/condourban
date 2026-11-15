from functools import lru_cache
from typing import List

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    app_name: str = 'CondoUrban API'
    app_env: str = 'development'
    debug: bool = True
    api_prefix: str = '/api/v1'

    # Security
    secret_key: str = 'change-me-to-a-super-secret-key-min-32-chars'
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 60

    # PostgreSQL Database Connection
    database_url: str = (
        'postgresql+asyncpg://postgres:postgres@localhost:5432/condourban'
    )

    # CORS
    cors_origins: str = (
        'http://localhost:3000,http://localhost:4200,http://localhost:5173'
    )

    @computed_field
    @property
    def cors_origins_list(self) -> List[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(',')
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
