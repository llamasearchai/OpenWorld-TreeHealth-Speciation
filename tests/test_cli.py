import json
import os
import tempfile
from typer.testing import CliRunner
from openworld_tshm.cli import app


runner = CliRunner()


def test_cli_list_plugins():
    result = runner.invoke(app, ["list-plugins"])
    assert result.exit_code == 0
    assert "lidar_laspy" in result.stdout


def test_cli_process_demo_and_report(tmp_path, monkeypatch):
    monkeypatch.setenv("OW_TSHM_ARTIFACTS_DIR", str(tmp_path))
    # process demo
    result = runner.invoke(app, ["process-demo", "1.5", "5"])  # forces generation
    assert result.exit_code == 0
    feats_path = tmp_path / "feats.json"
    assert feats_path.exists()
    # report with stub to avoid network
    out = tmp_path / "r.html"
    result = runner.invoke(app, ["report", str(out), "fallback"])
    assert result.exit_code == 0
    assert out.exists()


def test_cli_train_repro(tmp_path):
    out_dir = tmp_path / "run"
    result = runner.invoke(app, ["train", "--seed", "7", "--out-dir", str(out_dir)])
    assert result.exit_code == 0
    assert (out_dir / "metrics.json").exists()


