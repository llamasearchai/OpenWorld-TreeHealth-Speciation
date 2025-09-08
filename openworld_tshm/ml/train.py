from __future__ import annotations
import os
from dataclasses import asdict, dataclass
from typing import Any
import numpy as np
import matplotlib.pyplot as plt
import mlflow
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, accuracy_score
from .data_prep import synthesize_training_data, load_real_data, validate_and_impute
from .features import build_feature_matrix
from .models import HeightRegressor, SpeciesClassifier
from .models_advanced import XGBoostHeightRegressor, XGBoostSpeciesClassifier
from ..utils.io import ensure_dir, write_json

@dataclass
class TrainConfig:
    seed: int = 42
    out_dir: str = "artifacts/run"
    save_models: bool = True
    model_type: str = "basic"  # 'basic' or 'advanced'
    mlflow_experiment: str = None

def train_all(cfg: TrainConfig) -> dict[str, Any]:
    if cfg.mlflow_experiment:
        mlflow.set_experiment(cfg.mlflow_experiment)
        with mlflow.start_run(run_name=f"run_{cfg.seed}"):
            mlflow.log_params(asdict(cfg))
    
    rng = np.random.default_rng(cfg.seed)
    _ = rng.random()  # ensure deterministic path exercised
    # Use real data if possible, fallback to synthetic
    try:
        df = load_real_data(["test_forest.db.csv"], plugin_name="field_csv")
        df = validate_and_impute(df)
    except:
        df = synthesize_training_data(500, seed=cfg.seed)
    # Height model
    Xh, yh = build_feature_matrix(df, target="height")
    Xh_tr, Xh_te, yh_tr, yh_te = train_test_split(Xh, yh, test_size=0.2, random_state=cfg.seed)
    if cfg.model_type == "advanced":
        hr = XGBoostHeightRegressor.create(seed=cfg.seed)
        hr.fit(Xh_tr, yh_tr)
        yh_pred = hr.predict(Xh_te)
        mae = float(mean_absolute_error(yh_te, yh_pred))
        cv_mae = hr.cross_validate(Xh, yh)
        uncertainty_h = hr.uncertainty(Xh_te)
        metrics_h = {"height_mae": mae, "height_cv_mae": cv_mae, "height_uncertainty_mean": float(np.mean(uncertainty_h))}
        if cfg.mlflow_experiment:
            mlflow.log_metric("height_mae", mae)
            mlflow.log_metric("height_cv_mae", cv_mae)
            mlflow.log_metric("height_uncertainty_mean", np.mean(uncertainty_h))
            mlflow.log_artifact(os.path.join(cfg.out_dir, "uncertainty_height.png"))
    else:
        hr = HeightRegressor.create(seed=cfg.seed)
        hr.fit(Xh_tr, yh_tr)
        yh_pred = hr.predict(Xh_te)
        mae = float(mean_absolute_error(yh_te, yh_pred))
        metrics_h = {"height_mae": mae}
        if cfg.mlflow_experiment:
            mlflow.log_metric("height_mae", mae)
    # Species model
    Xs, ys = build_feature_matrix(df, target="species")
    Xs_tr, Xs_te, ys_tr, ys_te = train_test_split(
        Xs, ys, test_size=0.2, random_state=cfg.seed, stratify=ys
    )
    if cfg.model_type == "advanced":
        sc = XGBoostSpeciesClassifier.create(seed=cfg.seed)
        sc.fit(Xs_tr, ys_tr)
        ys_pred = sc.predict(Xs_te)
        acc = float(accuracy_score(ys_te, ys_pred))
        cv_acc = sc.cross_validate(Xs, ys)
        uncertainty_s = sc.uncertainty(Xs_te)
        # Plot uncertainties after both models trained
        plt.figure()
        plt.hist(uncertainty_h, bins=20)
        plt.title("Height Prediction Uncertainty")
        plt.savefig(os.path.join(cfg.out_dir, "uncertainty_height.png"))
        plt.close()
        plt.figure()
        plt.hist(uncertainty_s, bins=20)
        plt.title("Species Prediction Uncertainty")
        plt.savefig(os.path.join(cfg.out_dir, "uncertainty_species.png"))
        plt.close()
        metrics_s = {"species_acc": acc, "species_cv_acc": cv_acc, "species_uncertainty_mean": float(np.mean(uncertainty_s))}
        if cfg.mlflow_experiment:
            mlflow.log_metric("species_acc", acc)
            mlflow.log_metric("species_cv_acc", cv_acc)
            mlflow.log_metric("species_uncertainty_mean", np.mean(uncertainty_s))
            mlflow.log_artifact(os.path.join(cfg.out_dir, "uncertainty_species.png"))
    else:
        sc = SpeciesClassifier.create(seed=cfg.seed)
        sc.fit(Xs_tr, ys_tr)
        ys_pred = sc.predict(Xs_te)
        acc = float(accuracy_score(ys_te, ys_pred))
        metrics_s = {"species_acc": acc}
        if cfg.mlflow_experiment:
            mlflow.log_metric("species_acc", acc)
    
    ensure_dir(cfg.out_dir)
    metrics = {**metrics_h, **metrics_s}
    metrics["model_type"] = cfg.model_type
    if cfg.mlflow_experiment:
        mlflow.log_metrics(metrics)
    if cfg.save_models:
        hr_path = os.path.join(cfg.out_dir, "height_model.pkl")
        sc_path = os.path.join(cfg.out_dir, "species_model.pkl")
        hr.save(hr_path)
        sc.save(sc_path)
        metrics["height_model_path"] = hr_path
        metrics["species_model_path"] = sc_path
        if cfg.mlflow_experiment:
            mlflow.log_artifact(hr_path)
            mlflow.log_artifact(sc_path)
    write_json(os.path.join(cfg.out_dir, "metrics.json"), metrics)
    config_full = asdict(cfg)
    try:
        if cfg.model_type == "advanced":
            config_full["height_model_params"] = hr.model.get_params()
            config_full["species_model_params"] = sc.model.get_params()
        else:
            config_full["height_model_params"] = getattr(hr.model, "get_params", lambda: {})()
            config_full["species_model_params"] = getattr(sc.model, "get_params", lambda: {})()
    except Exception:
        pass
    write_json(os.path.join(cfg.out_dir, "config.json"), config_full)
    if cfg.mlflow_experiment:
        mlflow.log_artifact(os.path.join(cfg.out_dir, "metrics.json"))
        mlflow.log_artifact(os.path.join(cfg.out_dir, "config.json"))
    return metrics