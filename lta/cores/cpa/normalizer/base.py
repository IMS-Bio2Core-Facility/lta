import abc

import pandas as pd
import sklearn.discriminant_analysis as sk_da
import sklearn.preprocessing as sk_pre

class Normalizer(abc.ABC):
    def __init__(self):
        self._scaler = sk_da.StandardScaler()

    def normalize(self, data: pd.DataFrame) -> pd.DataFrame:
        # scale all features (columns) so that they become comparable
        d_scaled = self._scaler.fit_transform(data)
        # normalize the data so that it approximately follows a Gaussian distribution
        d_normalized = sk_pre.normalize(d_scaled)
        # return the normalized data as a DataFrame
        return pd.DataFrame(d_normalized, index=data.index)
