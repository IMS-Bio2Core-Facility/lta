# -*- coding: utf-8 -*-
"""Helper functions for handling data.

In order to make the pipeline from ``lta.helpers.pipeline`` more testable,
most of its constructor and processing functions have been moved here.
This makes the code more atomic -
and, thus, testable -
by removing it from the harder to test context of the object.
"""
import logging
from pathlib import Path
from typing import Any, List, Literal, Optional, Tuple

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def construct_df(
    file: Path,
    n_rows: int,
    metadata: List[str],
    index_names: Optional[List[str]] = None,
    **kwargs: Any,
) -> pd.DataFrame:
    """Construct a dataframe from the given path.

    A light wrapper to handing the reading of complex metadata.
    It reads the whole dataframe,
    then sices of ``n_rows`` to treat as metadata.
    Any undesired rows are dropped,
    then metadata is added as a multiindex onto the raw data,
    less those rows that were metadata.

    Any row metadata can be retained by specifying the
    ``index_col`` kwarg to ``pd.read_csv``.

    Parameters
    ----------
    file : Path
        The path to the data file
    n_rows : int
        The number of rows in the column metadata
    metadata : List[str]
        The metadata rows to include
    index_names : Optional[List[str]]
        Names for the data frame multi-index
    **kwargs : Any
        Further argument passed to ``pd.read_csv``

    Returns
    -------
    pd.DataFrame
        The created dataframe
    """
    counts: pd.DataFrame = pd.read_csv(file, **kwargs)

    # Retrieve column metadata
    cols = counts.iloc[:n_rows, :].copy()
    cols.index = cols.index.droplevel([0, 1])
    cols = cols.loc[metadata, :]

    # Create final dataframe
    data = counts.iloc[n_rows:, :].copy()
    data.columns = pd.MultiIndex.from_frame(cols.transpose())
    if index_names:
        data.index.names = index_names

    # Force numeric types
    data = data.apply(pd.to_numeric)

    return data


def not_zero(
    df: pd.DataFrame,
    axis: Literal["index", "columns"],
    level: str,
    compartment: str,
    thresh: float,
) -> pd.DataFrame:
    """Mark any group that has more than ``thresh`` fraction 0 as 0.

    Given a counts matrix, mark all counts that are zero.
    Then, groupby the level of the specified multiindex,
    and mark a whole group as 0 if there are more than
    ``thresh * len(group)`` 0s.
    Finally,
    any lipid that is all 0 is dropped on the specified ``axis``

    Grouping occurs across compartment and level in that order.

    Parameters
    ----------
    df : pd.DataFrame
        The lipid data to convert to boolean
    axis : Literal['index', 'columns']
        Which multiindex to consider
    level : str
        The level of the multiindex to groupby
    compartment : str
        The level of the multiindex containing compartment sample
    thresh : float
        The fraction of samples above which a group is said to be 0

    Returns
    -------
    pd.DataFrame
        The processed data.
    """
    df = (
        (df == 0)
        .groupby(axis=axis, level=[compartment, level])
        .agg(lambda x: x.sum() <= (thresh * len(x)))
    )
    if axis == "index":
        df = df.loc[:, df.any(axis=axis)]
    if axis == "columns":
        df = df.loc[df.any(axis=axis), :]
    return df


def enfc(
    df: pd.DataFrame,
    axis: Literal["index", "columns"],
    level: str,
    order: Optional[Tuple[str, str]] = None,
) -> pd.DataFrame:
    """Calculate the error normalised fold change for a dataframe.

    ENFC is defined as the log foldchange of lipid levels divide by the propagated error.
    The mean and standard deviation are calculated on the groups in ``level``,
    before applying the above calculation.

    Notes
    -----
    By definition,
    fold change requires an experimental and control group,
    othewise the notion of up- or down-regulated makes no sense.
    This function assumes these groups are named "experimental" and "control",
    respectively,
    though alternatives can be passed to the ``order`` argument.

    Additionally,
    the notion of fold change requires both samples to be non-0.
    When either x/0, 0/x, or 0/0 occurs during the FC calculation,
    these values are returned as NaN.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe containing lipid expression values
    axis : Literal['index', 'columns']
        Which multiindex to consider
    level : str
        The level of the multiindex containing experimental conditions
    order : Optional[Tuple[str, str]]
        default=('experimental', 'control')
        The names of the conditions to compare.
        Fold change will be ``order[0] / order[1]``.

    Returns
    -------
    pd.DataFrame
        The processed data.
    """
    if not order:
        logging.debug("Order not passed. Defaulting to ('experimental', 'control')")
        order = ("experimental", "control")
    mean = df.groupby(axis=axis, level=level).mean()
    logging.debug(f"Grouping/filtering on {axis}.")
    # Replace inf (x/0) with NaN
    # Replace 0 (0/x) with NaN
    # 0/0 is already NaN
    if axis == "index":
        logfc = np.log10(
            mean.loc[order[0], :]
            .div(mean.loc[order[1], :])
            .replace([np.inf, -np.inf, 0], np.NAN)
        )
    else:
        logfc = np.log10(
            mean.loc[:, order[0]]
            .div(mean.loc[:, order[1]])
            .replace([np.inf, -np.inf, 0], np.NAN)
        )
    error = (
        df.groupby(axis=axis, level=level).std().pow(2).sum(axis=axis).div(2).pow(0.5)
    )
    return logfc.div(error)
