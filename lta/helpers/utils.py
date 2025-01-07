"""Utility functions for DataFrame manipulation."""

import itertools
import operator
import typing

import pandas as pd


def merge_dataframe_by_columns(
    *,
    datas: typing.Iterable[pd.DataFrame],
) -> pd.DataFrame:
    """
    Merge multiple DataFrames by columns.

    Parameters
    ----------
    datas : typing.Iterable[pd.DataFrame]
        The DataFrames to merge.

    Returns
    -------
    pd.DataFrame
        The merged DataFrame.
    """
    output_df = pd.concat(datas, axis="columns")

    return output_df


def add_level_to_index(
    *,
    index: typing.Union[pd.MultiIndex, pd.Index],
    new_level: typing.Hashable,
    new_level_name: str,
) -> pd.MultiIndex:
    """
    Add a new level to the index of a DataFrame.

    Parameters
    ----------
    index : typing.Union[pd.MultiIndex, pd.Index]
        The index to add a level to.
    new_level : typing.Hashable
        The value to add to the new level.
    new_level_name : str
        The name of the new level.

    Returns
    -------
    pd.MultiIndex
        The new MultiIndex.
    """
    names = index.names + [new_level_name]
    if isinstance(index, pd.MultiIndex):
        index = index.to_flat_index()
    return pd.MultiIndex.from_tuples(
        [val + (new_level,) for val in index.array], names=names
    )


def reorder_index(
    *,
    index: typing.Union[pd.MultiIndex, pd.Index],
    orders: typing.List[typing.Union[str, int]],
) -> pd.MultiIndex:
    """
    Reorder the levels of a MultiIndex.

    Parameters
    ----------
    index : typing.Union[pd.MultiIndex, pd.Index]
        The index to reorder.
    orders : typing.List[typing.Union[str, int]]
        The new order of the levels.

    Returns
    -------
    pd.MultiIndex
        The reordered MultiIndex.
    """
    if isinstance(index, pd.MultiIndex):
        return index.reorder_levels(orders)
    return index


def sort_columns(
    *,
    data: pd.DataFrame,
    level: typing.Union[str, int],
    pressing: typing.List[typing.Union[str, int]],
) -> pd.DataFrame:
    """
    Sort the columns of a DataFrame.

    Parameters
    ----------
    data : pd.DataFrame
        The DataFrame to sort.
    level : typing.Union[str, int]
        The level to sort on.
    pressing : typing.List[typing.Union[str, int]]
        The columns to press to the front.

    Returns
    -------
    pd.DataFrame
        The sorted DataFrame.
    """
    idx = data.columns
    pressed = set(pressing)
    # get correct ordering of the index
    level_ordering = pressing + list(
        # filter out the pressing columns
        map(
            operator.itemgetter(0),
            itertools.groupby(
                sorted(
                    v for v in idx.get_level_values(level).values if v not in pressed
                )
            ),
        )
    )

    if not isinstance(idx, pd.MultiIndex):
        return data.reindex(columns=level_ordering, level=level)

    # recreate Multiindex with mapping and reindex all columns
    new_level_index = data.reindex(level=level, columns=level_ordering).columns
    new_column_order_map = dict(
        zip(  # noqa: B905
            idx[idx.isin(new_level_index)],
            new_level_index,
            # strict=True, TODO: Remove this when python3.9 is suppport is dropped
        )
    )
    new_multi_index = pd.MultiIndex.from_tuples(
        [new_column_order_map.get(x, x) for x in idx],
        names=idx.names,
    )
    return data.reindex(new_multi_index, axis=1)
