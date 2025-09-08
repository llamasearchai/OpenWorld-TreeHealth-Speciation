from __future__ import annotations

from fastapi import FastAPI
from structlog import get_logger

from .config import get_settings
from .routers import health, species, diagnose

logger = get_logger()


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(title=settings.app_name)

    application.include_router(health.router)
    application.include_router(species.router)
    application.include_router(diagnose.router)

    return application


app = create_app()


