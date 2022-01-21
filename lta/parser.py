# -*- coding: utf-8 -*-
"""The root `lta` parser.

For a detailed description of the tool and how to use it,
please see the README.
A short overview is given here.

The location of the input data file is the first positional argument,
while the location to which the output files should be saved is the second positional.
The "0" threshold is specified with option ``-t/--threshold``.
This should be passed as a floating point number between 0 and 1, inclusive.
If it is not provided,
then a default of 0.3 is used.
The number of bootstrap replicates to use for estimating the p-values
can be specified with ``-b/--boot-reps``.
Generally, higher repetitions increases accuracy,
A deault of 1000 is used to provide a balance between speed and accuracy.

Many calculations are dependent on knowing where certain metadata is stored.
Namely, the experimental conditions (specified with ``--group``),
the compartment of origin (specified with ``--compartment``),
the sample ID (specified with ``--sample-id``),
and the lipidomics mode (specifed with ``--mode``).
If these are not passed,
then they default to "Group", "Compartment", "SampleID", and "Mode" respectively.

We also have to know how many rows of metadata there are.
This is specified with ``--n-rows-metadata``,
and defaults to 11 if not given.

The error-normalised fold change (ENFC) calculation must know the labels for
experimental and control group.
Without this knowledge,
the concept of fold change is meaningless.
To specify, pass ``--control control``.
Every condition specified in ``Group`` will then be divided by ``control``
to calculate the ENFC for all conditions.

Finally,
all options *can be* passed in an config file.
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
    description="Lipid Traffic Analysis",
    allow_abbrev=False,
    add_config_file_help=True,
    default_config_files=["lta_conf.txt"],
    config_arg_is_required=False,
    ignore_unknown_config_file_keys=True,
    formatter_class=configargparse.ArgumentDefaultsRawHelpFormatter,
)

lta_parser.add_argument(
    "-c",
    "--config",
    required=False,
    is_config_file=True,
    help="Config file location.",
)

lta_parser.add_argument(
    "file",
    type=Path,
    help="Location of the input data csv file.",
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
    default=0.3,
    help="The '0' threshold",
)

lta_parser.add_argument(
    "-b",
    "--boot-reps",
    type=int,
    default=1000,
    help="Number of bootstrap repetitions",
)

lta_parser.add_argument(
    "-n",
    "--n-rows-metadata",
    type=int,
    default=11,
    help="Number of rows in column metadata",
)

lta_parser.add_argument(
    "--group",
    type=str,
    default="Group",
    help="Metadata label for experimental conditions",
)

lta_parser.add_argument(
    "--control",
    type=str,
    default="control",
    help="Control group for fold-change",
)

lta_parser.add_argument(
    "--compartment",
    type=str,
    default="Compartment",
    help="Metadata label for sample compartment",
)

lta_parser.add_argument(
    "--mode",
    type=str,
    default="Mode",
    help="Metadata label for lipidomics mode",
)

lta_parser.add_argument(
    "--sample-id",
    type=str,
    default="SampleID",
    help="Metadata label for Sample IDs",
)

lta_parser.add_argument(
    "-V",
    "--version",
    action="version",
    version=f"LTA v{__version__}",
    help="Display version information and exit.",
)

lta_parser.add_argument(
    "-v",
    "--verbose",
    action="count",
    default=0,
    help="Increase verbosity.",
)

lta_parser.add_argument(
    "-l",
    "--logfile",
    action="append",
    help="Location of logfile. May also be 'term' for Std.Out.",
)

lta_parser.set_defaults(func=run)
