# -*- coding: utf-8 -*-
"""Unit tests for the data_handling module."""
import sys
from typing import Callable, List, Tuple

import pandas as pd
import pytest

import lta.helpers.data_handling as dh

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


@pytest.mark.parametrize("axis,shape", [("rows", (3, 2)), ("columns", (2, 3))])
def test_not_zero(
    binary_df: pd.DataFrame, axis: Literal["rows", "columns"], shape: Tuple[int, int]
) -> None:
    """It correctly groups 0s."""
    if axis == "rows":
        df = dh.not_zero(binary_df.transpose(), axis, "y", 0.5)
    if axis == "columns":
        df = dh.not_zero(binary_df, axis, "y", 0.5)
    assert df.shape == shape
    assert df.index.names == list("xyz")
    assert df.columns.names == list("xyz")


@pytest.mark.parametrize(
    "axis,drop,rows,columns",
    [
        ("rows", ["x", "y"], ["z"], ["x", "y", "z"]),
        ("columns", ["x", "y"], ["x", "y", "z"], ["z"]),
    ],
)
def test_not_zero_drop(
    create_df: Callable,
    axis: Literal["rows", "columns"],
    drop: List[str],
    rows: List[str],
    columns: List[str],
) -> None:
    """It correctly drops levels."""
    df = dh.not_zero(create_df(dims=(6, 6)), axis, "z", 0.2, drop=drop)
    # Need to think of way to test thresh accuracy
    assert df.index.names == rows
    assert df.columns.names == columns
