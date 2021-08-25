# -*- coding: utf-8 -*-
"""Unit tests for ``lta.helpers.pipeline``.

Testing datahandling can be a challenge,
particularly for tools designed to handle compler, "omics" data.
At the moment,
only the basic error handling is tested.
If you can provide any contributions towards better unit tests for data science,
please reach out!
"""
from pathlib import Path
from tempfile import gettempdir

import pandas as pd
import pytest
from _pytest import capture
from pytest_mock import MockerFixture

from lta.helpers import pipeline


def test_raise_NotFound(capsys: capture.CaptureFixture) -> None:
    """It handles FileNotFoundErrors."""
    with pytest.raises(FileNotFoundError):
        pipeline.Pipeline(Path("foo.csv"), Path("bar"), "spam", "eggs", "green", 0.2, 1)
    out, err = capsys.readouterr()
    assert out == "foo.csv does not exist.\n"
    assert err == ""


def test_raise_NotDir(capsys: capture.CaptureFixture) -> None:
    """It handles NotADirectoryErrors."""
    with pytest.raises(IsADirectoryError):
        pipeline.Pipeline(
            Path(gettempdir()), Path("bar"), "spam", "eggs", "green", 0.2, 1
        )
    out, err = capsys.readouterr()
    assert out == f"{gettempdir()} is a directory.\n"
    assert err == ""


def test_raise_Runtime(mocker: MockerFixture) -> None:
    """It fails if a directory is empty."""
    mocker.patch("lta.helpers.data_handling.construct_df", return_value=pd.DataFrame())
    with pytest.raises(RuntimeError):
        pipeline.Pipeline(Path("foo"), Path("bar"), "spam", "eggs", "green", 0.2, 1)
