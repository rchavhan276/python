from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from .constant import (
    DATABASE_URL,
    UUID_URL,
    UUID_BATCH_URL,
    UUID_NAMESPACE_BASE_URL,
    API_PREFIX
    )

class Settings(BaseSettings):
    DATABASE_URL: str
    UUID_URL: str
    UUID_BATCH_URL: str
    UUID_NAMESPACE_BASE_URL: str
    API_PREFIX: str
    model_config = ConfigDict(env_file = ".env")
    

settings = Settings()