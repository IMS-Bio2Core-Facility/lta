# -*- coding: utf-8 -*-
"""Fixtures for pytest."""
from itertools import cycle, islice
from typing import Callable, List, Tuple

import numpy as np
import numpy.random as rand
import pandas as pd
import pytest


@pytest.fixture
def create_df() -> Callable[
    [Tuple[int, int], int, List[str], int, List[str]], pd.DataFrame
]:
    """Create a "random" dataframe.

    Technically, pytest fixtures don't take arguments.
    A form of argument passing can be achieved with indirect parametrization,
    but this iterates over the arguments,
    running each test multiple times.
    This isn't quite what we want,
    as we need to create (sometimes multiple) dataframes per test,
    running each test once.
    This is a bit of cheeky magic to create a fixture that "accepts" arguments.
    In reality, it is returning a function that does what we want.

    Returns
    -------
    Callable[[Tuple[int, int], int, List[str], int, List[str]], pd.DataFrame]
        A function that creates a random numeric dataframe.
        The first argument is the shape of the dataframe.
        The second and third argument is the number of levels and names for the row multiindex.
        The fourth and fifth argument is the number of levels and names for the column multiindex.
    """

    def _creator(
        dims: Tuple[int, int],
        index_levels: int,
        index_names: List[str],
        column_levels: int,
        column_names: List[str],
    ) -> pd.DataFrame:
        """Generate dataframe."""
        repeat = lambda x: list(islice(cycle(["a", "b", "c"]), x))

        data = rand.rand(*dims)
        index_data = np.array([repeat(dims[0]) for _ in range(index_levels)])
        column_data = np.array([repeat(dims[1]) for _ in range(column_levels)])
        return pd.DataFrame(
            data,
            columns=pd.MultiIndex.from_arrays(column_data, names=column_names),
            index=pd.MultiIndex.from_arrays(index_data, names=index_names),
        )

    return _creator
