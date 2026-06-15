"""Unit tests for Jaccard similarity helpers."""

import logging

import numpy as np
import pandas as pd
import pytest

from lta.helpers import jaccard


def b(*vals: int) -> np.ndarray:
    """Construct a 1-D boolean ndarray from integer literals."""
    return np.array(vals, dtype=bool)


# ---------------------------------------------------------------------------
# similarity
# ---------------------------------------------------------------------------


def test_similarity_identical_vectors() -> None:
    """Identical vectors should have similarity of 1."""
    x = b(1, 1, 0, 1)
    assert jaccard.similarity(x, x) == pytest.approx(1.0)


def test_similarity_disjoint_vectors() -> None:
    """Disjoint vectors should have similarity of 0."""
    x = b(1, 1, 0, 0)
    y = b(0, 0, 1, 1)
    assert jaccard.similarity(x, y) == pytest.approx(0.0)


def test_similarity_partial_overlap() -> None:
    """Vectors with partial overlap should return intersect/union."""
    x = b(1, 1, 1, 0)
    y = b(1, 1, 0, 1)
    # intersect=2, union=4 → 0.5
    assert jaccard.similarity(x, y) == pytest.approx(0.5)


def test_similarity_all_zeros_returns_nan() -> None:
    """All-zero vectors produce a zero denominator; result should be NaN."""
    x = b(0, 0, 0)
    y = b(0, 0, 0)
    result = jaccard.similarity(x, y)
    assert np.isnan(result)


def test_similarity_with_explicit_px_py() -> None:
    """Explicitly supplied px/py should be used instead of the sample mean."""
    x = b(1, 0, 1, 0)
    y = b(1, 0, 1, 0)
    result = jaccard.similarity(x, y, px=0.5, py=0.5)
    assert result == pytest.approx(1.0)


def test_similarity_centered() -> None:
    """Centered similarity should subtract the expected overlap under independence."""
    x = b(1, 1, 0, 0)
    y = b(1, 1, 0, 0)
    # j=1, px=py=0.5, denominator=0.75, centered = 1 - (0.25/0.75)
    expected = 1.0 - (0.25 / 0.75)
    assert jaccard.similarity(x, y, center=True) == pytest.approx(expected)


def test_similarity_raises_on_2d_input() -> None:
    """Non-1-D arrays should raise IndexError."""
    x = np.array([[True, False], [True, False]])
    y = np.array([[True, False], [True, False]])
    with pytest.raises(IndexError):
        jaccard.similarity(x, y)


def test_similarity_raises_on_length_mismatch() -> None:
    """Arrays of different lengths should raise IndexError."""
    with pytest.raises(IndexError):
        jaccard.similarity(b(1, 0), b(1, 0, 1))


def test_similarity_raises_on_non_boolean_dtype() -> None:
    """Integer arrays should raise TypeError."""
    x = np.array([1, 0, 1], dtype=int)
    y = np.array([1, 0, 1], dtype=int)
    with pytest.raises(TypeError):
        jaccard.similarity(x, y)


# ---------------------------------------------------------------------------
# distance
# ---------------------------------------------------------------------------


def test_distance_identical_vectors() -> None:
    """Identical vectors should have distance of 0."""
    x = b(1, 0, 1)
    assert jaccard.distance(x, x) == pytest.approx(0.0)


def test_distance_disjoint_vectors() -> None:
    """Disjoint vectors should have distance of 1."""
    x = b(1, 1, 0, 0)
    y = b(0, 0, 1, 1)
    assert jaccard.distance(x, y) == pytest.approx(1.0)


def test_distance_partial_overlap() -> None:
    """Distance should equal 1 minus the Jaccard similarity."""
    x = b(1, 1, 1, 0)
    y = b(1, 1, 0, 1)
    assert jaccard.distance(x, y) == pytest.approx(0.5)


def test_distance_with_explicit_px_py() -> None:
    """Explicit px/py should be forwarded to similarity correctly."""
    x = b(1, 0, 1, 0)
    y = b(1, 0, 1, 0)
    result = jaccard.distance(x, y, px=0.5, py=0.5)
    assert result == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# bootstrap
# ---------------------------------------------------------------------------


def test_bootstrap_returns_series_with_correct_index() -> None:
    """Bootstrap should return a Series with J-sim and p-val labels."""
    x = b(1, 0, 1, 0, 1, 0)
    y = b(1, 1, 0, 0, 1, 0)
    result = jaccard.bootstrap(x, y, seed=0)
    assert isinstance(result, pd.Series)
    assert list(result.index) == ["J-sim", "p-val"]


def test_bootstrap_p_value_in_range() -> None:
    """Bootstrap p-value should be in [0, 1]."""
    x = b(1, 0, 1, 0, 1, 0)
    y = b(1, 1, 0, 0, 1, 0)
    result = jaccard.bootstrap(x, y, n=200, seed=42)
    assert 0.0 <= result["p-val"] <= 1.0


def test_bootstrap_degenerate_all_ones(caplog: pytest.LogCaptureFixture) -> None:
    """All-ones vector should trigger the degenerate warning and return p-val=1."""
    x = b(1, 1, 1, 1)
    y = b(1, 0, 1, 0)
    with caplog.at_level(logging.WARNING, logger="lta.helpers.jaccard"):
        result = jaccard.bootstrap(x, y)
    assert result["p-val"] == pytest.approx(1.0)
    assert "degenerate" in caplog.text


def test_bootstrap_degenerate_all_zeros(caplog: pytest.LogCaptureFixture) -> None:
    """All-zeros vector should trigger the degenerate warning and return p-val=1."""
    x = b(0, 0, 0, 0)
    y = b(1, 0, 1, 0)
    with caplog.at_level(logging.WARNING, logger="lta.helpers.jaccard"):
        result = jaccard.bootstrap(x, y)
    assert result["p-val"] == pytest.approx(1.0)
    assert "degenerate" in caplog.text


def test_bootstrap_deterministic_with_seed() -> None:
    """Same seed should produce identical J-sim and p-val across calls."""
    x = b(1, 0, 1, 0, 1, 0, 1, 0)
    y = b(0, 1, 0, 1, 1, 0, 1, 0)
    r1 = jaccard.bootstrap(x, y, n=500, seed=7)
    r2 = jaccard.bootstrap(x, y, n=500, seed=7)
    assert r1["J-sim"] == r2["J-sim"]
    assert r1["p-val"] == r2["p-val"]


def test_bootstrap_jsim_matches_similarity() -> None:
    """J-sim in bootstrap result should match the plain similarity value."""
    x = b(1, 0, 1, 0, 1, 0)
    y = b(1, 1, 0, 0, 1, 0)
    result = jaccard.bootstrap(x, y, seed=42)
    expected_jsim = jaccard.similarity(x, y)
    assert result["J-sim"] == pytest.approx(expected_jsim)
