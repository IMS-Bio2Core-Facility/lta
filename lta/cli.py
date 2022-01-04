# -*- coding: utf-8 -*-
"""Provide entry point for CLI."""
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, cast

import configargparse

from lta.parser import lta_parser


def main(args: Optional[configargparse.Namespace] = None) -> None:
    """Provide entry point for CLI.

    This also configures the logger to use for the run.
    The ``-v`` flag can be passed multiple times,
    increasing verbosity from errors to debug.
    Additionally,
    file handlers are set up for ``--logfile``,
    unless the passed file is ``term``,
    in which case a stream handler is used.

    Parameters
    ----------
    args : Optional[configargparse.Namespace]
        If not specified, then the command line inputs are read.
        This is the *intended* behaviour,
        as this option only exists to allow for testing.
    """
    if args is None:
        args = lta_parser.parse_args()

    # Get verbosity level
    verbosity = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG,
    }
    level = verbosity.get(args.verbose, logging.DEBUG)

    # Configure formatter
    formatter = logging.Formatter(
        "{asctime} :: {levelname} :: {name} :: {message}", style="{"
    )

    # Configure handlers
    # Append does not overwrite defaults...
    # Dashes are used instead of my usual colons for time,
    # As they are Windows incompatible.
    if not args.logfile:
        logs = Path("logs")
        logs.mkdir(parents=False, exist_ok=True)
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        args.logfile = [logs / f"{now}.log"]

    handlers = [
        cast(logging.Handler, logging.StreamHandler())
        if log == "term"
        else cast(logging.Handler, logging.FileHandler(log))
        for log in args.logfile
    ]
    for h in handlers:
        h.setLevel(level)
        h.setFormatter(formatter)

    # Configure root logger
    logging.basicConfig(level=level, handlers=handlers)
    logger = logging.getLogger(__name__)

    logger.log(
        45, f"Running LTA with the following parameters:\n{lta_parser.format_values()}"
    )
    args.func(args)
