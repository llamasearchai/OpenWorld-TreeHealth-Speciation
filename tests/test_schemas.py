from openworld_tshm.schemas import TreeRecord, Metrics, ProvenanceRecordModel


def test_tree_record_validation():
    r = TreeRecord(label=1, height=10.5, point_count=50, footprint=12.3, centroid_x=0.0, centroid_y=1.0)
    assert r.label == 1 and r.footprint > 0


def test_metrics_validation():
    m = Metrics(num_trees=5, avg_height=12.0, species_breakdown={"pine": 0.5}, health_index_avg=0.8)
    assert m.num_trees == 5


def test_provenance_model_optional_env():
    p = ProvenanceRecordModel(timestamp=0.0, actor="a", host="h", step="s", params={}, inputs=[], outputs=[], code_version=None, digest="d")
    assert p.env is None

import pytest
from pydantic import ValidationError
from openworld_tshm.schemas import TreeRecord, Metrics


def test_tree_record_validation():
    r = TreeRecord(label=1, height=10.0, point_count=5, footprint=2.0, centroid_x=0.0, centroid_y=0.0)
    assert r.height == 10.0
    with pytest.raises(ValidationError):
        TreeRecord(label=-1, height=-1.0, point_count=0, footprint=-2.0, centroid_x=0.0, centroid_y=0.0)


def test_metrics_validation():
    m = Metrics(num_trees=2, avg_height=12.3, species_breakdown={"pine": 1}, health_index_avg=0.8)
    assert m.num_trees == 2

