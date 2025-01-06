"""Tests for the normalizer class."""

import unittest

import pandas as pd

from lta.cores.cpa.normalizer.base import Normalizer


class TestNormalizerMethods(unittest.TestCase):
    """Unit tests for the Normalizer class."""

    def setUp(self) -> None:
        """Set up the test data and the Normalizer object."""
        self.data = pd.DataFrame(
            {
                "feature1": [1, 2, 3, 4, 5],
                "feature2": [5, 4, 3, 2, 1],
                "feature3": [2, 3, 4, 5, 6],
            }
        )
        self.normalizer = Normalizer()

    def test_normalize(self) -> None:
        """Test the normalize method."""
        normalized_data = self.normalizer.normalize(self.data)
        self.assertEqual(normalized_data.shape, self.data.shape)
        # Check if the mean of each column is approximately 0
        self.assertTrue((normalized_data.mean(axis=0).abs() < 1e-6).all())
        # Check if the standard deviation of each column is approximately 1
        self.assertTrue((normalized_data.std(axis=0).abs() - 1 < 1e-6).all())
