# -*- coding: utf-8 -*-
"""Helper functions for handling data.

In order to make the pipeline from ``lta.helpers.pipeline`` more testable,
most of its constructor and processing functions have been moved here.
This makes the code more atomic -
and, thus, testable -
by removing it from the harder to test context of the object.
"""
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

import numpy as np
import pandas as pd

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


def construct_df(
    file: Path, index_names: List[str], column_names: List[str], **kwargs: Any
) -> pd.DataFrame:
    """Construct a dataframe from the given path.

    A light wrapper to handing basic reading and renaming of data.
    I find this function necessary as the parameters required to read metadata
    properly always seem to drop the necessary level names.
    Additionally, it also drops rows and columns that are completely NaN,
    as they are almost certainly uniformative.

    Parameters
    ----------
    file : Path
        The path to the data file
    index_names : List[str]
        The names of the index metadata columns
    column_names : List[str]
        The names of the column metadata rows
    **kwargs : Any
        Further argument passed to ``pd.read_csv``

    Returns
    -------
    pd.DataFrame
        The created dataframe
    """
    counts: pd.DataFrame = (
        pd.read_csv(file, **kwargs)
        .dropna(axis="rows", how="all")
        .dropna(axis="columns", how="all")
    )
    counts.index.names = index_names
    counts.columns.names = column_names
    return counts


def get_unique_level(
    frames: Iterable[pd.DataFrame], axis: Literal["rows", "columns"], level: str
) -> Set[str]:
    """Retrieve unique multiindex level values across dataframes.

    Given a list of dataframes with multi-indices,
    retrieve all unique values across a particular level.

    Parameters
    ----------
    frames : Iterable[pd.DataFrame]
        The data to search
    axis : Literal['rows', 'columns']
        Which multiindex to consider
    level : str
        The level of the multiindex to search

    Returns
    -------
    Set[str]
        The unique experimental values
    """
    values: Set[str] = set()
    if axis == "rows":
        values = values.union(
            *[df.index.get_level_values(level).unique().tolist() for df in frames]
        )
    if axis == "columns":
        values = values.union(
            *[df.columns.get_level_values(level).unique().tolist() for df in frames]
        )
    return values


def split_data(
    frames: Iterable[pd.DataFrame], axis: Literal["rows", "columns"], level: str
) -> Dict[str, List[pd.DataFrame]]:
    """Divide a list of dataframes into groups based on unique values in metadata.

    Given an iterable of dataframes,
    group those dataframes based on unique values in a multiindex level.
    This searches for unique values in the given multiindex level,
    then creates a dictionary where each key/value pair is
    a unique entry from the multiindex and a list of all dataframes
    containing the value at the given level.

    Parameters
    ----------
    frames : Iterable[pd.DataFrame]
        The data to be sorted.
    axis : Literal['rows', 'columns']
        Which multiindex to consider
    level : str
        The level of the multiindex to search

    Returns
    -------
    Dict[str, List[pd.DataFrame]]
        The sorted data.
    """
    values = get_unique_level(frames, axis=axis, level=level)
    if axis == "rows":
        data = {
            val: [
                df for df in frames if df.index.get_level_values(level).unique() == val
            ]
            for val in values
        }
    if axis == "columns":
        data = {
            val: [
                df
                for df in frames
                if df.columns.get_level_values(level).unique() == val
            ]
            for val in values
        }
    return data


def not_zero(
    df: pd.DataFrame,
    axis: Literal["rows", "columns"],
    level: str,
    thresh: float,
    drop: Optional[List[str]] = None,
) -> pd.DataFrame:
    """Mark any group that has more than ``thresh`` fraction 0 as 0.

    Given a counts matrix, mark all counts that are zero.
    Then, groupby the level of the specified multiindex,
    and mark a whole group as 0 if there are more than
    ``thresh * len(group)`` 0s.

    Frustratingly, index levels are lost when grouping on a multiindex.
    To ensure it is correctly added back, the metadata are saved,
    then joined back onto the resultant boolean data frame.

    Parameters
    ----------
    df : pd.DataFrame
        The lipid data to convert to boolean
    axis : Literal['rows', 'columns']
        Which multiindex to consider
    level : str
        The level of the multiindex to groupby
    thresh : float
        The fraction of samples above which a group is said to be 0
    drop : Optional[List[str]]
        A list of levels to drop from the metadata
        Defaults to None

    Returns
    -------
    pd.DataFrame
        The processed data.
    """
    if not drop:
        drop = []
    if axis == "rows":
        metadata = df.index.droplevel(drop).unique()
    if axis == "columns":
        metadata = df.columns.droplevel(drop).unique()
    df = (
        (df == 0)
        .groupby(axis=axis, level=level)
        .transform(lambda x: x.sum() <= (thresh * len(x)))
        .groupby(axis=axis, level=level)
        .all()
    )
    if axis == "rows":
        df = df.loc[:, df.any(axis=axis)].join(pd.DataFrame(index=metadata), how="left")
    if axis == "columns":
        df = (
            df.loc[df.any(axis=axis), :]
            .transpose()
            .join(pd.DataFrame(columns=metadata).transpose(), how="left")
            .transpose()
        )
    return df


def enfc(
    df: pd.DataFrame,
    axis: Literal["rows", "columns"],
    level: str,
    order: Tuple[str, str] = ("experimental", "control"),
) -> pd.Series:
    """Calculate the error normalised fold change for a dataframe.

    ENFC is defined as the log foldchange of lipid levels divide by the propagated error.
    The mean and standard deviation are calculated on the groups in ``level``,
    before applying the above calculation.
    If you haven't filtered your data to remove lipids with no counts,
    you're going to have a bad time.

    By definition,
    fold change requires an experimental and control group,
    othewise the notion of up- or down-regulated makes no sense.
    This function assumes these groups are named "experimental" and "control",
    respectively,
    though alternatives can be passed to the ``order`` argument.

    Parameters
    ----------
    df : pd.DataFrame
        The lipid data to convert to boolean
    axis : Literal['rows', 'columns']
        Which multiindex to consider
    level : str
        The level of the multiindex containing experimental conditions
    order : Tuple[str, str]
        default=('experimental', 'control')
        The names of the conditions to compare.
        Fold change will be ``order[0] / order[1]``.

    Returns
    -------
    pd.DataFrame
        The processed data.
    """
    logfc = np.log10(
        df.groupby(axis=axis, level=level)
        .mean()
        .pipe(lambda df: df.loc[:, order[1]].div(df.loc[:, order[0]]))
    )
    error = (
        df.groupby(axis=axis, level=level).std().pow(2).sum(axis=axis).div(2).pow(0.5)
    )
    return logfc.div(error)
