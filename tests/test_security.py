import os
import types
import pytest
from openworld_tshm.plugins.lidar_laspy import LidarLaspyPlugin
from openworld_tshm.plugins.field_csv import FieldCSVPlugin
import pandas as pd


def test_lidar_csv_size_guard(tmp_path, monkeypatch):
    p = tmp_path / "points.csv"
    p.write_text("x,y,z\n0,0,0\n1,1,1\n")
    # Pretend file is huge
    monkeypatch.setattr(os.path, "getsize", lambda _: 100 * 1024 * 1024)
    with pytest.raises(RuntimeError):
        LidarLaspyPlugin().ingest(str(p), max_mb=1)


def test_field_csv_validation_and_size(tmp_path, monkeypatch):
    p = tmp_path / "f.csv"
    pd.DataFrame({"species": ["pine"], "age": [10]}).to_csv(p, index=False)
    out = FieldCSVPlugin().ingest(str(p), max_mb=1)
    assert out["type"] == "field"
    # Missing required columns
    p2 = tmp_path / "bad.csv"
    pd.DataFrame({"foo": [1]}).to_csv(p2, index=False)
    with pytest.raises(ValueError):
        FieldCSVPlugin().ingest(str(p2))

