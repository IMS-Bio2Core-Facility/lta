# -*- coding: utf-8 -*-
"""Tests for the CLI.

This **will not** test built-in features of argparse,
such as const/default with `nargs='?'`,
the version flag,
or the help flag.
It **will** test that any custom code plugged into the parser behaves correctly.
"""
import argparse

from _pytest import capture

from lta.cli import main
from lta.commands.simple import simple


def test_echoes_text(capsys: capture.CaptureFixture) -> None:
    """The CLI prints text passed to it."""
    args = argparse.Namespace(
        func=simple, data="data", output="results", threshold=[0.2]
    )
    main(args)
    out, err = capsys.readouterr()
    assert err == "", "The main call errored."
    assert out == "data results [0.2]\n", "The main call echoed the wrong text."
