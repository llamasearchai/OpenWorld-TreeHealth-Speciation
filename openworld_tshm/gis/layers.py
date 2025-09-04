from __future__ import annotations
import json
import pandas as pd

try:  # pragma: no cover - optional heavy deps
    import geopandas as gpd  # type: ignore
    from shapely.geometry import Point  # type: ignore
except Exception:  # pragma: no cover
    gpd = None  # type: ignore
    Point = None  # type: ignore


def trees_geodataframe(records: list[dict]):
    if gpd is None or Point is None:
        # Lightweight fallback: return pandas DataFrame when heavy deps missing
        return pd.DataFrame(records)
    df = pd.DataFrame(records)
    geometry = [Point(xy) for xy in zip(df["centroid_x"], df["centroid_y"]) ]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:3857")
    return gdf


def to_geojson(gdf_or_df) -> dict:
    if gpd is None or not hasattr(gdf_or_df, "to_json"):
        # Manual minimal GeoJSON for pandas DataFrame
        features: list[dict] = []
        for _, r in gdf_or_df.iterrows():
            features.append({
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [float(r["centroid_x"]), float(r["centroid_y"])]},
                "properties": {k: (None if k in {"centroid_x", "centroid_y"} else r[k]) for k in gdf_or_df.columns},
            })
        return {"type": "FeatureCollection", "features": features}
    return json.loads(gdf_or_df.to_json())


