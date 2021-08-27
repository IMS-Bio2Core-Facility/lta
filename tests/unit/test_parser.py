# -*- coding: utf-8 -*-
"""Tests for lta.parser."""
from _pytest import capture

from lta.commands.run import run
from lta.parser import lta_parser

expected = """usage: lta [-h] [-c CONFIG] [-t {[0, 1]}] [-b BOOT_REPS]
           [--phenotype PHENOTYPE] [--order ORDER ORDER] [--tissue TISSUE]
           [--mode MODE] [-V] [-v] [-l LOGFILE]
           file output
"""


def test_correct_usage(capsys: capture.CaptureFixture) -> None:
    """It has the correct usage (ie. structure)."""
    lta_parser.print_usage()
    usage = capsys.readouterr()
    assert usage.out == expected, "LTA's usage is incorrect."


def test_default_func() -> None:
    """It has the correct default function."""
    assert (
        lta_parser.get_default("func") == run
    ), "The default function is not lta.commands.run."
