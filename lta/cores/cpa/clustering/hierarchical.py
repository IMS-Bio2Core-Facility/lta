"""Hierarchical Clustering."""

import typing as t

import pandas as pd
import sklearn.cluster as sk_cl

# using sklearn Agglomerative Clustering
# https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html


class HierarchicalClustering:
    """
    A class to perform hierarchical clustering using scikit-learn's AgglomerativeClustering.

    Parameters
    ----------
    - number_clusters (int): The number of clusters to find. Default is 2.
    - linkage (str): The linkage criterion to use. One of {'ward', 'complete', 'average', 'single'}. Default is 'ward'.
    - metric (str or callable): The metric to use when calculating distance between instances in a feature array. Default is 'euclidean'.

    Methods
    -------
    - cluster(data: pd.DataFrame) -> t.List[int]: Performs hierarchical clustering on the provided data and returns the cluster labels.
    """

    def __init__(
        self,
        number_clusters: int = 2,
        linkage: t.Literal["ward", "complete", "average", "single"] = "ward",
        metric: t.Union[
            t.Literal["euclidean", "l1", "l2", "manhattan", "cosine", "precomputed"],
            t.Callable,
        ] = "euclidean",
    ) -> None:
        self._n_clusters = number_clusters
        self._linkage = linkage
        self._metric = metric

    def cluster(self, data: pd.DataFrame) -> t.List[int]:
        """
        Perform hierarchical clustering on the provided data.

        Parameters
        ----------
        data : pd.DataFrame
            The data to cluster.

        Returns
        -------
        - t.List[int]: The cluster labels.
        """
        ac = sk_cl.AgglomerativeClustering(
            n_clusters=self._n_clusters, linkage=self._linkage, metric=self._metric
        )
        return ac.fit_predict(data)
