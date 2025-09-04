import os
from typer.testing import CliRunner
from openworld_tshm.cli import app


runner = CliRunner()


def test_cli_ingest_lidar_csv(tmp_path):
    csv = tmp_path / "pts.csv"
    csv.write_text("x,y,z\n0,0,0\n1,1,1\n")
    res = runner.invoke(app, ["ingest", "--plugin", "lidar_laspy", str(csv)])
    assert res.exit_code == 0
    assert "pointcloud" in res.stdout


def test_cli_export_sqlite(tmp_path, monkeypatch):
    # generate demo feats in tmp artifacts dir
    monkeypatch.setenv("OW_TSHM_ARTIFACTS_DIR", str(tmp_path))
    res = runner.invoke(app, ["process-demo", "1.2", "4"])
    assert res.exit_code == 0
    res = runner.invoke(app, ["export-sqlite", str(tmp_path / "forest.db")])
    assert res.exit_code == 0


