from __future__ import annotations
import numpy as np
from sklearn.cluster import DBSCAN


def segment_trees(points: np.ndarray, eps: float = 1.0, min_samples: int = 5) -> np.ndarray:
    """
    Cluster point cloud by X,Y using DBSCAN to approximate tree crowns.
    Returns labels per point, -1 is noise.
    """
    if points.shape[0] == 0:
        return np.array([])
    xy = points[:, :2]
    db = DBSCAN(eps=eps, min_samples=min_samples)
    labels = db.fit_predict(xy)
    return labels


