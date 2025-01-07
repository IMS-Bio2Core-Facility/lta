# -*- coding: utf-8 -*-
"""Unit tests for ``lta.helpers.pipeline``.

Testing datahandling can be a challenge,
particularly for tools designed to handle compler, "omics" data.
At the moment,
only the basic error handling is tested.
If you can provide any contributions towards better unit tests for data science,
please reach out!
"""
import logging
from pathlib import Path

import pandas as pd
import pytest
from pytest_mock import MockerFixture

from lta.helpers import pipeline


def test_raise_NotFound(caplog: pytest.LogCaptureFixture) -> None:
    """It handles FileNotFoundErrors."""
    with pytest.raises(FileNotFoundError):
        pipeline.Pipeline(
            Path("foo.csv"),
            Path("bar"),
            5,
            "spam",
            "eggs",
            "ham",
            "green",
            "sam",
            0.2,
            1,
            True,
        )
    assert caplog.record_tuples == [
        (
            "lta.helpers.pipeline",
            logging.ERROR,
            "foo.csv does not exist. A full traceback follows...",
        )
    ], "Log record is not correct."


def test_raise_NotDir(mocker: MockerFixture, caplog: pytest.LogCaptureFixture) -> None:
    """It handles IsADirectoryErrors."""
    # I don't like mocking, but troubleshooting permissions on Github actions is worse
    mocker.patch(
        "lta.helpers.data_handling.construct_df", side_effect=IsADirectoryError
    )
    with pytest.raises(IsADirectoryError):
        pipeline.Pipeline(
            Path("foo"),
            Path("bar"),
            5,
            "spam",
            "eggs",
            "ham",
            "green",
            "sam",
            0.2,
            1,
            True,
        )
    assert caplog.record_tuples == [
        (
            "lta.helpers.pipeline",
            logging.ERROR,
            "foo is a directory. A full traceback follows...",
        )
    ], "Log record is not correct."


def test_raise_Runtime(mocker: MockerFixture, caplog: pytest.LogCaptureFixture) -> None:
    """It fails if a file is empty."""
    # I don't like mocking, but troubleshooting permissions on Github actions is worse
    mocker.patch(
        "lta.helpers.data_handling.construct_df", side_effect=pd.errors.EmptyDataError
    )
    with pytest.raises(pd.errors.EmptyDataError):
        pipeline.Pipeline(
            Path("foo.csv"),
            Path("bar"),
            5,
            "spam",
            "eggs",
            "ham",
            "green",
            "sam",
            0.2,
            1,
            True,
        )
    assert caplog.record_tuples == [
        (
            "lta.helpers.pipeline",
            logging.ERROR,
            "foo.csv contains no data. A full traceback follows...",
        )
    ], "Log record is not correct."
