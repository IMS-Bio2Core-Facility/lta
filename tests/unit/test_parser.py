# -*- coding: utf-8 -*-
"""Tests for lta.parser."""
from _pytest import capture

from lta.commands.simple import simple
from lta.parser import lta_parser


def test_correct_usage(capsys: capture.CaptureFixture) -> None:
    """It has the correct usage (ie. structure)."""
    lta_parser.print_usage()
    usage = capsys.readouterr()
    assert (
        usage.out == "usage: lta [-h] [-V] [-t [TEXT]]\n"
    ), "LTA's usage is incorrect."


def test_default_func() -> None:
    """It has the correct default function."""
    assert (
        lta_parser.get_default("func") == simple
    ), "The default function is not lta.commands.simple."
