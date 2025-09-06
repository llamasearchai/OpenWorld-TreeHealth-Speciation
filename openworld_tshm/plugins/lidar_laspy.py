from __future__ import annotations
import os
import numpy as np
from typing import Any

try:
    import laspy  # type: ignore
except Exception:  # pragma: no cover
    laspy = None

from .base import SensorPlugin


class LidarLaspyPlugin(SensorPlugin):
    name = "lidar_laspy"

    def ingest(self, source: str, **kwargs: Any) -> dict:
        """
        Returns dict with:
        - type: 'pointcloud'
        - data: np.ndarray (N,3)
        - metadata: dict
        """
        # Allowlist extensions (.las, .laz, .csv [fallback])
        src_lower = str(source).lower()
        allowed = (src_lower.endswith(".las"), src_lower.endswith(".laz"), src_lower.endswith(".csv"))
        if not any(allowed):
            raise ValueError("LidarLaspyPlugin accepts only .las, .laz, or .csv (fallback) files")
        # Basic size guard (50MB default)
        max_mb = float(kwargs.get("max_mb", os.environ.get("OW_TSHM_MAX_CSV_MB", 50)))
        try:
            sz_mb = (os.path.getsize(source) / (1024 * 1024))
        except OSError:
            sz_mb = 0.0
        if sz_mb > max_mb:
            raise RuntimeError(f"Input file too large: {sz_mb:.1f}MB > {max_mb}MB")
        if laspy is None:
            # Fallback: interpret CSV with x,y,z header
            pts = np.loadtxt(source, delimiter=",", skiprows=1)
            return {"type": "pointcloud", "data": pts[:, :3], "metadata": {"source": source, "format": "csv"}}
        with laspy.open(source) as f:  # pragma: no cover - exercised only when laspy available
            las = f.read()  # pragma: no cover
            x = las.x  # pragma: no cover
            y = las.y  # pragma: no cover
            z = las.z  # pragma: no cover
        pts = np.vstack([x, y, z]).T.astype(float)  # pragma: no cover
        return {"type": "pointcloud", "data": pts, "metadata": {"source": source, "format": "las"}}  # pragma: no cover
