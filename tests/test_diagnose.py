from __future__ import annotations

from typing import Any

import pytest
import httpx
from openworld_treehealth.app import app


@pytest.mark.asyncio
async def test_diagnose_without_openai(monkeypatch: pytest.MonkeyPatch):
    # Force client factory to return None
    monkeypatch.setenv("OPENAI_API_KEY", "")

    payload = {"description": "Leaves yellowing with spots", "location": "park"}
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post("/diagnose/", json=payload)
    assert resp.status_code == 503


class DummyResponse:
    def __init__(self, text: str):
        self.output_text = text


class DummyClient:
    class Responses:
        @staticmethod
        def create(**_: Any) -> DummyResponse:  # noqa: ANN401
            return DummyResponse("Likely nutrient deficiency; check soil and watering.")

    responses = Responses()


@pytest.mark.asyncio
async def test_diagnose_with_openai(monkeypatch: pytest.MonkeyPatch):
    from openworld_treehealth import services

    # Patch the client factory to return our dummy client
    def fake_client():
        return DummyClient()

    monkeypatch.setenv("OPENAI_API_KEY", "test")
    monkeypatch.setattr(
        "openworld_treehealth.services.openai_client.get_openai_client", fake_client
    )

    payload = {"description": "Bark peeling rapidly after frost", "location": "backyard"}
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post("/diagnose/", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "diagnosis" in data and "safety_note" in data
    assert "nutrient" in data["diagnosis"].lower() or len(data["diagnosis"]) > 0


