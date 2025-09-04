from __future__ import annotations
from typing import Tuple
import math
import numpy as np


def bbox(points: np.ndarray) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
    """
    Compute axis-aligned 3D bounding box. points shape (N,3)
    Returns (minx,miny,minz), (maxx,maxy,maxz)
    """
    if points.size == 0:
        raise ValueError("Empty point array")
    mins = points.min(axis=0)
    maxs = points.max(axis=0)
    return (mins[0], mins[1], mins[2]), (maxs[0], maxs[1], maxs[2])


def bbox_volume(points: np.ndarray) -> float:
    lo, hi = bbox(points)
    return max(hi[0] - lo[0], 0.0) * max(hi[1] - lo[1], 0.0) * max(hi[2] - lo[2], 0.0)


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371000.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = phi2 - phi1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dl/2)**2
    return 2 * R * math.asin(math.sqrt(a))


def height_from_points(points: np.ndarray) -> float:
    """
    Estimate tree height as max Z minus 5th percentile Z (ground approx).
    """
    z = points[:, 2]
    ground = float(np.percentile(z, 5))
    return float(z.max() - ground)


