import numpy as np
from openworld_tshm.utils.geometry import bbox, bbox_volume, haversine, height_from_points


def test_bbox_volume():
    pts = np.array([[0,0,0],[1,1,1]])
    assert bbox_volume(pts) == 1.0


def test_haversine_symmetry():
    assert abs(haversine(0,0,0,1) - haversine(0,1,0,0)) < 1e-6


def test_height_from_points_ground_robust():
    z = np.array([0,0.1,0.2,10.0,9.0])
    pts = np.stack([np.zeros_like(z), np.zeros_like(z), z], axis=1)
    h = height_from_points(pts)
    assert 9.5 <= h <= 10.0


