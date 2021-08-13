# -*- coding: utf-8 -*-
"""The root `lta` parser.

Functionality will be added during on-going refactoring from R.

The current code represents a minimum functioning command.

For a detailed description of the tool and how to use it,
please see the README.
A short overview is given here.

The location of the input data is the first positional argument,
while the location to which the output files should be saved is the second positional.
The "0" threshold is specified with option ``-t/--threshold``.
This should be passed as a floating point number between 0 and 1, inclusive.
If it is not provided,
then a default of 0.2 is used.
The number of bootstrap replicates to use for estimating the p-values
can be specified with ``-b/--boot-reps``.
Generally, higher repetitions increases accuracy,
but there is little apparent improvement past ~20000 repetitions
(the default).

Like all good CLIs,
``-V/--version`` returns the version while ``-h/--help`` returns help.

Attributes
----------
lta_parser : argparse.ArgumentParser
    The argument parser for the root command.
"""
import argparse
from pathlib import Path

from lta import __version__
from lta.commands.run import run
from lta.helpers.custom_types import FloatRange

lta_parser = argparse.ArgumentParser(
    prog="lta", description="Lipid Trafficking Analysis"
)

lta_parser.add_argument(
    "-V",
    "--version",
    action="version",
    version=f"LTA v{__version__}",
    help="Display version information and exit.",
)

lta_parser.add_argument(
    "folder",
    type=Path,
    help="Location of the data files.",
)

lta_parser.add_argument(
    "output",
    type=Path,
    help="Where to write output file.",
)

# The type ignore silence mypy.
# Since we are checking, not iterating, a proper __iter__ is unnecessary
lta_parser.add_argument(
    "-t",
    "--threshold",
    type=float,
    choices=FloatRange(0, 1),  # type: ignore
    nargs=1,
    default=0.2,
)

lta_parser.add_argument(
    "-b",
    "--boot-reps",
    type=int,
    nargs=1,
    default=20000,
)

lta_parser.set_defaults(func=run)
