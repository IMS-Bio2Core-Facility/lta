# -*- coding: utf-8 -*-
"""Unit tests for the data_handling module."""
import sys
from typing import Tuple

import pandas as pd
import pytest

import lta.helpers.data_handling as dh

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


@pytest.mark.parametrize("axis,shape", [("index", (3, 2)), ("columns", (2, 3))])
def test_not_zero(
    binary_df: pd.DataFrame, axis: Literal["index", "columns"], shape: Tuple[int, int]
) -> None:
    """It correctly groups 0s."""
    if axis == "index":
        df = dh.not_zero(binary_df.transpose(), axis, "y", "z", thresh=0.5)
    else:
        df = dh.not_zero(binary_df, axis, "y", "z", 0.5)
    assert df.shape == shape, "The shape after filtering is incorrect."
    assert df.all().all(), "Groups were not correctly detected as not 0."
