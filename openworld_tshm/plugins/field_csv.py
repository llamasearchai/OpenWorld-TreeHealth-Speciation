from __future__ import annotations
import os
import pandas as pd
from typing import Any
from .base import SensorPlugin


class FieldCSVPlugin(SensorPlugin):
    name = "field_csv"

    def ingest(self, source: str, **kwargs: Any) -> dict:
        # Extension allowlist
        if not str(source).lower().endswith(".csv"):
            raise ValueError("FieldCSVPlugin accepts only .csv files")
        # Size guard (50MB default)
        max_mb = float(kwargs.get("max_mb", os.environ.get("OW_TSHM_MAX_CSV_MB", 50)))
        try:
            sz_mb = (os.path.getsize(source) / (1024 * 1024))
            if sz_mb > max_mb:
                raise RuntimeError(f"Input file too large: {sz_mb:.1f}MB > {max_mb}MB")
        except Exception:
            pass
        df = pd.read_csv(source)
        # Basic validation
        required_any = [{"species", "height"}, {"species", "age"}]
        if not any(req.issubset(df.columns) for req in required_any):
            raise ValueError("Field CSV must contain columns including 'species' and one of 'height' or 'age'")
        return {"type": "field", "data": df, "metadata": {"source": source}}
