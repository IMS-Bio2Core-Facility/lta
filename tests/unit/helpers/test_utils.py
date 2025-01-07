"""Unit tests for utility functions in the utils module."""

import numpy as np
import pandas as pd

from lta.helpers import utils


def test_merge_dataframe_by_level() -> None:
    """Test the merge_dataframe_by_level function."""
    idx = pd.MultiIndex.from_product(
        [["A", "B", "C"], ["1", "2", "3"]], names=["alphabet", "numeric"]
    )
    col = ["c1", "c2", "c3", "c4"]

    df1_data, df2_data = (
        np.array([[f"d{i+1}_{i1}{i2}_{c}" for c in col] for i1, i2 in idx])
        for i in range(2)
    )
    assert (df1_data != df2_data).all()
    frames = [
        pd.DataFrame(df1_data, idx, col),
        pd.DataFrame(df2_data, idx, col),
    ]
    res = utils.merge_dataframe_by_columns(datas=frames)
    assert res.index.identical(idx)
    assert res.columns.identical(pd.Index(col * 2))
    assert (res.to_numpy() == np.append(df1_data, df2_data, axis=1)).all()


def test_add_level_to_multi_index() -> None:
    """Test the add_level_to_index function."""
    idx = pd.MultiIndex.from_product(
        [["A", "B", "C"], ["1", "2", "3"]], names=["alphabet", "numeric"]
    )
    expected = pd.MultiIndex.from_product(
        [["A", "B", "C"], ["1", "2", "3"], ["ADDED"]],
        names=["alphabet", "numeric", "newly added"],
    )
    res = utils.add_level_to_index(
        index=idx, new_level="ADDED", new_level_name="newly added"
    )
    assert res.identical(expected)


def test_reorder_column_index() -> None:
    """Test the reorder_column_index function."""
    idx = pd.MultiIndex.from_product(
        [["A", "B", "C"], ["1", "2", "3"]], names=["alphabet", "numeric"]
    )
    new_idx = utils.reorder_index(index=idx, orders=["numeric", "alphabet"])
    col = ["c1", "c2", "c3", "c4"]
    df_data = np.array([[f"d{i1}{i2}_{c}" for c in col] for i1, i2 in idx])
    expected = pd.DataFrame(df_data, new_idx, col)
    res = pd.DataFrame(df_data, idx, col)
    res.index = new_idx
    assert expected.equals(res)


def test_sort_columns() -> None:
    """Test the sort_columns function."""
    idx = ["c1", "c2", "c3", "c4"]
    expected_col = pd.MultiIndex.from_product(
        [["A", "B", "C"], ["2", "3", "1"]], names=["alphabet", "numeric"]
    )
    expected_data = np.array(
        [[f"d{i1}{i2}_{c}" for c in idx] for i1, i2 in expected_col]
    ).T
    expected = pd.DataFrame(expected_data, idx, expected_col)
    col = pd.MultiIndex.from_product(
        [["A", "B", "C"], ["1", "2", "3"]], names=["alphabet", "numeric"]
    )
    df_data = np.array([[f"d{i1}{i2}_{c}" for c in idx] for i1, i2 in col]).T
    df = pd.DataFrame(df_data, idx, col)
    res = utils.sort_columns(data=df, level="numeric", pressing=["2", "3"])
    assert expected.equals(res)
