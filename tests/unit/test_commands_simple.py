# -*- coding: utf-8 -*-
"""Tests for the simple command function."""
import argparse

from _pytest import capture

from lta.commands.simple import simple


def test_prints_text(capsys: capture.CaptureFixture) -> None:
    """It prints the text."""
    args = argparse.Namespace(data="data", output="results")
    simple(args)
    out, err = capsys.readouterr()
    assert err == "", "The simple call errored."
    assert out == "data results\n", "Simple did not print the write text."
