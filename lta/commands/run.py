# -*- coding: utf-8 -*-
"""A simple sample function for the CLI."""
import argparse

from lta.helpers.pipeline import Pipeline


def run(args: argparse.Namespace) -> None:
    """Initialise and run the LTA pipeline.

    This function constructs a ``lta.helpers.pipeline.Pipeline`` instance from
    the ``argparser.Namespace``,
    and then calls the ``run`` method.
    Nothing more, nothing less.
    The rest of the magis is handled by the pipeline.

    Parameters
    ----------
    args: argparse.Namespace
        The passed args.
    """
    pl = Pipeline(
        args.file,
        args.output,
        args.phenotype,
        args.tissue,
        args.mode,
        args.threshold,
        args.boot_reps,
    )
    pl.run(args.order)
