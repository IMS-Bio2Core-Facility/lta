# -*- coding: utf-8 -*-
"""Jaccard similarities and their p-values.

Vendored from boolean-jaccard 0.1.1 (https://github.com/rbpatt2019/boolean-jaccard),
which is unmaintained and capped at Python <3.11.
Original: python port of the R jaccard package by N. Chung.
"""

import logging
from typing import Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def similarity(
    x: np.ndarray,
    y: np.ndarray,
    center: bool = False,
    px: Optional[float] = None,
    py: Optional[float] = None,
) -> float:
    """Calculate Jaccard similarity."""
    if x.ndim != 1 or y.ndim != 1:
        logging.error(
            f"All vectors must be 1-d. ndims: {[x.ndim, y.ndim]}.", stack_info=True
        )
        raise IndexError
    if x.shape != y.shape:  # type: ignore[operator]
        logging.error(
            f"All vectors must have the same length. shape: {[x.shape, y.shape]}",
            stack_info=True,
        )
        raise IndexError
    if x.dtype != bool or y.dtype != bool:
        logging.error(
            f"All vectors must be boolean. dtypes: {[x.dtype, y.dtype]}",
            stack_info=True,
        )
        raise TypeError

    if px is None:
        px = float(x.mean())
    if py is None:
        py = float(y.mean())

    intersect = (x & y).sum()
    union = x.sum() + y.sum() - intersect

    denominator = px + py - (px * py)
    if denominator == 0:
        return np.nan

    if union == 0:
        j = (px * py) / denominator
    else:
        j = intersect / union

    if center:
        return j - ((px * py) / denominator)
    return j


def distance(
    x: np.ndarray, y: np.ndarray, px: Optional[float] = None, py: Optional[float] = None
) -> float:
    """Calculate Jaccard distance (1 - similarity)."""
    if px is None:
        px = float(x.mean())
    if py is None:
        py = float(y.mean())
    return 1 - similarity(x, y, center=False, px=px, py=py)


def bootstrap(
    x: np.ndarray,
    y: np.ndarray,
    px: Optional[float] = None,
    py: Optional[float] = None,
    n: int = 1000,
    seed: int = 42,
) -> pd.Series:
    """Bootstrap p-value for Jaccard similarity."""
    j = similarity(x, y, center=False, px=px, py=py)
    if px is None:
        px = float(x.mean())
    if py is None:
        py = float(y.mean())
    if px == 1 or py == 1 or len(x) == x.sum() or len(y) == y.sum():
        logger.warning("Bootstrap is degenerate as at least one vector is all 1.")
        return pd.Series([j, 1], index=["J-sim", "p-val"])
    if px == 0 or py == 0 or x.sum() == 0 or y.sum() == 0:
        logger.warning("Bootstrap is degenerate as at least one vector is all 0.")
        return pd.Series([j, 1], index=["J-sim", "p-val"])

    j_obs = similarity(x, y, center=True, px=px, py=py)

    rng = np.random.default_rng(seed)
    vals = (
        similarity(
            rng.choice(x, size=len(x), replace=True, shuffle=False),
            rng.choice(y, size=len(y), replace=True, shuffle=False),
            center=True,
        )
        for _ in range(n)
    )
    j_null = np.fromiter(vals, dtype=np.float32, count=n)
    np.abs(j_null, dtype=np.float32, out=j_null)
    p_val = (j_null >= np.abs(j_obs)).sum() / n
    return pd.Series([j, p_val], index=["J-sim", "p-val"])
