import numpy as np
from openworld_tshm.pointcloud.chm import compute_chm


def test_compute_chm_not_empty():
    pts = np.array([[0,0,0],[0.4,0.4,1.0],[1.2,0.1,2.0]])
    chm, xmin, ymin, csx, csy = compute_chm(pts, cell_size=1.0)
    assert chm.shape[0] >= 1 and chm.shape[1] >= 1
    assert csx == 1.0 and csy == 1.0


