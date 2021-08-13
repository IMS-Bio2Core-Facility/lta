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

import pytest
from _pytest import capture
from pytest_mock import MockerFixture

from lta.helpers import pipeline


def test_raise_NotFound(mocker: MockerFixture, capsys: capture.CaptureFixture) -> None:
    """It handles FileNotFoundErrors."""
    mocker.patch("lta.helpers.pipeline.Path.iterdir", side_effect=FileNotFoundError())
    with pytest.raises(FileNotFoundError):
        pipeline.Pipeline(Path("foo"), Path("bar"), 0.2, 10)
    out, err = capsys.readouterr()
    assert out == "foo does not exist.\n"
    assert err == ""


def test_raise_NotDir(mocker: MockerFixture, capsys: capture.CaptureFixture) -> None:
    """It handles NotADirectoryErrors."""
    mocker.patch("lta.helpers.pipeline.Path.iterdir", side_effect=NotADirectoryError())
    with pytest.raises(NotADirectoryError):
        pipeline.Pipeline(Path("foo"), Path("bar"), 0.2, 10)
    out, err = capsys.readouterr()
    assert out == "foo is not directory.\n"
    assert err == ""


def test_raise_Runtime(tmp_path: Path) -> None:
    """It fails if a directory is empty."""
    with pytest.raises(RuntimeError):
        pipeline.Pipeline(tmp_path, Path("bar"), 0.2, 10)
