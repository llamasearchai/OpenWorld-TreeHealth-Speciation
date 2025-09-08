from __future__ import annotations
from dataclasses import dataclass
from typing import Any, List
import joblib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error, accuracy_score
from xgboost import XGBRegressor, XGBClassifier, DMatrix
from ..ml.data_prep import synthesize_training_data  # For testing

@dataclass
class XGBoostHeightRegressor:
    model: Any
    n_estimators: int = 100

    @classmethod
    def create(cls, seed: int = 42) -> "XGBoostHeightRegressor":
        model = XGBRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=seed,
            n_jobs=-1
        )
        return cls(model=model)

    def fit(self, X, y) -> None:
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def uncertainty(self, X: np.ndarray, n_samples: int = 100) -> np.ndarray:
        # Approximate uncertainty as std of predictions from trees
        dmat = DMatrix(X)
        preds = []
        booster = self.model.get_booster()
        for i in range(1, self.model.n_estimators + 1):
            pred = booster.predict(dmat, iteration_range=(0, i))
            preds.append(pred)
        preds = np.array(preds)
        return np.std(preds, axis=0)

    def cross_validate(self, X, y, cv=5) -> float:
        scores = cross_val_score(self.model, X, y, cv=cv, scoring='neg_mean_absolute_error')
        return -scores.mean()

    def save(self, path: str) -> None:
        joblib.dump(self, path)

    @classmethod
    def load(cls, path: str) -> "XGBoostHeightRegressor":
        return joblib.load(path)

@dataclass
class XGBoostSpeciesClassifier:
    model: Any
    n_estimators: int = 100

    @classmethod
    def create(cls, seed: int = 42) -> "XGBoostSpeciesClassifier":
        model = XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=seed,
            n_jobs=-1,
            eval_metric='mlogloss'
        )
        return cls(model=model)

    def fit(self, X, y) -> None:
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def uncertainty(self, X: np.ndarray, n_samples: int = 100) -> np.ndarray:
        # Std of prediction probabilities
        dmat = DMatrix(X)
        probs = self.model.predict_proba(dmat)
        return np.std(probs, axis=1)

    def cross_validate(self, X, y, cv=5) -> float:
        scores = cross_val_score(self.model, X, y, cv=cv, scoring='accuracy')
        return scores.mean()

    def save(self, path: str) -> None:
        joblib.dump(self, path)

    @classmethod
    def load(cls, path: str) -> "XGBoostSpeciesClassifier":
        return joblib.load(path)

# Example usage for testing
if __name__ == "__main__":
    df = synthesize_training_data(200)
    from .features import build_feature_matrix
    Xh, yh = build_feature_matrix(df, "height")
    hr = XGBoostHeightRegressor.create()
    mae_cv = hr.cross_validate(Xh, yh)
    print(f"CV MAE: {mae_cv}")
    assert mae_cv < 5.0  # Meets threshold on synthetic

    Xs, ys = build_feature_matrix(df, "species")
    sc = XGBoostSpeciesClassifier.create()
    acc_cv = sc.cross_validate(Xs, ys)
    print(f"CV Acc: {acc_cv}")
    assert acc_cv > 0.8