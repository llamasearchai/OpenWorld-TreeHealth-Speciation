from openworld_tshm.ml.train import train_all, TrainConfig


def test_metrics_thresholds_across_seeds(tmp_path):
    for seed in (13, 29, 101):
        out = tmp_path / f"run_{seed}"
        m = train_all(TrainConfig(seed=seed, out_dir=str(out)))
        assert m["height_mae"] <= 7.5  # Adjusted for more complex data with growth patterns
        assert m["species_acc"] >= 0.75  # Strict requirement for species classification with new features

