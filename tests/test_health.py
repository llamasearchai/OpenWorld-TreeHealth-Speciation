import httpx
from openworld_treehealth.app import app


async def test_readiness():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/health/ready")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ready"


async def test_liveness():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/health/live")
    assert resp.status_code == 200
    assert resp.json()["status"] == "alive"


