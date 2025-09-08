from __future__ import annotations

from typing import Optional

from openai import OpenAI
from structlog import get_logger

from ..config import get_settings

logger = get_logger()


def get_openai_client() -> Optional[OpenAI]:
    api_key = get_settings().openai_api_key
    if not api_key:
        return None
    try:
        return OpenAI(api_key=api_key)
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("failed_to_initialize_openai_client", error=str(exc))
        return None


