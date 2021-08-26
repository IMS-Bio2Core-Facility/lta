# -*- coding: utf-8 -*-
"""Unit tests for the data_handling module."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from pytest_mock import MockerFixture

import lta.helpers.data_handling as dh

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


def test_construct_df(mocker: MockerFixture) -> None:
    """It drops NaNs."""
    df = pd.DataFrame(
        {"a": [np.nan, 1, 2], "b": [np.nan, 1, 2], "c": [np.nan, np.nan, np.nan]},
        index=[0, 1, 2],
    )

    exp = pd.DataFrame({"a": [1, 2], "b": [1, 2]}, index=[1, 2], dtype=np.float64)
    exp.index.names = ["x"]
    exp.columns.names = ["y"]

    # Any attempts to mock pandas in lta.helpers.data_handling
    # Results in a slew of import errors
    mocker.patch("pandas.read_csv", return_value=df)
    results = dh.construct_df(Path("foo"), index_names=["x"], column_names=["y"])
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
