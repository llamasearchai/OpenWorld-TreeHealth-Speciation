from __future__ import annotations
from typing import Any

try:
    import rasterio  # type: ignore
except Exception:  # pragma: no cover
    rasterio = None

from .base import SensorPlugin


class MultispectralRasterioPlugin(SensorPlugin):
    name = "multispectral_rasterio"

    def ingest(self, source: str, **kwargs: Any) -> dict:
        if rasterio is None:
            raise RuntimeError("rasterio not available")
        try:  # pragma: no cover - requires rasterio dataset
            with rasterio.open(source) as ds:  # pragma: no cover
                data = ds.read()  # (bands, rows, cols)
                transform = ds.transform
                crs = ds.crs
            return {"type": "raster", "data": data, "metadata": {"source": source, "crs": str(crs), "transform": tuple(transform)}}
        except Exception as e:  # pragma: no cover
            raise RuntimeError(str(e))


