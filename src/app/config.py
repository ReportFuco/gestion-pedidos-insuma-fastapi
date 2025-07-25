import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.env"))

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=DOTENV_PATH,
        extra="ignore"
    )

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
