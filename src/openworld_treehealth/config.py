from __future__ import annotations

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env",), env_file_encoding="utf-8", extra="ignore"
    )

    app_name: str = "OpenWorld Tree Health API"
    environment: str = "development"
    openai_api_key: Optional[str] = None


def get_settings() -> Settings:
    # Return a fresh Settings instance to respect environment changes at runtime/tests
    return Settings()  # type: ignore[call-arg]


