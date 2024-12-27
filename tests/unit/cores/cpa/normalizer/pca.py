import unittest
import pandas as pd
from lta.cores.cpa.normalizer.pca import PrincipalComponentAnalysis


class TestPrincipalComponentAnalysis(unittest.TestCase):
    def setUp(self):
        self.output_dimensions = 2
        self.data = pd.DataFrame(
            {
                "feature1": [1, 2, 3, 4, 5],
                "feature2": [5, 4, 3, 2, 1],
                "feature3": [2, 3, 4, 5, 6],
            }
        )
        self.pca = PrincipalComponentAnalysis(output_dimensions=self.output_dimensions)

    def test_normalize(self):
        normalized_data = self.pca.normalize(self.data)
        self.assertEqual(
            normalized_data.shape, (self.data.shape[0], self.output_dimensions)
        )
        self.assertTrue((normalized_data.mean(axis=0).abs() < 1e-6).all())
        self.assertTrue((normalized_data.std(axis=0).abs() - 1 < 1e-6).all())
