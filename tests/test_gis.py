from openworld_tshm.gis.layers import trees_geodataframe, to_geojson
from openworld_tshm.gis.export import export_trees_sqlite
import pandas as pd


def test_gis_fallbacks():
    records = [{"label": 1, "centroid_x": 0.0, "centroid_y": 1.0, "height": 10.0}]
    g = trees_geodataframe(records)
    gj = to_geojson(g)
    assert gj["type"] == "FeatureCollection"
    assert gj["features"][0]["geometry"]["type"] == "Point"


def test_export_sqlite_and_csv(tmp_path):
    df = pd.DataFrame([{ "label": 1, "x": 1 }])
    db = tmp_path / "forest.db"
    export_trees_sqlite(df, db_path=str(db))
    # One of the two should exist depending on sqlite_utils availability
    assert db.exists() or (tmp_path / "forest.db.csv").exists()


