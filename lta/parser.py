# -*- coding: utf-8 -*-
"""The root `lta` parser.

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
but there is little apparent improvement past ~10000 repetitions.
A deault of 1000 is used to provide a balance between speed and accuracy.

Many calculations are dependent on knowing where certain metadata is stored.
Namely, the experimental conditions (specified with ``--phenotype``)
and the tissue of origin (specified with ``--tissue``).
If these are not passed,
then they default to "Phenotype" and "Tissue", respectively.

Finally,
all options passed in an config file.
This file expects values of the format ``option=value``.
By default,
the CLI looks for ``lta_conf.txt``,
though any file can be specified with the ``-c/--config`` flag.
Values in the config file override the defaults,
and values passed to the CLI override the config file.

Like all good CLIs,
``-V`` returns the version while ``-h/--help`` returns help.

Attributes
----------
lta_parser : argparse.ArgumentParser
    The argument parser for the root command.
"""
from pathlib import Path

import configargparse

from lta import __version__
from lta.commands.run import run
from lta.helpers.custom_types import FloatRange

lta_parser = configargparse.ArgumentParser(
    prog="lta",
    description="Lipid Trafficking Analysis",
    allow_abbrev=False,
    add_config_file_help=True,
    default_config_files=["lta_conf.txt"],
    config_arg_is_required=False,
    ignore_unknown_config_file_keys=True,
    formatter_class=configargparse.ArgumentDefaultsRawHelpFormatter,
)

lta_parser.add_argument(
    "-V",
    action="version",
    version=f"LTA v{__version__}",
    help="Display version information and exit.",
)

lta_parser.add_argument(
    "-c",
    "--config",
    required=False,
    is_config_file=True,
    help="Config file location.",
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
    help="The '0' threshold",
)

lta_parser.add_argument(
    "-b",
    "--boot-reps",
    type=int,
    nargs=1,
    default=20000,
    help="Number of bootstrap repetitions",
)

lta_parser.add_argument(
    "--phenotype",
    type=str,
    default="Phenotype",
    help="Metadata label for experimental conditions",
)

lta_parser.add_argument(
    "--order",
    type=str,
    nargs=2,
    default=["experimental", "control"],
    help="Experimental and control group labels",
)

lta_parser.add_argument(
    "--tissue",
    type=str,
    default="Tissue",
    help="Metadata label for sample tissue",
)

lta_parser.set_defaults(func=run)
