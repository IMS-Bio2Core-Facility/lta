import typing as t
import pandas as pd
import sklearn.cluster as sk_cl


# using sklearn's AgglomerativeClustering
# https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html


class HierarchicalClustering:
    def __init__(
        self,
        number_clusters: int = 2,
        linkage: t.Literal["ward", "complete", "average", "single"] = "ward",
        metric: (
            t.Literal["euclidean", "l1", "l2", "manhattan", "cosine", "precomputed"]
            | t.Callable
        ) = "euclidean",
    ):
        self._n_clusters = number_clusters
        self._linkage = linkage
        self._metric = metric

    def cluster(self, data: pd.DataFrame) -> t.List[int]:
        ac = sk_cl.AgglomerativeClustering(
            n_clusters=self._n_clusters, linkage=self._linkage, metric=self._metric
        )
        return ac.fit_predict(data)
