import numpy as np
from openworld_tshm.plugins.lidar_laspy import LidarLaspyPlugin


def test_lidar_csv_ingest_fallback(tmp_path):
    p = tmp_path / "points.csv"
    with open(p, "w", encoding="utf-8") as f:
        f.write("x,y,z\n0,0,0\n1,2,3\n")
    plugin = LidarLaspyPlugin()
    out = plugin.ingest(str(p))
    assert out["type"] == "pointcloud"
    assert out["data"].shape == (2,3)


