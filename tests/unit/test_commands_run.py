# -*- coding: utf-8 -*-
"""Tests for the simple command function."""
import argparse

from _pytest import capture

from lta.commands.run import run


def test_prints_text(capsys: capture.CaptureFixture) -> None:
    """It prints the text."""
    args = argparse.Namespace(folder="data", output="results", threshold=[0.2])
    run(args)
    out, err = capsys.readouterr()
    assert err == "", "The run call errored."
    assert out == "data results [0.2]\n", "Simple did not print the write text."
