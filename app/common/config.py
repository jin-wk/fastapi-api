from pydantic import BaseSettings
from functools import lru_cache


class Config(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    APP_ENV: str
    LOG_LEVEL: str

    DB_USERNAME: str
    DB_PASSWORD: str
    DB_DATABASE: str
    DB_HOST: str
    DB_PORT: str

    JWT_SECRET: str
    JWT_EXPIRES_MIN: int

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_config():
    return Config()
