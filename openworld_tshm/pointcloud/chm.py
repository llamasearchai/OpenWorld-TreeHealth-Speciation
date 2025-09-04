from __future__ import annotations
import numpy as np


def compute_chm(points: np.ndarray, cell_size: float = 1.0) -> tuple[np.ndarray, float, float, float, float]:
    """
    Compute a simple Canopy Height Model as max Z per grid cell minus 5th percentile per cell.
    Returns (chm_grid, xmin, ymin, cell_size_x, cell_size_y)
    """
    if points.shape[0] == 0:
        raise ValueError("No points provided")
    x, y, z = points[:, 0], points[:, 1], points[:, 2]
    xmin, ymin = x.min(), y.min()
    ix = np.floor((x - xmin) / cell_size).astype(int)
    iy = np.floor((y - ymin) / cell_size).astype(int)
    nx, ny = ix.max() + 1, iy.max() + 1
    max_z = np.full((nx, ny), -np.inf)
    # Compute exact 5th percentile per cell using per-cell accumulation (sufficient for demo sizes)
    per_cell: dict[tuple[int, int], list[float]] = {}
    for i in range(points.shape[0]):
        cx, cy = int(ix[i]), int(iy[i])
        zval = float(z[i])
        if zval > max_z[cx, cy]:
            max_z[cx, cy] = zval
        per_cell.setdefault((cx, cy), []).append(zval)
    p5_z = np.zeros((nx, ny), dtype=float)
    for (cx, cy), zs in per_cell.items():
        if len(zs) == 1:
            p5 = zs[0]
        else:
            p5 = float(np.percentile(np.array(zs, dtype=float), 5))
        p5_z[cx, cy] = p5
    chm = max_z - p5_z
    chm[np.isinf(chm)] = 0.0
    return chm, xmin, ymin, cell_size, cell_size

