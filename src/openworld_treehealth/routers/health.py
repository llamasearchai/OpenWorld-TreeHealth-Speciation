from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/ready")
async def readiness() -> dict[str, str]:
    return {"status": "ready"}


@router.get("/live")
async def liveness() -> dict[str, str]:
    return {"status": "alive"}


