import httpx
from openworld_treehealth.app import app


async def test_species_pine():
    payload = {
        "leaf_shape": "needle",
        "bark_texture": "furrowed",
        "seed_type": "cone",
        "region": "boreal",
    }
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post("/species/classify", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["species"] == "Pinus sylvestris"
    assert 0.0 <= data["confidence"] <= 1.0


async def test_species_unknown():
    payload = {
        "leaf_shape": "broad",
        "bark_texture": "smooth",
        "seed_type": "pod",
        "region": "arid",
    }
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post("/species/classify", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "species" in data and "confidence" in data


