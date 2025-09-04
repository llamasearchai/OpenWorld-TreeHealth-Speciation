from __future__ import annotations
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    data_dir: str = os.getenv("OW_TSHM_DATA_DIR", "./data")
    artifacts_dir: str = os.getenv("OW_TSHM_ARTIFACTS_DIR", "./artifacts")
    provenance_ledger: str = os.getenv("OW_TSHM_PROVENANCE_LEDGER", "./provenance/ledger.jsonl")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3")


settings = Settings()


def get_settings() -> Settings:
    # Recreate settings to pick up environment changes at runtime
    return Settings()


