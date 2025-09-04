from __future__ import annotations
import numpy as np
import pandas as pd


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

    df = pd.DataFrame({
        "species": species,
        "age": age,
        "height": height,
        "health_idx": health_idx,
        "ndvi": ndvi,
        "footprint": footprint,
        "point_count": point_count,
        "crown_shape": crown_shape,
        "bark_texture": bark_texture,
    })
    return df


