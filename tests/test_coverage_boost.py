"""Additional tests to boost coverage to 95%."""
import json
import numpy as np
from openworld_tshm.utils.geometry import height_from_points
from openworld_tshm.pointcloud.chm import compute_chm
from openworld_tshm.pointcloud.segmentation import segment_trees


def test_height_from_points_edge_cases():
    """Test edge cases for height_from_points."""
    # Single point
    pts = np.array([[0, 0, 10]])
    h = height_from_points(pts)
    assert h == 0.0  # No variation, should be 0

    # All same height
    pts = np.array([[0, 0, 5], [1, 1, 5], [2, 2, 5]])
    h = height_from_points(pts)
    assert h == 0.0


def test_compute_chm_edge_cases():
    """Test edge cases for CHM computation."""
    # Single point
    pts = np.array([[0, 0, 10]])
    chm, xmin, ymin, csx, csy = compute_chm(pts)
    assert chm.size == 1
    assert chm[0, 0] == 0.0  # Single point should have 0 height


def test_segment_trees_edge_cases():
    """Test edge cases for tree segmentation."""
    # Single point with min_samples=1 becomes a cluster
    pts = np.array([[0, 0, 10]])
    labels = segment_trees(pts, eps=1.0, min_samples=1)
    assert len(labels) == 1
    assert labels[0] == 0  # Single point with min_samples=1 becomes cluster 0

    # Single point with min_samples=2 becomes noise
    labels = segment_trees(pts, eps=1.0, min_samples=2)
    assert len(labels) == 1
    assert labels[0] == -1  # Single point with min_samples=2 becomes noise

    # Two close points
    pts = np.array([[0, 0, 10], [0.1, 0.1, 11]])
    labels = segment_trees(pts, eps=1.0, min_samples=1)
    assert len(labels) == 2
    assert labels[0] != -1  # Should form a cluster


def test_json_serialization_coverage():
    """Test JSON serialization coverage."""
    # Test provenance record serialization
    from openworld_tshm.provenance import ProvenanceStore
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmp:
        ps = ProvenanceStore(os.path.join(tmp, "test.jsonl"))
        rec = ps.log("test", {"param": 1}, ["input.txt"], ["output.txt"])

        # Check that JSON was written
        ledger_file = os.path.join(tmp, "test.jsonl")
        assert os.path.exists(ledger_file)

        with open(ledger_file, "r") as f:
            line = f.readline()
            data = json.loads(line)
            assert "env" in data
            assert "python" in data["env"]


def test_multispectral_plugin_fallback():
    """Test multispectral plugin fallback behavior."""
    from openworld_tshm.plugins.multispectral_rasterio import MultispectralRasterioPlugin

    plugin = MultispectralRasterioPlugin()
    try:
        plugin.ingest("/nonexistent.tif")
        assert False, "Should have raised RuntimeError"
    except RuntimeError as e:
        assert "rasterio not available" in str(e) or "No such file" in str(e)


def test_field_csv_plugin_validation():
    """Test field CSV plugin validation."""
    import tempfile
    import os
    from openworld_tshm.plugins.field_csv import FieldCSVPlugin

    plugin = FieldCSVPlugin()

    # Test missing required columns
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("invalid_col,value\n1,2\n")
        f.flush()

        try:
            plugin.ingest(f.name)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "species" in str(e)
        finally:
            os.unlink(f.name)
