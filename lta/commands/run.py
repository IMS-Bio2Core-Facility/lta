# -*- coding: utf-8 -*-
"""A simple sample function for the CLI."""
import logging

import configargparse

from lta.helpers.pipeline import Pipeline

logger = logging.getLogger(__name__)


def run(args: configargparse.Namespace) -> None:
    """Initialise and run the LTA pipeline.

    This function constructs a ``lta.helpers.pipeline.Pipeline`` instance from
    the ``configargparser.Namespace``,
    and then calls the ``run`` method.
    Nothing more, nothing less.
    The rest of the magis is handled by the pipeline.

    Parameters
    ----------
    args: configargparse.Namespace
        The passed args.
    """
    logger.debug("Instantiating pipeline instance.")
    pl = Pipeline(
        args.file,
        args.output,
        args.phenotype,
        args.tissue,
        args.mode,
        args.threshold,
        args.boot_reps,
    )
    logger.debug("Running pipeline.")
    pl.run(args.order)
