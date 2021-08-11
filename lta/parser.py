# -*- coding: utf-8 -*-
"""The root `lta` parser.

Functionality will be added during on-going refactoring from R.

The current code represents a minimum functioning command.

Like all good CLIs, `-V/--version` returns the version while `-h/--help` help for the
root command. Help for the subcommands can be found by calling `-h` after a subcommand,
like this: `lta sub -h`.

Attributes
----------
lta_parser : argparse.ArgumentParser
    The argument parser for the root command.
"""
import argparse
from pathlib import Path

from lta import __version__
from lta.commands.simple import simple
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
    "data",
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

lta_parser.set_defaults(func=simple)
