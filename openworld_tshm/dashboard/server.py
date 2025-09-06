from __future__ import annotations
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
import uuid
import numpy as np
from ..pointcloud.segmentation import segment_trees
from ..pointcloud.features import cluster_features


app = FastAPI(title="OpenWorld TSHM Dashboard")
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Optional CORS support controlled by env var DASHBOARD_CORS_ORIGINS (comma-separated)
_cors = os.getenv("DASHBOARD_CORS_ORIGINS")
if _cors:
    origins = [o.strip() for o in _cors.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )


class _RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):  # type: ignore[override]
        rid = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        response = await call_next(request)
        response.headers["X-Request-ID"] = rid
        return response


class _SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):  # type: ignore[override]
        response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        # Simple CSP suitable for static content and JSON endpoints
        response.headers.setdefault("Content-Security-Policy", "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self'")
        return response


app.add_middleware(_RequestIDMiddleware)
app.add_middleware(_SecurityHeadersMiddleware)


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
