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
    The rest of the magic is handled by the pipeline.

    Parameters
    ----------
    args: configargparse.Namespace
        The passed args.
    """
    logger.debug("Instantiating pipeline instance.")
    pl = Pipeline(
        args.file,
        args.output,
        args.n_rows_metadata,
        args.group,
        args.control,
        args.compartment,
        args.mode,
        args.sample_id,
        args.threshold,
        args.boot_reps,
    )
    logger.debug("Running pipeline.")
    pl.run()
