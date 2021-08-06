# -*- coding: utf-8 -*-
"""Tests for the simple command function."""
import argparse

from _pytest import capture

from lta.commands.simple import simple


def test_prints_text(capsys: capture.CaptureFixture) -> None:
    """It prints the text."""
    args = argparse.Namespace(text="Hello World")
    simple(args)
    out, err = capsys.readouterr()
    assert err == "", "The simple call errored."
    assert out == "Hello World\n", "Simple did not print the write text."
