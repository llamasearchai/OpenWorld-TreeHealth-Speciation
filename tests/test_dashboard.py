from fastapi.testclient import TestClient
from openworld_tshm.dashboard.server import app


def test_dashboard_health_and_trees():
    client = TestClient(app)
    r = client.get("/api/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"
    r = client.post("/api/trees")
    assert r.status_code == 200
    data = r.json()
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) > 0


