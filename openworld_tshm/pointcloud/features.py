from __future__ import annotations
import numpy as np
from ..utils.geometry import height_from_points
try:
    from shapely.geometry import MultiPoint  # type: ignore
except Exception:  # pragma: no cover
    MultiPoint = None  # type: ignore


def cluster_features(points: np.ndarray, labels: np.ndarray) -> list[dict]:
    """
    Compute simple features per cluster: height, point_count, footprint area approx.
    """
    feats: list[dict] = []
    for lab in set(labels):
        if lab == -1:
            continue
        mask = labels == lab
        pts = points[mask]
        if pts.shape[0] < 3:
            continue
        height = height_from_points(pts)
        # Enriched height statistics
        p95 = float(np.percentile(pts[:, 2], 95))
        p50 = float(np.percentile(pts[:, 2], 50))
        # Footprint via convex hull area if available
        spread_x = float(pts[:, 0].max() - pts[:, 0].min())
        spread_y = float(pts[:, 1].max() - pts[:, 1].min())
        bbox_area = spread_x * spread_y
        crown_area = bbox_area
        if MultiPoint is not None:  # pragma: no cover - optional heavy dep
            try:
                hull = MultiPoint(pts[:, :2]).convex_hull  # type: ignore
                crown_area = float(hull.area) if hasattr(hull, "area") else bbox_area
            except Exception:
                crown_area = bbox_area
        density = float(pts.shape[0] / crown_area) if crown_area > 0 else float("inf")
        rec = {
            "label": int(lab),
            "height": float(height),
            "point_count": int(pts.shape[0]),
            "footprint": float(crown_area),
            "p95_height": p95,
            "p50_height": p50,
            "density": density,
            "centroid_x": float(pts[:, 0].mean()),
            "centroid_y": float(pts[:, 1].mean()),
        }
        feats.append(rec)
    return feats

