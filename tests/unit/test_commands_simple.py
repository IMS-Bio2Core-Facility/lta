# -*- coding: utf-8 -*-
"""Tests for the simple command function."""
import argparse

from _pytest import capture

from lta.commands.simple import simple


def test_prints_text(capsys: capture.CaptureFixture) -> None:
    """It prints the text."""
    args = argparse.Namespace(data="data", output="results", threshold=[0.2])
    simple(args)
    out, err = capsys.readouterr()
    assert err == "", "The simple call errored."
    assert out == "data results [0.2]\n", "Simple did not print the write text."
