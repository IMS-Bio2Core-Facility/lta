# -*- coding: utf-8 -*-
"""A simple sample function for the CLI."""
import argparse


def simple(args: argparse.Namespace) -> None:
    """Print some text.

    Print text passed to the CLI.

    Parameters
    ----------
    args: argparse.Namespace
        The passed args.
    """
    print(args.text)
