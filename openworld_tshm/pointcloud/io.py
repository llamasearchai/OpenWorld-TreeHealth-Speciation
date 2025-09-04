from __future__ import annotations
import numpy as np


def to_xy_grid(points: np.ndarray, cell_size: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute grid indices and max Z per cell (CHM helper).
    Returns tuple (ix, iy, max_z_per_cell) where ix,iy are arrays matching input points,
    and max_z_per_cell is the z array here (used downstream).
    """
    x, y, z = points[:, 0], points[:, 1], points[:, 2]
    ix = np.floor((x - x.min()) / cell_size).astype(int)
    iy = np.floor((y - y.min()) / cell_size).astype(int)
    return ix, iy, z


