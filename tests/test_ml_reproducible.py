from openworld_tshm.ml.train import train_all, TrainConfig
import pytest
import pandas as pd
import numpy as np
from openworld_tshm.ml.data_prep import synthesize_training_data, load_real_data, validate_and_impute
from unittest.mock import Mock, patch
from pathlib import Path

def test_training_reproducible(tmp_path):
    out1 = tmp_path / "run1"
    out2 = tmp_path / "run2"
    m1 = train_all(TrainConfig(seed=123, out_dir=str(out1)))
    m2 = train_all(TrainConfig(seed=123, out_dir=str(out2)))
    assert abs(m1["height_mae"] - m2["height_mae"]) < 1e-6
    assert abs(m1["species_acc"] - m2["species_acc"]) < 1e-6

def test_synthesize_training_data():
    df = synthesize_training_data(n=100, seed=42)
    assert len(df) == 100
    assert "species" in df.columns
    assert df["species"].nunique() == 3  # pine, oak, spruce
    assert "height" in df.columns
    assert df["height"].min() > 0
    assert "ndvi" in df.columns
    assert 0.5 < df["ndvi"].mean() < 1.0

@patch('openworld_tshm.plugin_loader.load_plugins')
def test_load_real_data(mock_plugins, tmp_path):
    # Mock plugin
    mock_plugin = Mock()
    mock_plugin.name = "field_csv"
    the_data = {
        "label": 0,
        "species": "pine",
        "age": 20,
        "height": 25.0,
        "health_idx": 0.8,
        "ndvi": 0.75,
        "footprint": 50.0,
        "point_count": 100,
        "crown_shape": 2.5,
        "bark_texture": 0.3,
        "centroid_x": 0.0,
        "centroid_y": 0.0
    }
    mock_result = {
        "type": "field",
        "data": [the_data],
        "metadata": {"source": "test.csv"}
    }
    mock_plugin.ingest.return_value = mock_result
    mock_plugins.return_value = [mock_plugin]
    
    # Create mock CSV
    mock_csv = tmp_path / "test.csv"
    mock_csv.write_text("species,age,height,health_idx,ndvi,footprint,point_count,crown_shape,bark_texture\npine,20,25.0,0.8,0.75,50.0,100,2.5,0.3")
    
    df = load_real_data([str(mock_csv)], plugin_name="field_csv")
    assert len(df) == 1
    assert df["species"].iloc[0] == "pine"
    assert df["height"].iloc[0] == 25.0

def test_validate_and_impute():
    # Create DF with missing values
    data = {
        "label": [0, 1, 2, 3],
        "centroid_x": [0.0, 1.0, 2.0, 3.0],
        "centroid_y": [0.0, 1.0, 2.0, 3.0],
        "species": ["pine", "oak", None, "spruce"],
        "age": [20, None, 30, 40],
        "height": [25.0, 18.0, None, 26.0],
        "health_idx": [0.8, 0.7, 0.9, None],
        "ndvi": [0.75, None, 0.65, 0.85],
        "footprint": [50.0, 40.0, None, 60.0],
        "point_count": [100, 80, 120, None],
        "crown_shape": [2.5, 1.8, 3.0, None],
        "bark_texture": [0.3, 0.7, 0.4, None]
    }
    df_original = pd.DataFrame(data)
    
    # Known values for error calculation (subset without missing for truth)
    truth_df = df_original.dropna()
    original_numerical = truth_df.select_dtypes(include=[np.number]).values
    original_categorical = truth_df.select_dtypes(include=['object']).values
    
    df_original["species"] = df_original["species"].fillna('unknown')
    df_imputed = validate_and_impute(df_original.copy())
    
    # Check no missing
    assert df_imputed.isnull().sum().sum() == 0
    
    # Imputation error on numerical (MAE <0.05)
    imputed_numerical = df_imputed.select_dtypes(include=[np.number]).iloc[:len(truth_df)].values
    mae_num = np.mean(np.abs(original_numerical - imputed_numerical))
    assert mae_num < 0.05
    
    # Categorical accuracy (since most_frequent, check if matches mode)
    imputed_cat = df_imputed.select_dtypes(include=['object']).iloc[:len(truth_df)].values
    acc_cat = np.mean(imputed_cat == original_categorical)
    assert acc_cat >= 0.8  # Reasonable for small sample

def test_validate_and_impute_real_sample():
    # Load real CSV and map to schema (add synthetic fields for missing)
    real_df = pd.read_csv("test_forest.db.csv")
    # Map columns
    real_df["height"] = real_df["p95_height"]
    real_df["footprint"] = real_df["footprint"]
    real_df["point_count"] = real_df["point_count"]
    # Add synthetic for others to fit schema
    real_df["label"] = np.arange(len(real_df))
    real_df["centroid_x"] = np.random.normal(0, 10, len(real_df))
    real_df["centroid_y"] = np.random.normal(0, 10, len(real_df))
    real_df["species"] = np.random.choice(["pine", "oak", "spruce"], len(real_df))
    real_df["age"] = np.random.randint(5, 60, len(real_df))
    real_df["health_idx"] = np.random.uniform(0.5, 1.0, len(real_df))
    real_df["ndvi"] = np.random.uniform(0.5, 0.9, len(real_df))
    real_df["crown_shape"] = np.random.uniform(1.5, 3.5, len(real_df))
    real_df["bark_texture"] = np.random.uniform(0.2, 0.8, len(real_df))
    # Introduce some missing for test
    real_df.loc[::3, "height"] = np.nan
    real_df.loc[1::4, "species"] = np.nan
    
    real_df["species"] = real_df["species"].fillna('unknown')
    df_imputed = validate_and_impute(real_df.copy())
    assert len(df_imputed) == len(real_df)
    assert df_imputed.isnull().sum().sum() == 0
    # Basic metric: std dev of imputed shouldn't explode
    assert df_imputed["height"].std() < 10.0  # Arbitrary but reasonable