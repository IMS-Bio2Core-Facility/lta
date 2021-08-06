# -*- coding: utf-8 -*-
"""Provide entry point for CLI."""
import argparse
from typing import Optional

from lta.parser import lta_parser


def main(args: Optional[argparse.Namespace] = None) -> None:
    """Provide entry point for CLI.

    Parameters
    ----------
    args : Optional[argparse.Namespace]
        If not specified, then the command line inputs are read.
        This is the *intended* behaviour,
        as this option only exists to allow for testing.
    """
    if args is None:
        args = lta_parser.parse_args()
    args.func(args)
