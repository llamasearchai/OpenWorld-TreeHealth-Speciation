"""Integration tests for CLI workflows."""
import os
import json
import tempfile
import pandas as pd
from typer.testing import CliRunner
from openworld_tshm.cli import app


runner = CliRunner()


def test_end_to_end_demo_workflow(tmp_path):
    """Test the complete demo workflow: process -> export -> report."""
    # Set up environment
    artifacts_dir = tmp_path / "artifacts"
    os.environ["OW_TSHM_ARTIFACTS_DIR"] = str(artifacts_dir)

    # Step 1: Process demo data
    result = runner.invoke(app, ["process-demo", "2.0", "5"])
    assert result.exit_code == 0
    assert "Clusters:" in result.stdout

    # Verify artifacts were created
    assert (artifacts_dir / "feats.json").exists()

    # Step 2: Export to SQLite
    db_path = tmp_path / "test_forest.db"
    result = runner.invoke(app, ["export-sqlite", str(db_path)])
    assert result.exit_code == 0
    assert "Exported" in result.stdout

    # Verify database or CSV fallback was created
    assert db_path.exists() or (db_path.parent / f"{db_path.name}.csv").exists()

    # Step 3: Generate report
    report_path = tmp_path / "test_report.html"
    result = runner.invoke(app, ["report", str(report_path), "fallback"])
    assert result.exit_code == 0
    assert "Report written" in result.stdout

    # Verify report was created
    assert report_path.exists()
    with open(report_path, "r") as f:
        content = f.read()
        assert "OpenWorld TSHM" in content


def test_ingestion_workflow(tmp_path):
    """Test data ingestion workflow."""
    # Create test CSV
    csv_path = tmp_path / "test_data.csv"
    test_data = """species,height,age,health_idx
pine,25.5,20,0.85
oak,18.2,15,0.78
spruce,22.1,18,0.92"""
    csv_path.write_text(test_data)

    # Test ingestion
    result = runner.invoke(app, ["ingest", "--plugin", "field_csv", str(csv_path)])
    assert result.exit_code == 0
    assert "field" in result.stdout
    assert "test_data.csv" in result.stdout


def test_cli_error_handling():
    """Test CLI error handling."""
    # Test missing file
    result = runner.invoke(app, ["ingest", "--plugin", "field_csv", "/nonexistent/file.csv"])
    assert result.exit_code != 0

    # Test invalid plugin
    result = runner.invoke(app, ["ingest", "--plugin", "nonexistent_plugin", "/tmp/test.csv"])
    assert result.exit_code != 0

    # Test invalid process-demo args
    result = runner.invoke(app, ["process-demo", "--eps", "-1", "--min-samples", "0"])
    assert result.exit_code != 0
