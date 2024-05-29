"""Configuration settings for the application"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the application"""

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "ColbertDB"
    ALGORITHM: str = "HS256"
    SECRET_KEY: str
    MANAGEMENT_API_KEY: str


settings = Settings()  # type: ignore
