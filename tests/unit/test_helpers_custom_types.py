# -*- coding: utf-8 -*-
"""Unit tests for the lta.helpers.custom_types module."""
from collections.abc import Iterable

from _pytest import capture

from lta.helpers.custom_types import FloatRange


def test_FloatRange_attributes() -> None:
    """It has a start and end value."""
    fr = FloatRange(0, 1)
    assert fr.start == 0, "FloatRange's start value is not correct."
    assert fr.end == 1, "FloatRange's end value is not correct."


def test_FloatRange_repr(capsys: capture.CaptureFixture) -> None:
    """It correctly prints the repr."""
    fr = FloatRange(0, 1)
    print(fr)
    usage = capsys.readouterr()
    assert usage.out == "[0, 1]\n", "FloatRange's repr is not correct."


def test_FloatRange_contains() -> None:
    """It checks the range contains a value."""
    fr = FloatRange(0, 1)
    assert fr.__contains__(0.5), "FloatRange doesn't detect a value in range."
    assert not fr.__contains__(2), "FloatRange doesn't detect a value out of range."


def test_FloatRange_iter() -> None:
    """It is iterable."""
    fr = FloatRange(0, 1)
    assert isinstance(fr, Iterable), "FloatRange is not iterable."
