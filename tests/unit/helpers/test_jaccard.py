"""Unit tests for Jaccard similarity helpers."""

import numpy as np
import pandas as pd
import pytest

from lta.helpers import jaccard


def b(*vals: int) -> np.ndarray:
    return np.array(vals, dtype=bool)


# ---------------------------------------------------------------------------
# similarity
# ---------------------------------------------------------------------------


def test_similarity_identical_vectors() -> None:
    x = b(1, 1, 0, 1)
    assert jaccard.similarity(x, x) == pytest.approx(1.0)


def test_similarity_disjoint_vectors() -> None:
    x = b(1, 1, 0, 0)
    y = b(0, 0, 1, 1)
    assert jaccard.similarity(x, y) == pytest.approx(0.0)


def test_similarity_partial_overlap() -> None:
    x = b(1, 1, 1, 0)
    y = b(1, 1, 0, 1)
    # intersect=2, union=4 → 0.5
    assert jaccard.similarity(x, y) == pytest.approx(0.5)


def test_similarity_all_zeros_returns_nan() -> None:
    x = b(0, 0, 0)
    y = b(0, 0, 0)
    result = jaccard.similarity(x, y)
    assert np.isnan(result)


def test_similarity_with_explicit_px_py() -> None:
    x = b(1, 0, 1, 0)
    y = b(1, 0, 1, 0)
    result = jaccard.similarity(x, y, px=0.5, py=0.5)
    assert result == pytest.approx(1.0)


def test_similarity_centered() -> None:
    x = b(1, 1, 0, 0)
    y = b(1, 1, 0, 0)
    # j=1, px=py=0.5, denominator=0.75, centered = 1 - (0.25/0.75)
    expected = 1.0 - (0.25 / 0.75)
    assert jaccard.similarity(x, y, center=True) == pytest.approx(expected)


def test_similarity_raises_on_2d_input() -> None:
    x = np.array([[True, False], [True, False]])
    y = np.array([[True, False], [True, False]])
    with pytest.raises(IndexError):
        jaccard.similarity(x, y)


def test_similarity_raises_on_length_mismatch() -> None:
    with pytest.raises(IndexError):
        jaccard.similarity(b(1, 0), b(1, 0, 1))


def test_similarity_raises_on_non_boolean_dtype() -> None:
    x = np.array([1, 0, 1], dtype=int)
    y = np.array([1, 0, 1], dtype=int)
    with pytest.raises(TypeError):
        jaccard.similarity(x, y)


# ---------------------------------------------------------------------------
# distance
# ---------------------------------------------------------------------------


def test_distance_identical_vectors() -> None:
    x = b(1, 0, 1)
    assert jaccard.distance(x, x) == pytest.approx(0.0)


def test_distance_disjoint_vectors() -> None:
    x = b(1, 1, 0, 0)
    y = b(0, 0, 1, 1)
    assert jaccard.distance(x, y) == pytest.approx(1.0)


def test_distance_partial_overlap() -> None:
    x = b(1, 1, 1, 0)
    y = b(1, 1, 0, 1)
    assert jaccard.distance(x, y) == pytest.approx(0.5)


def test_distance_with_explicit_px_py() -> None:
    x = b(1, 0, 1, 0)
    y = b(1, 0, 1, 0)
    result = jaccard.distance(x, y, px=0.5, py=0.5)
    assert result == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# bootstrap
# ---------------------------------------------------------------------------


def test_bootstrap_returns_series_with_correct_index() -> None:
    x = b(1, 0, 1, 0, 1, 0)
    y = b(1, 1, 0, 0, 1, 0)
    result = jaccard.bootstrap(x, y, seed=0)
    assert isinstance(result, pd.Series)
    assert list(result.index) == ["J-sim", "p-val"]


def test_bootstrap_p_value_in_range() -> None:
    x = b(1, 0, 1, 0, 1, 0)
    y = b(1, 1, 0, 0, 1, 0)
    result = jaccard.bootstrap(x, y, n=200, seed=42)
    assert 0.0 <= result["p-val"] <= 1.0


def test_bootstrap_degenerate_all_ones(caplog: pytest.LogCaptureFixture) -> None:
    x = b(1, 1, 1, 1)
    y = b(1, 0, 1, 0)
    import logging

    with caplog.at_level(logging.WARNING, logger="lta.helpers.jaccard"):
        result = jaccard.bootstrap(x, y)
    assert result["p-val"] == pytest.approx(1.0)
    assert "degenerate" in caplog.text


def test_bootstrap_degenerate_all_zeros(caplog: pytest.LogCaptureFixture) -> None:
    x = b(0, 0, 0, 0)
    y = b(1, 0, 1, 0)
    import logging

    with caplog.at_level(logging.WARNING, logger="lta.helpers.jaccard"):
        result = jaccard.bootstrap(x, y)
    assert result["p-val"] == pytest.approx(1.0)
    assert "degenerate" in caplog.text


def test_bootstrap_deterministic_with_seed() -> None:
    x = b(1, 0, 1, 0, 1, 0, 1, 0)
    y = b(0, 1, 0, 1, 1, 0, 1, 0)
    r1 = jaccard.bootstrap(x, y, n=500, seed=7)
    r2 = jaccard.bootstrap(x, y, n=500, seed=7)
    assert r1["J-sim"] == r2["J-sim"]
    assert r1["p-val"] == r2["p-val"]


def test_bootstrap_jsim_matches_similarity() -> None:
    x = b(1, 0, 1, 0, 1, 0)
    y = b(1, 1, 0, 0, 1, 0)
    result = jaccard.bootstrap(x, y, seed=42)
    expected_jsim = jaccard.similarity(x, y)
    assert result["J-sim"] == pytest.approx(expected_jsim)
