import typing
import pandas as pd


def merge_dataframe_by_level(
    *, datas: typing.Iterable[pd.DataFrame], levels: typing.Iterable[typing.Hashable]
) -> pd.DataFrame:
    output_df = pd.concat(datas, axis="columns", levels=levels)

    return output_df


def add_level_to_index(
    *, index: pd.MultiIndex | pd.Index, new_level: typing.Any, new_level_name: str
) -> pd.MultiIndex:
    names = index.names + [new_level_name]
    if isinstance(index, pd.MultiIndex):
        index = index.to_flat_index()
    return pd.MultiIndex.from_tuples(
        list(val + (new_level,) for val in index.array), names=names
    )
