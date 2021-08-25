# -*- coding: utf-8 -*-
"""A dataclass that allows for an object oriented pipeline."""
import itertools
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple

import pandas as pd

import lta.helpers.data_handling as dh
import lta.helpers.jaccard as jac

idx = pd.IndexSlice


@dataclass
class Pipeline:
    """The Lipid Trafficking Analysis pipeline.

    Attributes
    ----------
    file : Path
        The path to the combined data input file.
    output : Path
        Where to save the results.
    level : str
        Metadata location of experimental conditions
    tissue : str
        Metadata location of sample tissue compartment
    mode : str
        Metadata location of lipidomics mode
    thresh : float
        The fraction of samples that are 0 above which a lipid will be called 0 for a tissue.
    n : int
        Number of bootstrap replicates.
    """

    file: Path
    output: Path
    level: str
    tissue: str
    mode: str
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
        RuntimeError
            If there is no data in self.folder.
        """
        try:
            data = dh.construct_df(
                self.file,
                index_names=["Lipid", "Category", "m/z"],
                column_names=[
                    "Mode",
                    "Sample",
                    "Phenotype",
                    "Generation",
                    "Tissue",
                    "Handling",
                ],
                index_col=[0, 1, 2],
                header=list(range(2, 8)),
                skiprows=[8, 9, 10, 11],
            ).pipe(
                lambda x: x.loc[:, x.any()]
            )  # Drop all-0 samples
        except FileNotFoundError:
            print(f"{self.file} does not exist.")
            raise
        except IsADirectoryError:
            print(f"{self.file} is a directory.")
            raise
        else:
            if data.shape[0] == 0:
                raise RuntimeError(f"{self.file} contains no data.")
        self.binary = {
            group: dh.not_zero(
                df,
                axis="columns",
                level=self.level,
                tissue=self.tissue,
                thresh=self.thresh,
            )
            for group, df in data.groupby(axis="columns", level=self.mode)
        }
        self.filtered = {
            group: df.loc[self.binary[group].index, :]
            for group, df in data.groupby(axis="columns", level=self.mode)
        }
        self.output.mkdir(exist_ok=True, parents=True)

    def _calculate_enfc(
        self, order: Optional[Tuple[str, str]] = None
    ) -> Dict[str, pd.DataFrame]:
        """Calculate error-normalised fold change.

        Calculates the ENFC for each tissue across modes.
        There are 2 outputs.
        The first is the raw ENFC output.
        The second is the mean and standard deviation of the ENFC,
        grouped by lipid Category, for each tissue independently.
        Empty/NaN values means that the lipid or category was a "0".

        Parameters
        ----------
        order : Tuple[str, str]
            The experimental group labels.
            logfc fill be ``order[0] / order[1]``.

        Returns
        -------
        Dict[str, pd.DataFrame]
            Key is mode, value is the ENFC data
        """
        enfc = {
            mode: df.groupby(axis="columns", level=self.tissue).agg(
                dh.enfc,
                axis="columns",
                level=self.level,
                order=order,
            )
            for mode, df in self.filtered.items()
        }
        for mode, df in enfc.items():
            df.droplevel(["Category", "m/z"]).to_csv(
                self.output / f"enfc_{mode}_all_tissues.csv"
            )
            df.groupby(axis="rows", level="Category").agg(["mean", "std"]).to_csv(
                self.output / f"enfc_{mode}_grouped_all_tissues.csv"
            )
        return enfc

    def _get_a_lipids(self) -> Dict[str, pd.DataFrame]:
        """Extract A-lipids from the dataset.

        Any tissue where more than self.thresh of the samples are 0
        is considered a total 0 for that lipid.
        Lipids that are non-0 for all tissues in any Phenotype
        are considered A-lipids.

        Returns
        -------
        Dict[str, pd.DataFrame]
            Key is mode, value is table of A-lipids
        """
        results = {
            mode: (
                df.groupby(axis="columns", level=self.level)
                .all()
                .pipe(lambda x: x.loc[x.any(axis="columns"), :])
            )
            for mode, df in self.binary.items()
        }
        for mode, data in results.items():
            data.droplevel(["Category", "m/z"]).to_csv(
                self.output / f"a_lipids_{mode}.csv"
            )
            data.groupby(axis="rows", level="Category").sum().to_csv(
                self.output / f"a_lipids_{mode}_counts.csv"
            )
        return results

    def _get_b_lipids(self, picky: bool = True) -> Dict[str, pd.DataFrame]:
        """Extract B-lipids from the dataset.

        Any tissue where more than self.thresh of the samples are 0
        is considered a total 0 for that lipid.
        Lipids that are non-0 for any pair of tissues within any Phenotype
        are considered B-lipids.

        Notes
        -----
        By definition,
        all A-lipids will also be B-lipids for every pair of tissues.
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
            Keys are the tissue pair and mode.
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
            print("You must find A-lipids before B-lipids.")
            raise
        else:
            # This assumes that self.binary and a_lip will have the same keys
            # Which is definitely True
            if picky:
                data = {
                    mode: df.drop(index=a_lip[mode]) for mode, df in self.binary.items()
                }
                subtype = "p"
            else:
                data = {
                    mode: df.loc[a_lip[mode], :] for mode, df in self.binary.items()
                }
                subtype = "c"

        results = {}
        for mode, df in data.items():
            tissues = df.columns.get_level_values(self.tissue)
            pairs = itertools.combinations(tissues.unique(), 2)
            for group in pairs:
                unified = (
                    df.loc[:, tissues.isin(group)]
                    .groupby(axis="columns", level=self.level)
                    .all()
                    .pipe(lambda x: x.loc[x.any(axis="columns"), :])
                )
                pairing = "_".join([x.upper() for x in group])
                unified.droplevel(["Category", "m/z"]).to_csv(
                    self.output / f"b{subtype}_lipids_{pairing}_{mode}.csv"
                )
                unified.groupby(axis="rows", level="Category").sum().to_csv(
                    self.output / f"b{subtype}_lipids_{pairing}_{mode}_counts.csv"
                )
                results[f"{pairing}_{mode}"] = unified
        return results

    def _get_n_lipids(self, n: int) -> Dict[str, pd.DataFrame]:
        r"""Extract N-lipids from the dataset.

        Any tissue where more than self.thresh of the samples are 0
        is considered a total 0 for that lipid.
        Lipids that are non-0 for ``n`` tissues in any Phenotype
        are considered N-lipids.

        Notes
        -----
        For historical consistency,
        N1-lipids (*ie* those found in only 1 tissue) are called U-lipids
        as they are **U**\nique.
        Also N2-lipids are not the same as B-lipids.
        A B-lipid could occur in multiple pairs of tissue,
        while N2-lipids must only occur in 1.

        Parameters
        ----------
        n : int
            The number of tissues to limit the search to

        Returns
        -------
        Dict[str, pd.DataFrame]
            Keys are the tissue group and mode.
            Values are the table of N-lipids for that grouping.
        """
        results = {}
        for mode, df in self.binary.items():
            tissues = df.columns.get_level_values(self.tissue)
            # Mask required to prevent dropping levels
            # The initial check must be done with all tissues (only n)...
            mask = (
                df.groupby(axis="columns", level=self.tissue).any().sum(axis="columns")
                == n
            )

            data = [
                (group, df.loc[mask, tissues.isin(group)])
                for group in itertools.combinations(tissues.unique(), n)
            ]
            # ...which necessitates a second check to drop those that are not
            # Again, mask necessary for keeping info
            # Also, we only care for groups with lipids
            masks = [
                df.groupby(axis="columns", level=self.tissue).any().sum(axis="columns")
                == n
                for _, df in data
            ]
            data = [
                (group, df.loc[mask, :].groupby(axis="columns", level=self.level).all())
                for (group, df), mask in zip(data, masks)
                if mask.sum() != 0
            ]
            for (tissues, df) in data:
                n_type = "u" if n == 1 else f"n{n}"
                group = "_".join([x.upper() for x in tissues])
                df.droplevel(["Category", "m/z"]).to_csv(
                    self.output / f"{n_type}_lipids_{group}_{mode}.csv"
                )
                df.groupby(axis="rows", level="Category").sum().to_csv(
                    self.output / f"{n_type}_lipids_{group}_{mode}_counts.csv"
                )
                results[f"{group}_{mode}"] = df
        return results

    def _jaccard(self, data: Dict[str, pd.DataFrame], lipid_group: str) -> None:
        """Calculate jaccard distances and p-values.

        This takes a dictionary of data.
        As the output of each group of lipids will be structured as such,
        it should be called per lipid group.

        Notes
        -----
        The P-values are calculated using a bootstrap approach on a centered Jaccard similarity.
        Since Jaccard distance is simply 1 - Jaccard similarity,
        The P-value for similarity may be taken as the P-value for distance, as well.

        Parameters
        ----------
        data : Dict[str, pd.DataFrame]
            A dictionary of modes and lipid data
        lipid_group : str
            The class of lipids analysed
        """
        for mode, lipids in data.items():
            if len(lipids) == 0:
                # Overwrite if data is empty
                (self.output / f"{lipid_group}_{mode}_jaccard.csv").write_text("")
            else:
                # Write if data exists
                sim = lipids.groupby(axis="rows", level="Category").apply(
                    lambda df: jac.bootstrap(df.iloc[:, 0], df.iloc[:, 1], n=self.n)
                )
                dist = pd.DataFrame(
                    sim.to_list(), index=sim.index, columns=["J_dist", "p-val"]
                )
                # Convert from similarity to distance
                dist["J_dist"] = 1 - dist["J_dist"]
                dist.to_csv(self.output / f"{lipid_group}_{mode}_jaccard.csv")

    def run(self, order: Tuple[str, str]) -> None:
        """Run the full LTA pipeline.

        This:

        #. Calculates error-normalised fold change
        #. Finds A-lipids and Jaccard distances.
        #. Finds U-lipids and Jaccard distances.
        #. Finds B-lipids (both picky and consistent) and Jaccard distances.
        #. Finds N2-lipids and Jaccard distances.

        Parameters
        ----------
        order : Tuple[str, str]
            The experimental group labels.
            logfc fill be ``order[0] / order[1]``.
        """
        self.enfc = self._calculate_enfc(order)

        self.a_lipids = self._get_a_lipids()
        self._jaccard(self.a_lipids, "a_lipids")

        self.u_lipids = self._get_n_lipids(1)
        self._jaccard(self.u_lipids, "u_lipids")

        self.bc_lipids = self._get_b_lipids(picky=False)
        self.bp_lipids = self._get_b_lipids(picky=True)
        self._jaccard(self.bc_lipids, "bc_lipids")
        self._jaccard(self.bp_lipids, "bp_lipids")

        self.n2_lipids = self._get_n_lipids(2)
        self._jaccard(self.n2_lipids, "n2_lipids")
