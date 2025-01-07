"""Base class for normalizer."""

import pandas as pd
import sklearn.discriminant_analysis as sk_da
import sklearn.preprocessing as sk_pre


class Normalizer:
    """
    A base class for normalizing data.

    This class provides a template for normalizing data using scikit-learn's StandardScaler and normalize functions.
    """

    def __init__(self) -> None:
        self._scaler = sk_da.StandardScaler()

    def normalize(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize the provided data.

        Parameters
        ----------
        data : pd.DataFrame
            The data to normalize.

        Returns
        -------
        pd.DataFrame: The normalized data.
        """
        # scale all features (columns) so that they become comparable
        d_scaled = self._scaler.fit_transform(data)
        # normalize the data so that it approximately follows a Gaussian distribution
        d_normalized = sk_pre.normalize(d_scaled)
        # return the normalized data as a DataFrame
        return pd.DataFrame(d_normalized, index=data.index)
