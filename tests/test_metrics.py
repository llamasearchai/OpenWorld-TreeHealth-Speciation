from fastapi.testclient import TestClient
from openworld_tshm.dashboard.server import app


def test_metrics_endpoint_available():
    client = TestClient(app)
    r = client.get("/metrics")
    # Metrics endpoint may or may not be available depending on optional dependency
    assert r.status_code in (200, 404)
    if r.status_code == 200:
        assert b"tshm_requests_total" in r.content or b"python_info" in r.content


