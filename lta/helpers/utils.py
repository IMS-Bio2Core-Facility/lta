import itertools
import operator
import typing
import pandas as pd


def merge_dataframe_by_level(
    *, datas: typing.Iterable[pd.DataFrame], levels: typing.Iterable[typing.Hashable]
) -> pd.DataFrame:
    output_df = pd.concat(datas, axis="columns", levels=levels)

    return output_df


def add_level_to_index(
    *, index: typing.Union[pd.MultiIndex, pd.Index], new_level: typing.Any, new_level_name: str
) -> pd.MultiIndex:
    names = index.names + [new_level_name]
    if isinstance(index, pd.MultiIndex):
        index = index.to_flat_index()
    return pd.MultiIndex.from_tuples(list(val + (new_level,) for val in index.array), names=names)


def reorder_index(
    *,
    index: typing.Union[pd.MultiIndex, pd.Index],
    orders: typing.List[typing.Union[str, int]],
) -> pd.MultiIndex:
    if isinstance(index, pd.MultiIndex):
        return index.reorder_levels(orders)
    return index


def sort_columns(
    *,
    data: pd.DataFrame,
    level: typing.Union[str, int],
    pressing: typing.List[typing.Union[str, int]],
) -> pd.DataFrame:
    idx = data.columns
    pressed = set(pressing)
    # get correct ordering of the index
    level_ordering = pressing + list(
        # filter out the pressing columns
        map(
            operator.itemgetter(0),
            itertools.groupby(sorted(v for v in idx.get_level_values(level).values if v not in pressed)),
        )
    )

    if not isinstance(idx, pd.MultiIndex):
        return data.reindex(columns=level_ordering, level=level)

    # recreate Multiindex with mapping and reindex all columns
    new_level_index = data.reindex(level=level, columns=level_ordering).columns
    new_column_order_map = dict(zip(idx[idx.isin(new_level_index)], new_level_index))
    new_multi_index = pd.MultiIndex.from_tuples(
        [new_column_order_map.get(x, x) for x in idx],
        names=idx.names,
    )
    return data.reindex(new_multi_index, axis=1)
