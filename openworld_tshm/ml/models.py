from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression


@dataclass
class HeightRegressor:
    model: Any

    @classmethod
    def create(cls, seed: int = 42) -> "HeightRegressor":
        # Using RandomForest for better performance on complex data
        from sklearn.ensemble import RandomForestRegressor
        return cls(model=RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=seed
        ))

    def fit(self, X, y) -> None:
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def save(self, path: str) -> None:
        joblib.dump(self.model, path)

    @classmethod
    def load(cls, path: str) -> "HeightRegressor":
        return cls(joblib.load(path))


@dataclass
class SpeciesClassifier:
    model: Any

    @classmethod
    def create(cls, seed: int = 42) -> "SpeciesClassifier":
        # Larger forest with balanced subsampling for stability across seeds
        return cls(model=RandomForestClassifier(
            n_estimators=300,
            max_depth=None,
            class_weight="balanced_subsample",
            random_state=seed,
        ))

    def fit(self, X, y) -> None:
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def save(self, path: str) -> None:
        joblib.dump(self.model, path)

    @classmethod
    def load(cls, path: str) -> "SpeciesClassifier":
        return cls(joblib.load(path))


