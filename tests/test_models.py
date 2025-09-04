import pandas as pd
from openworld_tshm.ml.train import train_all, TrainConfig
from openworld_tshm.ml.models import HeightRegressor, SpeciesClassifier


def test_model_save_and_load(tmp_path):
    out = tmp_path / "run"
    metrics = train_all(TrainConfig(seed=5, out_dir=str(out)))
    # Load back
    hr = HeightRegressor.load(str(out / "height_model.pkl"))
    sc = SpeciesClassifier.load(str(out / "species_model.pkl"))
    # Predict on minimal synthetic rows
    Xh = pd.DataFrame([{ "age": 20, "ndvi": 0.8, "footprint": 30.0, "point_count": 150 }])
    yh = hr.predict(Xh)
    assert len(yh) == 1
    Xs = pd.DataFrame([{
        "age": 20, "ndvi": 0.8, "footprint": 30.0, "point_count": 150, "height": 25.0,
        "crown_shape": 2.0, "bark_texture": 0.5
    }])
    ys = sc.predict(Xs)
    assert len(ys) == 1


