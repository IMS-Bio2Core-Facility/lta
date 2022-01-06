# -*- coding: utf-8 -*-
"""Unit tests for the data_handling module."""
import sys
from pathlib import Path
from typing import List, Optional

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal, assert_series_equal
from pytest_mock import MockerFixture

import lta.helpers.data_handling as dh

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


@pytest.mark.parametrize("index_names", [None, ["one", "two", "three"]])
def test_construct_df(mocker: MockerFixture, index_names: Optional[List[str]]) -> None:
    """It drops NaNs."""
    idx = pd.MultiIndex.from_arrays(
        [
            [None, None, "a", "a", "b", "b"],
            [None, None, "e", "e", "f", "f"],
            ["one", "two", "c", "c", "d", "d"],
        ]
    )
    df = pd.DataFrame(
        {0: ["e", "f", "1", "2", "3", "4"], 1: ["g", "h", 5, 6, 7, 8]}, index=idx
    )

    exp_idx = pd.MultiIndex.from_arrays(
        [["a", "a", "b", "b"], ["e", "e", "f", "f"], ["c", "c", "d", "d"]],
        names=index_names,
    )
    exp_col = pd.MultiIndex.from_arrays([["f", "h"]], names=["two"])
    exp = pd.DataFrame(
        [[1, 5], [2, 6], [3, 7], [4, 8]],
        index=exp_idx,
        columns=exp_col,
    )

    # Any attempts to mock pandas in lta.helpers.data_handling
    # Results in a slew of import errors
    mocker.patch("pandas.read_csv", return_value=df)
    results = dh.construct_df(
        Path("foo"), n_rows=2, metadata=["two"], index_names=index_names
    )
    assert_frame_equal(results, exp)


@pytest.mark.parametrize("axis", ["index", "columns"])
def test_not_zero(
    binary_df: pd.DataFrame,
    axis: Literal["index", "columns"],
) -> None:
    """It correctly groups 0s."""
    exp = pd.DataFrame(
        {("a", "a"): [True, True], ("b", "b"): [True, True], ("c", "c"): [True, True]},
        index=["b", "c"],
    )
    exp.columns.names = ["z", "y"]

    if axis == "index":
        df = dh.not_zero(binary_df.transpose(), axis, "y", "z", thresh=0.5)
        assert_frame_equal(df, exp.transpose())
    else:
        df = dh.not_zero(binary_df, axis, "y", "z", 0.5)
        assert_frame_equal(df, exp)


@pytest.mark.parametrize("axis", ["index", "columns"])
def test_enfc_axis(axis: Literal["index", "columns"]) -> None:
    """It respects the axis."""
    df = pd.DataFrame(
        {
            ("A", "experimental"): [5, 0.5],
            ("B", "experimental"): [15, 1.5],
            ("A", "control"): [1.5, 15],
            ("B", "control"): [0.5, 5],
        }
    )
    df.columns.names = ["first", "second"]

    exp = pd.Series([0.199007, -0.199007], index=[0, 1])

    if axis == "index":
        results = dh.enfc(df.transpose(), axis=axis, level="second")
        assert_series_equal(results, exp)
    else:
        results = dh.enfc(df, axis=axis, level="second")
        assert_series_equal(results, exp)


def test_enfc_order() -> None:
    """It respects passed order."""
    df = pd.DataFrame(
        {
            ("A", "experimental"): [5, 0.5],
            ("B", "experimental"): [15, 1.5],
            ("A", "control"): [1.5, 15],
            ("B", "control"): [0.5, 5],
        }
    )
    df.columns.names = ["first", "second"]

    exp = pd.Series([-0.199007, 0.199007], index=[0, 1])

    results = dh.enfc(
        df, axis="columns", level="second", order=("control", "experimental")
    )
    assert_series_equal(results, exp)
