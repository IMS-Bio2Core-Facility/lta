# -*- coding: utf-8 -*-
"""A dataclass that allows for an object oriented pipeline."""
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set

import pandas as pd

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
                self._post_process(self._construct_df(file))
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
        self.data = self._split_data(self._get_modes(frames), frames)
        self.output.mkdir(exist_ok=True, parents=True)

    def _construct_df(self, file: Path) -> pd.DataFrame:
        """Construct a dataframe from the given path.

        This assumes several things about the structure of the data.
        First, that the first 11 rows contain the metadata.
        Second, that the metadata Sample, Phenotype, Generation, Tissue,
        Handling, and Mode are in rows 4 through 9, respectively
        Third, any empty row or column is not informative.
        Finally, the data should be a csv.

        Parameters
        ----------
        file : Path
            The path to the data file.

        Returns
        -------
        pd.DataFrame
            The created dataframe
        """
        counts: pd.DataFrame = pd.read_csv(
            file, index_col=[0, 1, 2], header=list(range(3, 9)), skiprows=[9, 10, 11]
        )
        counts = counts.dropna(axis="rows", how="all").dropna(axis="columns", how="all")
        counts.columns.names = [
            "Sample",
            "Phenotype",
            "Generation",
            "Tissue",
            "Handling",
            "Mode",
        ]
        counts.index.names = ["Lipid", "Category", "m/z"]
        return counts

    def _get_modes(self, frames: List[pd.DataFrame], level: str = "Mode") -> Set[str]:
        """Get the experimental modes.

        Given a list of dataframes, retrieve all uniques experimental modes.

        Parameters
        ----------
        frames : List[pd.DataFrame]
            The data to search
        level : str, default="Mode"  # noqa: DAR103
            The level containing the experimental modes.

        Returns
        -------
        Set[str]
            The unique experimental values
        """
        modes: Set[str] = set()
        modes = modes.union(
            *[df.columns.get_level_values(level).unique().tolist() for df in frames]
        )
        return modes

    def _split_data(
        self, modes: Set[str], frames: List[pd.DataFrame]
    ) -> Dict[str, List[pd.DataFrame]]:
        """Split data on mode.

        Creates a dictionary where each key is a unique experimental mode,
        and the values are lists of dataframes created with that experimental mode.

        Parameters
        ----------
        modes : Set[str]
            The experimental modes.
        frames : List[pd.DataFrame]
            The data to be sorted.

        Returns
        -------
        Dict[str, List[pd.DataFrame]]
            The sorted data.
        """
        data = {
            mode: [
                df
                for df in frames
                if df.columns.get_level_values("Mode").unique() == mode
            ]
            for mode in modes
        }
        return data

    def _post_process(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process data frame to boolean counts.

        All processing downstream is dependent on boolean data,
        so, to prevent duplicate calculations, the data is converted
        to this boolean form immediately after reading in.

        This method makes all the same assumptions that ``_construct_df``
        makes, and also assumes that the phenotype comparison occurs along
        the column metadata "Phenotype".

        Frustratingly, index levels are lost when grouping on a multiindex.
        To ensure it is correctly added back, the metadata are saved,
        then joined back onto the resultant boolean data frame.

        Parameters
        ----------
        df : pd.DataFrame
            The lipid data to convert to boolean.

        Returns
        -------
        pd.DataFrame
            The processed data.
        """
        metadata = df.columns.droplevel("Sample").unique()
        df = (
            (df == 0)
            .groupby(axis="columns", level="Phenotype")
            .transform(lambda x: x.sum() <= (self.thresh * len(x)))
            .groupby(axis="columns", level="Phenotype")
            .all()
            .pipe(lambda x: x.loc[x.any(axis="columns"), :])
        )
        df = df.transpose().join(pd.DataFrame(columns=metadata).transpose(), how="left")
        return df.transpose()

    def _get_a_lipids(self, level: str = "Phenotype") -> None:
        """Extract A-lipids from the dataset.

        Any tissue where more than self.thresh of the samples are 0
        is considered a total 0 for that lipid.
        Lipids that are non-0 for all tissues in any Phenotype
        are considered A-lipids.

        Parameters
        ----------
        level : str, default="Phenotype"  # noqa: DAR103
            Where the experimental conditions are located in the metadata
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

    def _jaccard(self, data: Dict[str, pd.DataFrame]) -> None:
        """Calculate jaccard distances and p-values.

        This takes a dictionary of data. As the output of each group of lipids will be
        structured as such, if should be called per lipid group.

        Parameters
        ----------
        data : Dict[str, pd.DataFrame]
            A dictionary of modes and lipid data
        """
        for mode, lipids in data.items():
            sim = lipids.groupby(axis="rows", level="Category").apply(
                lambda df: jac.bootstrap(df.iloc[:, 0], df.iloc[:, 1], n=self.n)
            )
            dist = pd.DataFrame(
                sim.to_list(), index=sim.index, columns=["J_dist", "p-val"]
            )
            # Convert from similarity to distance
            dist["J_dist"] = 1 - dist["J_dist"]
            dist.to_csv(self.output / f"a_lipids_{mode}_jaccard.csv")

    def run(self) -> None:
        """Run the full LTA pipeline.

        This determines the various classes of lipids
        as well as the distance between the respective vectors.
        """
        self._get_a_lipids()
        self._jaccard(self.a_lipids)
