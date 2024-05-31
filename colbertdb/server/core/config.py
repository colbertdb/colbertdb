"""Configuration settings for the application"""

import os
from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load the .env file only if it exists
if find_dotenv():
    load_dotenv()


class Settings(BaseSettings):
    """Settings for the application"""

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "ColbertDB"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    SECRET_KEY: str
    MANAGEMENT_API_KEY: str
    DEFAULT_API_KEY: str
    DATA_DIR: str = ".data"
    STORES_FILE: str = "stores.json"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()  # type: ignore
