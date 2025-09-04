from __future__ import annotations
import pandas as pd


FEATURES_HEIGHT = ["age", "ndvi", "footprint", "point_count"]
FEATURES_SPECIES = ["age", "ndvi", "footprint", "point_count", "height", "crown_shape", "bark_texture"]


def build_feature_matrix(df: pd.DataFrame, target: str) -> tuple[pd.DataFrame, pd.Series]:
    if target == "height":
        X = df[FEATURES_HEIGHT]
        y = df["height"]
    elif target == "species":
        X = df[FEATURES_SPECIES]
        y = df["species"]
    else:
        raise ValueError("Unknown target")
    return X, y


