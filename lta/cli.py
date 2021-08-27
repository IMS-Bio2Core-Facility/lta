# -*- coding: utf-8 -*-
"""Provide entry point for CLI."""
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

import configargparse

from lta.parser import lta_parser


def main(args: Optional[configargparse.Namespace] = None) -> None:
    """Provide entry point for CLI.

    This also configures the logger to use for the run.

    Parameters
    ----------
    args : Optional[configargparse.Namespace]
        If not specified, then the command line inputs are read.
        This is the *intended* behaviour,
        as this option only exists to allow for testing.
    """
    if args is None:
        args = lta_parser.parse_args()

    # Configure logging
    now = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
    logs = Path("logs")
    logs.mkdir(parents=False, exist_ok=True)

    formatter = logging.Formatter(
        "{asctime} :: {levelname} :: {name} :: {message}", style="{"
    )
    handlers = [
        logging.FileHandler(logs / f"{now}.log"),
        logging.StreamHandler(),
    ]  # file future arg flag?
    for h in handlers:
        h.setLevel(logging.INFO)  # Change with arg flag
        h.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=handlers)  # Changer with arg flag
    logger = logging.getLogger(__name__)

    logger.info(
        f"Running LTA with the following parameters:\n{lta_parser.format_values()}"
    )
    args.func(args)
