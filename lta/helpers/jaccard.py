# -*- coding: utf-8 -*-
"""Jaccard similarities and their p-values.

The code here represents a python implementation of the Jaccard package hosted
`here <https://github.com/ncchung/jaccard>`_ by N. Chung. Its citation follows.

Citation
--------
Chung, N., Miasojedow, B., Startek, M., and Gambin, A. "Jaccard/Tanimoto similarity test and estimation methods for biological presence-absence data" BMC Bioinformatics (2019) 20(Suppl 15): 644. https://doi.org/10.1186/s12859-019-3118-5
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
    """Calculate Jaccard similarity.

    The vectors must be of the same length, and must be boolean.

    Parameters
    ----------
    x : np.ndarray
        A boolean array.
    y : np.ndarray
        A boolean array.
    center : bool, default=False  # noqa: DAR103
        Whether to center the score.
    px : Optional[float]
        The probability of success in x.
        If None, then px = x.mean()
    py : Optional[float]
        The probability of success in x.
        If None, then px = x.mean()

    Returns
    -------
    float
        The Jaccard similarity between the 2 vectors

    Raises
    ------
    IndexError
        If the vectors are not 1-d, or if the vectors are not the same length.
    TypeError
        If the vectors are not boolean.

    """
    if x.ndim != 1 or y.ndim != 1:
        logging.error(
            f"All vectors must be 1-d. ndims: {[x.ndim, y.ndim]}.", stack_info=True
        )
        raise IndexError
    if x.shape != y.shape:
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
        logging.debug("px not provided. Calculating as mean of x.")
        px = x.mean()
        assert isinstance(px, float)
    if py is None:
        logging.debug("py not provided. Calculating as mean of y.")
        py = y.mean()
        assert isinstance(py, float)

    intersect = (x & y).sum()
    union = x.sum() + y.sum() - intersect

    denominator = px + py - (px * py)
    if denominator == 0:
        logging.debug("Denominator is 0. Returning np.nan")
        return np.nan

    if union == 0:
        logging.debug("Union is 0. Calculating using px and py.")
        j = (px * py) / denominator
    else:
        j = intersect / union

    if center:
        logging.debug("Centering J.")
        return j - ((px * py) / denominator)
    else:
        return j


def distance(
    x: np.ndarray, y: np.ndarray, px: Optional[float] = None, py: Optional[float] = None
) -> float:
    """Calculate Jaccard distance.

    Classically defined as:

    Jdist = 1 - Jsimiliarity

    The vectors must be of the same length, and must be boolean.

    Note
    ----
    The centering method applied in Jaccard similarity is not
    applicable here, so it is not passed as an option.

    Parameters
    ----------
    x : np.ndarray
        A boolean array.
    y : np.ndarray
        A boolean array.
    px : Optional[float]
        The probability of success in x.
        If None, then px = x.mean()
    py : Optional[float]
        The probability of success in x.
        If None, then px = x.mean()

    Returns
    -------
    float
        The Jaccard distance between the 2 vectors
    """
    if px is None:
        logging.debug("px not provided. Calculating as mean of x.")
        px = x.mean()
        assert isinstance(px, float)
    if py is None:
        logging.debug("py not provided. Calculating as mean of y.")
        py = y.mean()
        assert isinstance(py, float)
    return 1 - similarity(x, y, center=False, px=px, py=py)


def bootstrap(
    x: np.ndarray,
    y: np.ndarray,
    px: Optional[float] = None,
    py: Optional[float] = None,
    n: int = 1000,
    seed: int = 42,
) -> pd.Series:
    """Use the bootstrap test to return a p-value.

    The p-value is defined as the fraction of values in the null statistic
    whose absolute value is greater than the absolute value of the observed
    statistic.

    Note
    ----
    Returning a series facilitates applications with pandas and groupby.

    Parameters
    ----------
    x : np.ndarray
        a boolean array.
    y : np.ndarray
        a boolean array.
    n : int
        the number of bootstrap repetitions to perform.
    px : Optional[float]
        The probability of success in x.
        If None, then px = x.mean()
    py : Optional[float]
        The probability of success in x.
        If None, then px = x.mean()
    seed : int
        the random seed to use for resampling.

    Returns
    -------
    Tuple[float, float]
        The Jaccard similarity and p_val.
    """
    j = similarity(x, y, center=False, px=px, py=py)
    if px is None:
        logging.debug("px not provided. Calculating as mean of x.")
        px = x.mean()
        assert isinstance(px, float)
    if py is None:
        logging.debug("py not provided. Calculating as mean of y.")
        py = y.mean()
        assert isinstance(py, float)
    if px == 1 or py == 1 or len(x) == x.sum() or len(y) == y.sum():
        logger.warning("Bootstrap is degenerate as at least one vector is all 1.")
        return pd.Series([j, 1], index=["J-sim", "p-val"])
    if px == 0 or py == 0 or x.sum() == 0 or y.sum() == 0:
        logger.warning("Bootstrap is degenerate as at least one vector is all 0.")
        return pd.Series([j, 1], index=["J-sim", "p-val"])

    j_obs = similarity(x, y, center=True, px=px, py=py)

    rng = np.random.default_rng(seed)
    vals = (  # pragma: no branch
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
