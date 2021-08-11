# -*- coding: utf-8 -*-
"""A dataclass that allows for an object oriented pipeline."""
from dataclasses import dataclass
from pathlib import Path
from typing import List, Set

import pandas as pd


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
    """

    folder: Path
    output: Path
    thresh: float

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
            self.data: List[pd.DataFrame] = [
                self._construct_df(file) for file in self.folder.iterdir()
            ]
        except FileNotFoundError:
            print(f"{self.folder} does not exist.")
            raise
        except NotADirectoryError:
            print(f"{self.folder} is not directory.")
            raise
        else:
            if len(self.data) == 0:
                raise RuntimeError(f"{self.folder} contains no data.")
        self.output.mkdir(exist_ok=True, parents=True)
        # Long-standing mypy type bug
        # See https://github.com/python/mypy/issues/2013
        self.modes: Set[str] = set()
        self.modes = self.modes.union(
            *[df.columns.get_level_values("Mode").unique().tolist() for df in self.data]
        )

    def _construct_df(self, file: Path) -> pd.DataFrame:
        """Construct a dataframe from the given path.

        This assumes several things about the structure of the data.
        First, that the first 11 rows contain the metadata.
        Second, that the names of the metadata are in column 2 because
        Third, the first 3 columns are the row metadata.
        Finally, the data should be a csv.

        Additionally, there is some agressive dropping of NaNs.
        I have pandas inconsistently read empty columns as full of NaNs
        rather than not reading them.
        It seems to be an artifact from the software the file was created with.
        To avoid this,
        these types of columns and rows are dropped.

        Parameters
        ----------
        file : Path
            The path to the data file.

        Returns
        -------
        pd.DataFrame
            The created dataframe
        """
        metadata: pd.DataFrame = pd.read_csv(file, nrows=11, index_col=2, header=None)
        metadata = (
            metadata.dropna(axis="columns", how="all")
            .dropna(axis="rows", how="all")
            .transpose()
        )

        counts: pd.DataFrame = pd.read_csv(file, skiprows=11, index_col=[0, 1, 2])
        counts = counts.loc[:, ~counts.columns.str.startswith("Unnamed")].dropna(
            axis="rows", how="all"
        )
        counts.columns = pd.MultiIndex.from_frame(metadata)
        return counts

    def _get_a_lipids(self) -> None:
        """Extract A-lipids from the dataset.

        Any tissue where more than self.thresh of the samples are 0
        is considered a total 0 for that lipid.
        Lipids that are non-0 for all tissues in any Phenotype
        are considered A-lipids.
        """
        for mode in self.modes:
            not_zeros = [
                (df == 0)
                .groupby(axis="columns", level="Phenotype")
                .transform(lambda x: x.sum() <= (self.thresh * len(x)))
                .groupby(axis="columns", level="Phenotype")
                .all()
                .pipe(lambda x: x.loc[x.any(axis="columns"), :])
                for df in self.data
                if df.columns.get_level_values("Mode").unique() == mode
            ]
            unified = (
                pd.concat(not_zeros, join="inner", axis="columns")
                .groupby(axis="columns", level="Phenotype")
                .all()
                .pipe(lambda x: x.loc[x.any(axis="columns"), :])
            )
            unified.droplevel(["Category", "m/z"]).to_csv(
                self.output / f"a_lipids_{mode}.csv"
            )
            unified.groupby(axis="rows", level="Category").sum().to_csv(
                self.output / f"a_lipids_{mode}_counts.csv"
            )

    def run(self) -> None:
        """Run the full LTA pipeline.

        This determines the various classes of lipids
        as well as the distance between the respective vectors.
        """
        self._get_a_lipids()
