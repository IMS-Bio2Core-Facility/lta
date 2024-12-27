import pandas as pd
import sklearn.decomposition as sk_dc

from lta.cores.cpa.normalizer.base import Normalizer

class PrincipalComponentAnalysis(Normalizer):
    def __init__(self, output_dimensions: int = 2):
        super().__init__()
        self._pca = sk_dc.PCA(n_components=output_dimensions)

    def normalize(self, data: pd.DataFrame) -> pd.DataFrame:
        normalized = super().normalize(data)
        # reduce the dimensionality of the data
        d_principal = self._pca.fit_transform(normalized)
        return pd.DataFrame(d_principal, index=data.index)