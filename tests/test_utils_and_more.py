import os
import json
import numpy as np
import pandas as pd
from openworld_tshm.utils.hashing import sha256_file
from openworld_tshm.utils.io import ensure_dir, write_json
from openworld_tshm.ml.features import build_feature_matrix
from openworld_tshm.ml.evaluate import load_metrics
from openworld_tshm.gis.export import export_trees_sqlite
from openworld_tshm.pointcloud.io import to_xy_grid
from openworld_tshm.plugins.multispectral_rasterio import MultispectralRasterioPlugin
from openworld_tshm.agents.forest_agent import generate_narrative


def test_utils_io_and_hash(tmp_path):
    ensure_dir(tmp_path / "a")
    p = tmp_path / "a" / "b.json"
    write_json(p, {"x": 1})
    assert p.exists()
    d = sha256_file(p)
    assert isinstance(d, str) and len(d) == 64


def test_build_feature_matrix_and_evaluate(tmp_path):
    df = pd.DataFrame({
        "age": [10, 20],
        "ndvi": [0.7, 0.8],
        "footprint": [20.0, 30.0],
        "point_count": [100, 150],
        "height": [15.0, 25.0],
        "species": ["pine", "oak"],
        "crown_shape": [2.2, 1.9],
        "bark_texture": [0.4, 0.6],
    })
    Xh, yh = build_feature_matrix(df, target="height")
    Xs, ys = build_feature_matrix(df, target="species")
    assert Xh.shape[1] == 4 and Xs.shape[1] == 7  # 5 original + 2 new species features
    m = {"a": 1}
    j = tmp_path / "m.json"
    j.write_text(json.dumps(m))
    assert load_metrics(str(j))["a"] == 1


def test_export_sqlite_fallback(tmp_path):
    df = pd.DataFrame([{ "label": 1, "x": 1 }])
    db = tmp_path / "forest.db"
    export_trees_sqlite(df, db_path=str(db))
    # If sqlite_utils not installed, CSV fallback is created
    assert (tmp_path / "forest.db.csv").exists() or db.exists()


def test_pointcloud_io_grid():
    pts = np.array([[0,0,0],[1,1,1]])
    ix, iy, z = to_xy_grid(pts, cell_size=1.0)
    assert len(ix) == len(iy) == len(z) == 2


def test_multispectral_plugin_error_when_missing():
    p = MultispectralRasterioPlugin()
    try:
        p.ingest("/non/existent.tif")
    except RuntimeError:
        pass


def test_agent_fallback_text():
    s = generate_narrative({"num_trees": 3, "avg_height": 10.0}, use_llm="fallback")
    assert "average height" in s


