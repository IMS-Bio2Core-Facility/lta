# -*- coding: utf-8 -*-
"""Unit tests for the data_handling module."""
import sys
from typing import Callable, List, Tuple

import pytest

import lta.helpers.data_handling as dh

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


def test_get_unique_rows(create_df: Callable) -> None:
    """It checks the row axis."""
    values = dh.get_unique_level(
        [create_df(dims=(2, 2)), create_df(dims=(3, 2))], axis="rows", level="y"
    )
    assert values == {"a", "b", "c"}


def test_get_unique_columns(create_df: Callable) -> None:
    """It checks the columns axis."""
    values = dh.get_unique_level(
        [create_df(dims=(2, 2)), create_df(dims=(2, 3))], axis="columns", level="y"
    )
    assert values == {"a", "b", "c"}


@pytest.mark.parametrize("axis,shape", [("rows", (3, 6)), ("columns", (6, 3))])
def test_not_zero_rows(
    create_df: Callable, axis: Literal["rows", "columns"], shape: Tuple[int, int]
) -> None:
    """It correctly groups 0s."""
    df = dh.not_zero(create_df(dims=(6, 6)), axis, "y", 0.2)
    # Need to think of way to test thresh accuracy
    assert all([x == "bool" for x in df.dtypes])
    if axis == "rows":
        assert df.index.names == ["x", "y", "z"]
    if axis == "columns":
        assert df.index.names == ["x", "y", "z"]
    assert df.shape == shape


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
