"""Configuration settings for the application"""

import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    """Settings for the application"""

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "ColbertDB"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    MANAGEMENT_API_KEY: str = os.getenv("MANAGEMENT_API_KEY")
    DEFAULT_API_KEY: str = os.getenv("DEFAULT_API_KEY")
    DATA_DIR: str = ".data"
    STORES_FILE: str = "stores.json"


settings = Settings()  # type: ignore
