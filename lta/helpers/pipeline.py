# -*- coding: utf-8 -*-
"""A dataclass that allows for an object oriented pipeline."""
import itertools
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import pandas as pd

import lta.helpers.data_handling as dh
import lta.helpers.jaccard as jac

logger = logging.getLogger(__name__)


@dataclass
class Pipeline:
    """The Lipid Traffic Analysis pipeline.

    Attributes
    ----------
    file : Path
        The path to the combined data input file.
    output : Path
        Where to save the results.
    n_rows_metadata : int
        The number of rows to treat as column metadata.
        As Python is 0-indexed, passing ``11`` will read in rows ``0-10``.
    level : str
        Metadata location of experimental conditions.
    control : str
        Value within self.level that represents the control condition.
    compartment : str
        Metadata location of sample tissue compartment.
    mode : str
        Metadata location of lipidomics mode.
    sample_id : str
        Metadata location of sample IDs.
    thresh : float
        The fraction of samples that are 0 above which a lipid will be called 0 for a compartment.
    n : int
        Number of bootstrap replicates.
    """

    file: Path
    output: Path
    n_rows_metadata: int
    level: str
    control: str
    compartment: str
    mode: str
    sample_id: str
    thresh: float
    n: int

    def __post_init__(self) -> None:
        """Post-process parameters.

        The magic of DataClasses!
        The post-init method allows for much of the processing normally required.
        Several things happen here.
        The file is read into a dataframe,
        which is split by ``Mode``,
        and stored twice as binary data (for Switch Analysis)
        and filtered counts (for ENFC Analysis).
        Any sample which contains all 0-values is dropped.
        Should the file not exist,
        not contain any data,
        or be a directory,
        then the appropriate errors are logged.
        Also, output folder is created if it does not exist already.

        Raises
        ------
        FileNotFoundError
            If self.file does not exist.
        IsADirectoryError
            If self.file is a directory.
        pd.errors.EmptyDataError
            If there is no data in self.file.
        """
        try:
            logger.debug(f"Reading data from {self.file}...")
            data = dh.construct_df(
                self.file,
                self.n_rows_metadata,
                [self.mode, self.level, self.compartment, self.sample_id],
                index_names=["Lipid", "Category", "m/z"],
                index_col=[0, 1, 2],
                header=None,
            ).pipe(
                lambda x: x.loc[:, x.any()]
            )  # Drop all-0 samples
        except FileNotFoundError:
            logger.exception(f"{self.file} does not exist. A full traceback follows...")
            raise
        except IsADirectoryError:
            logger.exception(f"{self.file} is a directory. A full traceback follows...")
            raise
        except pd.errors.EmptyDataError:
            logger.exception(
                f"{self.file} contains no data. A full traceback follows..."
            )
            raise
        logger.debug("Binarizing data...")
        self.binary = {
            group: dh.not_zero(
                df,
                axis="columns",
                level=self.level,
                compartment=self.compartment,
                thresh=self.thresh,
            )
            for group, df in data.groupby(axis="columns", level=self.mode)
        }
        logger.debug("Filtering data...")
        self.filtered = {
            group: df.loc[self.binary[group].index, :]
            for group, df in data.groupby(axis="columns", level=self.mode)
        }
        Path(self.output, "enfc").mkdir(exist_ok=True, parents=True)
        Path(self.output, "jaccard").mkdir(exist_ok=True, parents=True)

        conditions = [
            df.columns.get_level_values(self.level).unique()
            for df in self.filtered.values()
        ]
        self.conditions = [
            val for mode in conditions for val in mode if val != self.control
        ]

    def _calculate_enfc(self) -> Dict[str, Dict[str, pd.DataFrame]]:
        """Calculate error-normalised fold change.

        Calculates the ENFC for each compartment across modes.
        For fold change to be meaningful,
        order must be specified.
        This will report fold-change as
        ``condition / self.control`` for all conditions
        except control within self.value.

        Returns
        -------
        Dict[str, Dict[str, pd.DataFrame]]
            Top level key is the experimental condition,
            mapped to a dictionary of modes and ENFC results
        """
        logger.info("Calculating ENFC...")
        enfc = {
            group: {
                mode: df.groupby(axis="columns", level=self.compartment).agg(
                    dh.enfc,
                    axis="columns",
                    level=self.level,
                    order=(group, self.control),
                )
                for mode, df in self.filtered.items()
            }
            for group in self.conditions
        }
        return enfc

    def _get_a_lipids(self) -> Dict[str, pd.DataFrame]:
        """Extract A-lipids from the dataset.

        Any compartment where more than self.thresh of the samples are 0
        is considered a total 0 for that lipid.
        Lipids that are non-0 for all compartments in any Phenotype
        are considered A-lipids.

        Returns
        -------
        Dict[str, pd.DataFrame]
            Key is mode, value is table of A-lipids
        """
        logger.info("Calculating A-lipids...")
        results = {
            f"a_{mode}": (
                df.groupby(axis="columns", level=self.level)
                .all()
                .pipe(lambda x: x.loc[x.any(axis="columns"), :])
            )
            for mode, df in self.binary.items()
        }
        return results

    def _get_b_lipids(self, picky: bool = True) -> Dict[str, pd.DataFrame]:
        """Extract B-lipids from the dataset.

        Any compartment where more than self.thresh of the samples are 0
        is considered a total 0 for that lipid.
        Lipids that are non-0 for any pair of compartments within any Phenotype
        are considered B-lipids.

        Notes
        -----
        By definition,
        all A-lipids will also be B-lipids for every pair of compartments.
        These are referred to as B-consistent,
        or Bc for short.
        Those B-lipids that are not A-lipids are also known as B-picky,
        or Bp for short.
        Which set is calculated is controlled by the boolean flag ``picky``.

        Parameters
        ----------
        picky : bool
            default=True
            If true, do **not** consider lipids that are also A-lipids

        Returns
        -------
        Dict[str, pd.DataFrame]
            Keys are the compartment pair and mode.
            Values are the table of B-lipids for that grouping.

        Raises
        ------
        AttributeError
            If A-lipids have not been previously calculated
        """
        # drop or keep a-lipids, depending on picky
        try:
            a_lip = {mode: df.index for mode, df in self.a_lipids.items()}
        except AttributeError:
            logger.exception("You must find A-lipids before B-lipids.")
            raise
        else:
            # This assumes that self.binary and a_lip will have the same keys
            # Which is definitely True
            if picky:
                data = {
                    mode: df.drop(index=a_lip[f"a_{mode}"])
                    for mode, df in self.binary.items()
                }
                subtype = "p"
            else:
                data = {
                    mode: df.loc[a_lip[f"a_{mode}"], :]
                    for mode, df in self.binary.items()
                }
                subtype = "c"

        logger.info(f"Calculating B{subtype}-lipids...")
        results = {}
        for mode, df in data.items():
            logger.debug(f"Calculating B{subtype}-lipids for {mode}...")
            compartments = df.columns.get_level_values(self.compartment)
            pairs = itertools.combinations(compartments.unique(), 2)
            for group in pairs:
                logger.debug(f"Calculating B{subtype}-lipids for {group}...")
                unified = (
                    df.loc[:, compartments.isin(group)]
                    .groupby(axis="columns", level=self.level)
                    .all()
                    .pipe(lambda x: x.loc[x.any(axis="columns"), :])
                )
                pairing = "_".join([x.upper() for x in group])
                results[f"b{subtype}_{pairing}_{mode}"] = unified
        return results

    def _get_n_lipids(self, n: int) -> Dict[str, pd.DataFrame]:
        r"""Extract N-lipids from the dataset.

        Any compartment where more than self.thresh of the samples are 0
        is considered a total 0 for that lipid.
        Lipids that are non-0 for ``n`` compartments in any Phenotype
        are considered N-lipids.

        Notes
        -----
        For historical consistency,
        N1-lipids (*ie* those found in only 1 compartment) are called U-lipids
        as they are **U**\nique.
        Also N2-lipids are not the same as B-lipids.
        A B-lipid could occur in multiple pairs of compartment,
        while N2-lipids must only occur in 1.

        Parameters
        ----------
        n : int
            The number of compartments to limit the search to

        Returns
        -------
        Dict[str, pd.DataFrame]
            Keys are the compartment group and mode.
            Values are the table of N-lipids for that grouping.
        """
        logger.info(f"Calculating N{n}-lipids...")
        results = {}
        for mode, df in self.binary.items():
            logger.debug(f"Calculating N{n}-lipids for {mode}...")
            compartments = df.columns.get_level_values(self.compartment)
            # Mask required to prevent dropping levels
            # The initial check must be done with all compartments (only n)...
            mask = (
                df.groupby(axis="columns", level=self.compartment)
                .any()
                .sum(axis="columns")
                == n
            )

            data = [
                (group, df.loc[mask, compartments.isin(group)])
                for group in itertools.combinations(compartments.unique(), n)
            ]
            logger.debug(
                f"N{n} compartment groups before filtering: {[group for group, _ in data]}"
            )
            # ...which necessitates a second check to drop those that are not
            # Again, mask necessary for keeping info
            # Also, we only care for groups with lipids
            masks = [
                df.groupby(axis="columns", level=self.compartment)
                .any()
                .sum(axis="columns")
                == n
                for _, df in data
            ]
            data = [
                (group, df.loc[mask, :].groupby(axis="columns", level=self.level).all())
                for (group, df), mask in zip(data, masks)
                if mask.sum() != 0
            ]
            logger.debug(
                f"N{n} compartment groups after filtering: {[group for group, _ in data]}"
            )
            for (compartments, df) in data:
                n_type = "u" if n == 1 else f"n{n}"
                group = "_".join([x.upper() for x in compartments])
                results[f"{n_type}_{group}_{mode}"] = df
        return results

    def _jaccard(
        self, data: Dict[str, pd.DataFrame], group: str
    ) -> Dict[str, Dict[str, pd.DataFrame]]:
        """Calculate jaccard similarity and p-values.

        This takes a dictionary of data.
        As the output of each group of lipids will be structured as such,
        it should be called per lipid group.

        Notes
        -----
        The P-values are calculated using a bootstrap approach on a centered Jaccard similarity.

        Parameters
        ----------
        data : Dict[str, pd.DataFrame]
            A dictionary of modes and lipid data
        group : str
            Which lipids are being checke.
            This is used by logging only.

        Returns
        -------
        Dict[str, Dict[str, pd.DataFrame]]
            Keys are the compartment group and mode.
            Values are the table of Jaccard similarity and p-values.
        """
        logger.info(f"Calculating Jaccard similarity for {group}...")
        jaccard = {
            group: {
                mode: lipids.loc[:, [group, self.control]]
                .pipe(lambda df: df.loc[df.sum(axis=1) != 0, :])
                .groupby(axis="index", level="Category")
                .apply(
                    lambda x: jac.bootstrap(
                        x.loc[:, group], x.loc[:, self.control], n=self.n
                    )
                )
                for mode, lipids in data.items()
            }
            for group in self.conditions
        }
        return jaccard

    def run(self) -> None:
        """Run the full LTA pipeline.

        This:

        #. Calculates error-normalised fold change for all conditions relatve to control
        #. Finds A-lipids and Jaccard distances.
        #. Finds U-lipids and Jaccard distances.
        #. Finds B-lipids (both picky and consistent) and Jaccard distances.
        #. Finds N2-lipids and Jaccard distances.
        #. Writes combined results.
        """
        logger.debug("Generating ENFC summary files...")
        self.enfcs = self._calculate_enfc()
        for group, data in self.enfcs.items():
            pd.concat(data, axis="columns").to_csv(
                self.output
                / "enfc"
                / f"{group}_by_{self.control}_individual_lipids.csv"
            )

        logger.debug("Generating class ENFC summary files...")
        self.filtered = {
            mode: df.groupby(axis="index", level="Category").sum()
            for mode, df in self.filtered.items()
        }
        self.enfcs = self._calculate_enfc()
        for group, data in self.enfcs.items():
            pd.concat(data, axis="columns").to_csv(
                self.output / "enfc" / f"{group}_by_{self.control}_lipid_classes.csv"
            )

        self.a_lipids = self._get_a_lipids()
        self.a_jaccard = self._jaccard(self.a_lipids, "A-lipids")

        self.u_lipids = self._get_n_lipids(1)
        self.u_jaccard = self._jaccard(self.u_lipids, "U-lipids")

        self.bc_lipids = self._get_b_lipids(picky=False)
        self.bc_jaccard = self._jaccard(self.bc_lipids, "Bc-lipids")

        self.bp_lipids = self._get_b_lipids(picky=True)
        self.bp_jaccard = self._jaccard(self.bp_lipids, "Bp-lipids")

        self.n2_lipids = self._get_n_lipids(2)
        self.n2_jaccard = self._jaccard(self.n2_lipids, "N2-lipids")

        logger.debug("Generating Switch Analysis (lipid-type) summary files...")
        summary = pd.concat(
            {
                **self.a_lipids,
                **self.bc_lipids,
                **self.bp_lipids,
                **self.n2_lipids,
                **self.u_lipids,
            },
            axis="columns",
        ).fillna(False)
        summary.columns.names = ["type_compartment_mode", "Phenotype"]
        summary.to_csv(self.output / "switch_individual_lipids.csv")
        summary.groupby(axis="index", level="Category").sum().to_csv(
            self.output / "switch_lipid_classes.csv"
        )

        logger.debug("Generating Jaccard distance summary files...")
        for group in self.conditions:
            jaccard = pd.concat(
                {
                    **self.a_jaccard[group],
                    **self.bc_jaccard[group],
                    **self.bp_jaccard[group],
                    **self.n2_jaccard[group],
                    **self.u_jaccard[group],
                },
                axis="columns",
            )
            jaccard.columns.names = ["type_compartment_mode", "Metrics"]
            jaccard.to_csv(
                self.output
                / "jaccard"
                / f"{group}_to_{self.control}_jaccard_similarity.csv"
            )
