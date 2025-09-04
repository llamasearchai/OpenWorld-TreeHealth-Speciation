from __future__ import annotations
import os
from dataclasses import asdict, dataclass
from typing import Any
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, accuracy_score
from .data_prep import synthesize_training_data
from .features import build_feature_matrix
from .models import HeightRegressor, SpeciesClassifier
from ..utils.io import ensure_dir, write_json


@dataclass
class TrainConfig:
    seed: int = 42
    out_dir: str = "artifacts/run"
    save_models: bool = True


def train_all(cfg: TrainConfig) -> dict[str, Any]:
    rng = np.random.default_rng(cfg.seed)
    _ = rng.random()  # ensure deterministic path exercised
    df = synthesize_training_data(500, seed=cfg.seed)
    # Height model
    Xh, yh = build_feature_matrix(df, target="height")
    Xh_tr, Xh_te, yh_tr, yh_te = train_test_split(Xh, yh, test_size=0.2, random_state=cfg.seed)
    hr = HeightRegressor.create(seed=cfg.seed)
    hr.fit(Xh_tr, yh_tr)
    yh_pred = hr.predict(Xh_te)
    mae = float(mean_absolute_error(yh_te, yh_pred))
    # Species model
    Xs, ys = build_feature_matrix(df, target="species")
    Xs_tr, Xs_te, ys_tr, ys_te = train_test_split(
        Xs, ys, test_size=0.2, random_state=cfg.seed, stratify=ys
    )
    sc = SpeciesClassifier.create(seed=cfg.seed)
    sc.fit(Xs_tr, ys_tr)
    ys_pred = sc.predict(Xs_te)
    acc = float(accuracy_score(ys_te, ys_pred))

    ensure_dir(cfg.out_dir)
    metrics = {"height_mae": mae, "species_acc": acc}
    if cfg.save_models:
        hr_path = os.path.join(cfg.out_dir, "height_model.pkl")
        sc_path = os.path.join(cfg.out_dir, "species_model.pkl")
        hr.save(hr_path)
        sc.save(sc_path)
        metrics["height_model_path"] = hr_path
        metrics["species_model_path"] = sc_path
    write_json(os.path.join(cfg.out_dir, "metrics.json"), metrics)
    config_full = asdict(cfg)
    try:
        config_full["height_model_params"] = getattr(hr.model, "get_params", lambda: {})()
        config_full["species_model_params"] = getattr(sc.model, "get_params", lambda: {})()
    except Exception:
        pass
    write_json(os.path.join(cfg.out_dir, "config.json"), config_full)
    return metrics

