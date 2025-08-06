from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from dotenv import load_dotenv
import os


load_dotenv()


ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

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

#Hola