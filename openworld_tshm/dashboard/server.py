from __future__ import annotations
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
import numpy as np
from ..pointcloud.segmentation import segment_trees
from ..pointcloud.features import cluster_features


app = FastAPI(title="OpenWorld TSHM Dashboard")
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", response_class=HTMLResponse)
def index():
    with open(os.path.join(static_dir, "index.html"), "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/trees")
def api_trees():
    # Synthetic small demo dataset
    rng = np.random.default_rng(42)
    centers = rng.uniform(0, 100, size=(10, 2))
    points = []
    for i, c in enumerate(centers):
        for _ in range(50):
            x = c[0] + rng.normal(0, 1)
            y = c[1] + rng.normal(0, 1)
            z = 20 + 5 * rng.random() + i * 0.2
            points.append([x, y, z])
    pts = np.array(points)
    labels = segment_trees(pts, eps=2.0, min_samples=5)
    feats = cluster_features(pts, labels)
    # Map minimal GeoJSON-ish structure
    features = []
    for f in feats:
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [f["centroid_x"], f["centroid_y"]]},
            "properties": {"label": f["label"], "height": f["height"], "point_count": f["point_count"], "footprint": f["footprint"]}
        })
    return JSONResponse({"type": "FeatureCollection", "features": features})

try:
    from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST  # type: ignore
    import time

    REQUEST_COUNT = Counter("tshm_requests_total", "Total HTTP requests", ["path"])  # pragma: no cover
    TREES_DURATION = Histogram("tshm_trees_seconds", "/api/trees processing time (s)")  # pragma: no cover

    @app.middleware("http")
    async def _metrics_mw(request, call_next):  # pragma: no cover - trivial
        start = time.time()
        response = await call_next(request)
        try:
            REQUEST_COUNT.labels(path=str(request.url.path)).inc()
        except Exception:
            pass
        return response

    @app.get("/metrics")
    def metrics():
        return HTMLResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)
except Exception:  # pragma: no cover
    pass


