"""Principal Component Analysis (PCA) Normalizer."""

import pandas as pd
import sklearn.decomposition as sk_dc

from lta.cores.cpa.normalizer.base import Normalizer


class PrincipalComponentAnalysis(Normalizer):
    """
    A class to perform normalization and dimensionality reduction using Principal Component Analysis (PCA).

    This class extends the Normalizer base class to first normalize the data and then apply PCA to reduce its dimensionality.

    Parameters
    ----------
    - output_dimensions (int): The number of principal components to keep. Default is 2.

    """

    def __init__(self, output_dimensions: int = 2) -> None:
        super().__init__()
        self._pca = sk_dc.PCA(n_components=output_dimensions)

    def normalize(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize the provided data and reduce its dimensionality using PCA.

        Parameters
        ----------
        data : pd.DataFrame
            The data to normalize and reduce dimensionality.

        Returns
        -------
        pd.DataFrame: The normalized and reduced data.
        """
        normalized = super().normalize(data)
        # reduce the dimensionality of the data
        d_principal = self._pca.fit_transform(normalized)
        return pd.DataFrame(d_principal, index=data.index)
