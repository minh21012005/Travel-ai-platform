from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Travel AI Platform"
    app_env: str = "dev"
    log_level: str = "INFO"

    google_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    request_timeout: int = 30
    
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()
