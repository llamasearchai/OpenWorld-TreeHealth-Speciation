from openworld_tshm.ml.train import train_all, TrainConfig


def test_training_reproducible(tmp_path):
    out1 = tmp_path / "run1"
    out2 = tmp_path / "run2"
    m1 = train_all(TrainConfig(seed=123, out_dir=str(out1)))
    m2 = train_all(TrainConfig(seed=123, out_dir=str(out2)))
    assert abs(m1["height_mae"] - m2["height_mae"]) < 1e-6
    assert abs(m1["species_acc"] - m2["species_acc"]) < 1e-6


