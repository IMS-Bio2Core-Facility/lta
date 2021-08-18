# -*- coding: utf-8 -*-
"""A dataclass that allows for an object oriented pipeline."""
import itertools
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import pandas as pd

import lta.helpers.data_handling as dh
import lta.helpers.jaccard as jac


@dataclass
class Pipeline:
    """The Lipid Trafficking Analysis pipeline.

    Attributes
    ----------
    folder : Path
        The directory containing the data.
    output : Path
        Where to save the results.
    thresh : float
        The fraction of samples that are 0 above which a lipid will be called 0 for a tissue.
    n : int
        Number of bootstrap replicates.
    """

    folder: Path
    output: Path
    thresh: float
    n: int

    def __post_init__(self) -> None:
        """Post-process parameters.

        The magic of DataClasses!
        The post-init method allows for much of the processing normally required.
        Several things happen here.
        The contents of folder are read into dataframes.
        Should the folder not exist,
        or not be a directory,
        then the appropriate errors are logged.
        Also, output is created if it does not exist already.
        Finally, the modes are extracted from the metadata.

        Raises
        ------
        FileNotFoundError
            If self.folder does not exist.
        NotADirectoryError
            If self.folder is not a directory.
        RuntimeError
            If there is no data in self.folder.
        """
        try:
            frames: List[pd.DataFrame] = [
                dh.not_zero(
                    dh.construct_df(
                        file,
                        index_names=["Lipid", "Category", "m/z"],
                        column_names=[
                            "Sample",
                            "Phenotype",
                            "Generation",
                            "Tissue",
                            "Handling",
                            "Mode",
                        ],
                        index_col=[0, 1, 2],
                        header=list(range(3, 9)),
                        skiprows=[9, 10, 11],
                    ),
                    axis="columns",
                    level="Phenotype",
                    thresh=self.thresh,
                    drop=["Sample"],
                )
                for file in self.folder.iterdir()
            ]
        except FileNotFoundError:
            print(f"{self.folder} does not exist.")
            raise
        except NotADirectoryError:
            print(f"{self.folder} is not directory.")
            raise
        else:
            if len(frames) == 0:
                raise RuntimeError(f"{self.folder} contains no data.")
        self.data = dh.split_data(frames, axis="columns", level="Mode")
        self.output.mkdir(exist_ok=True, parents=True)

    def _get_a_lipids(self, level: str) -> None:
        """Extract A-lipids from the dataset.

        Any tissue where more than self.thresh of the samples are 0
        is considered a total 0 for that lipid.
        Lipids that are non-0 for all tissues in any Phenotype
        are considered A-lipids.

        Parameters
        ----------
        level : str
            The column metadata level that contains the experimental groups
        """
        self.a_lipids = {
            mode: pd.concat(frames, join="inner", axis="columns")
            .groupby(axis="columns", level=level)
            .all()
            .pipe(lambda x: x.loc[x.any(axis="columns"), :])
            for mode, frames in self.data.items()
        }
        for mode, data in self.a_lipids.items():
            data.droplevel(["Category", "m/z"]).to_csv(
                self.output / f"a_lipids_{mode}.csv"
            )
            data.groupby(axis="rows", level="Category").sum().to_csv(
                self.output / f"a_lipids_{mode}_counts.csv"
            )

    def _get_b_lipids(
        self, tissue: str, level: str, picky: bool = True
    ) -> Dict[str, pd.DataFrame]:
        """Extract B-lipids from the dataset.

        Any tissue where more than self.thresh of the samples are 0
        is considered a total 0 for that lipid.
        Lipids that are non-0 for any pair of tissues within any Phenotype
        are considered B-lipids.

        Parameters
        ----------
        tissue : str
            The column metadata containing sample tissue
        level : str
            The column metadata containing experimental groups
        picky : bool
            default=True
            If true, do **not** consider lipids that are also A-lipids

        Returns
        -------
        Dict[str, pd.DataFrame]
            Keys are groupings with the B-lipids for that set

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
            # This assumes that self.data and a_lip will have the same keys
            # Which is definitely True
            if picky:
                data = {
                    mode: [df.drop(index=idx) for df in self.data[mode]]
                    for mode, idx in a_lip.items()
                }
                subtype = "p"
            else:
                data = {
                    mode: [df.loc[idx, :] for df in self.data[mode]]
                    for mode, idx in a_lip.items()
                }
                subtype = "c"

        results = {}
        for mode, frames in data.items():
            pairs = itertools.combinations(frames, 2)
            for first, second in pairs:
                unified = first.join(second, how="inner")
                groups = unified.columns.get_level_values(tissue).unique()
                unified = (
                    unified.groupby(axis="columns", level=level)
                    .all()
                    .pipe(lambda x: x.loc[x.any(axis="columns"), :])
                )
                unified.droplevel(["Category", "m/z"]).to_csv(
                    self.output
                    / f"b{subtype}_lipids_{groups[0]}_{groups[1]}_{mode}.csv"
                )
                unified.groupby(axis="rows", level="Category").sum().to_csv(
                    self.output
                    / f"b{subtype}_lipids_{groups[0]}_{groups[1]}_{mode}_counts.csv"
                )
                results[f"{groups[0]}_{groups[1]}_{mode}"] = unified
        return results

    def _get_u_lipids(self, tissue: str) -> None:
        """Extract U-lipids from the dataset.

        Any tissue where more than self.thresh of the samples are 0
        is considered a total 0 for that lipid.
        Lipids that are non-0 for all tissues in any Phenotype
        are considered U-lipids.

        Parameters
        ----------
        tissue : str
            The column metadata containing sample tissue
        """
        self.u_lipids = {}
        for mode, frames in self.data.items():
            # This can be done with pipes, but its functional unreadable that way
            unified = pd.concat(frames, join="outer", axis="columns").fillna(False)
            u_mask = (
                unified.groupby(axis="columns", level=tissue).any().sum(axis="columns")
                == 1
            )
            unified = unified.loc[u_mask, :]
            data = [
                unified.xs(group, axis="columns", level=tissue, drop_level=False)
                for group in unified.columns.get_level_values(tissue).unique()
            ]
            data = [
                df.loc[df.any(axis="columns"), :].droplevel(
                    axis="columns", level=["Generation", "Handling", "Mode"]
                )
                for df in data
            ]
            for df in data:
                group = df.columns.get_level_values(tissue).unique()[0].upper()
                df.droplevel(["Category", "m/z"]).to_csv(
                    self.output / f"u_lipids_{group}_{mode}.csv"
                )
                df.groupby(axis="rows", level="Category").sum().to_csv(
                    self.output / f"u_lipids_{group}_{mode}_counts.csv"
                )
                self.u_lipids[f"{group}_{mode}"] = df

    def _jaccard(self, data: Dict[str, pd.DataFrame], lipid_group: str) -> None:
        """Calculate jaccard distances and p-values.

        This takes a dictionary of data. As the output of each group of lipids will be
        structured as such, if should be called per lipid group.

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

    def run(self, level: str, tissue: str) -> None:
        """Run the full LTA pipeline.

        This determines the various classes of lipids
        as well as the distance between the respective vectors.

        Parameters
        ----------
        tissue : str
            The column metadata containing sample tissue
        level : str
            The column metadata containing experimental groups
        """
        self._get_a_lipids(level)
        self._jaccard(self.a_lipids, "a_lipids")
        self._get_u_lipids(tissue)
        self._jaccard(self.u_lipids, "u_lipids")
        self.bc_lipids = self._get_b_lipids(tissue, level, picky=False)
        self.bp_lipids = self._get_b_lipids(tissue, level, picky=True)
        self._jaccard(self.bc_lipids, "bc_lipids")
        self._jaccard(self.bp_lipids, "bp_lipids")
