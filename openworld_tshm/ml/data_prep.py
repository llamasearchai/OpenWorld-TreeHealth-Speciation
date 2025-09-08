from __future__ import annotations
import numpy as np
import pandas as pd
import os
from sklearn.impute import KNNImputer, SimpleImputer
from typing import List
from ..plugin_loader import load_plugins
from ..schemas import TreeRecord

def synthesize_training_data(n: int = 200, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    species = rng.choice(["pine", "oak", "spruce"], size=n)
    # Increase separability between species with distinct base heights
    base_height = np.array([{ "pine": 35, "oak": 18, "spruce": 26 }[s] for s in species])
    age = rng.integers(5, 60, size=n)
    health_idx = rng.uniform(0.5, 1.0, size=n) - 0.005 * (age - 30).clip(min=0)

    # Species-specific growth patterns
    growth_factor = np.array([{ "pine": 0.4, "oak": 0.25, "spruce": 0.35 }[s] for s in species])
    noise = rng.normal(0, 0.8, size=n)
    height = base_height + growth_factor * age * health_idx + noise

    # Species-specific NDVI offsets for separability
    ndvi_offset = np.array([{ "pine": 0.08, "oak": -0.05, "spruce": 0.03 }[s] for s in species])
    ndvi = health_idx + ndvi_offset + rng.normal(0, 0.02, size=n)

    # Add crown shape characteristics (pine: conical, oak: rounded, spruce: columnar)
    crown_ratio = np.array([{ "pine": 2.5, "oak": 1.8, "spruce": 3.0 }[s] for s in species])
    crown_shape = crown_ratio + rng.normal(0, 0.3, size=n)

    footprint = rng.uniform(8, 120, size=n)
    point_count = (footprint * 6 + rng.integers(0, 60, size=n)).astype(int)

    # Add bark texture indicator (roughness)
    bark_roughness = np.array([{ "pine": 0.3, "oak": 0.7, "spruce": 0.4 }[s] for s in species])
    bark_texture = bark_roughness + rng.normal(0, 0.1, size=n)

    label = np.arange(n)
    centroid_x = rng.normal(0, 10, n)
    centroid_y = rng.normal(0, 10, n)
    df = pd.DataFrame({
        "label": label,
        "species": species,
        "age": age,
        "height": height,
        "health_idx": health_idx,
        "ndvi": ndvi,
        "footprint": footprint,
        "point_count": point_count,
        "crown_shape": crown_shape,
        "bark_texture": bark_texture,
        "centroid_x": centroid_x,
        "centroid_y": centroid_y,
    })
    return df

def load_real_data(source_paths: List[str], plugin_name: str = "auto") -> pd.DataFrame:
    """
    Load real data from multiple sources using plugins.
    Combines ingested data into a single DataFrame.
    """
    plugins = load_plugins()
    if plugin_name == "auto":
        if not plugins:
            raise ValueError("No plugins available")
        plugin = plugins[0]  # Default to first plugin; in production, add logic for type detection
    else:
        plugin = next((p for p in plugins if p.name == plugin_name), None)
        if not plugin:
            raise ValueError(f"Plugin '{plugin_name}' not found")
    
    data_frames = []
    for path in source_paths:
        if not os.path.exists(path):  # Need import os
            raise FileNotFoundError(f"Source path not found: {path}")
        result = plugin.ingest(path)
        if result["type"] == "field":
            # Assume field data is list of dicts or direct DF convertible
            if isinstance(result["data"], list):
                df_part = pd.DataFrame(result["data"])
            else:
                df_part = pd.DataFrame(result["data"])
        elif result["type"] in ["pointcloud", "raster"]:
            # For pointcloud/raster, extract features (simplified; integrate with pointcloud.features)
            # Placeholder: assume metadata has aggregated features
            df_part = pd.DataFrame([result.get("metadata", {})])  # Expand as needed
        else:
            raise ValueError(f"Unsupported data type: {result['type']}")
        data_frames.append(df_part)
    
    if not data_frames:
        raise ValueError("No data loaded from sources")
    
    df = pd.concat(data_frames, ignore_index=True)
    return df

def validate_and_impute(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate DataFrame rows against TreeRecord schema and impute missing values.
    Numerical: KNNImputer, Categorical: most_frequent.
    """
    # Imputation first to handle missing values
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    if numerical_cols:
        imputer_num = KNNImputer(n_neighbors=5)
        df[numerical_cols] = imputer_num.fit_transform(df[numerical_cols])
    
    if categorical_cols:
        imputer_cat = SimpleImputer(strategy='most_frequent')
        df[categorical_cols] = imputer_cat.fit_transform(df[categorical_cols])
    
    # Validation after imputation
    for idx, row in df.iterrows():
        try:
            TreeRecord(**row.to_dict())
        except ValueError as e:
            raise ValueError(f"Validation failed for row {idx}: {e}")
    
    return df