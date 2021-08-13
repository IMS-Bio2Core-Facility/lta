# -*- coding: utf-8 -*-
"""Unit tests for the Jaccard module."""
import numpy as np
import pytest
from _pytest import capture

import lta.helpers.jaccard as jac


def test_sim_2d() -> None:
    """It raises an index error when input is not 1d."""
    x = np.array([[True], [False]], bool)
    y = np.array([[True], [False]], bool)
    with pytest.raises(IndexError):
        jac.similarity(x, y)


def test_sim_shape() -> None:
    """It raises an index error when input is not the same length."""
    x = np.array([True], bool)
    y = np.array([True, False], bool)
    with pytest.raises(IndexError):
        jac.similarity(x, y)


def test_sim_bool() -> None:
    """It raises a TypeError when the dtype is not bool."""
    x = np.array([1, 0], int)
    y = np.array([1, 0], int)
    with pytest.raises(TypeError):
        jac.similarity(x, y)


def test_sim_center() -> None:
    """It centers the similarity, when center is True."""
    x = np.array([True, True, False], bool)
    y = np.array([True, False, True], bool)
    val = jac.similarity(x, y, center=True)
    np.testing.assert_allclose(val, -1 / 6)


def test_sim_pxpy() -> None:
    """It uses px/py when passed."""
    x = np.array([False, False, False], bool)
    y = np.array([False, False, False], bool)
    val = jac.similarity(x, y, px=0.5, py=0.5)
    np.testing.assert_allclose(val, 1 / 3)


def test_sim_default() -> None:
    """It returns the Jaccard similarity."""
    x = np.array([True, True, False], bool)
    y = np.array([True, False, True], bool)
    val = jac.similarity(x, y)
    np.testing.assert_allclose(val, 1 / 3)


def test_distance() -> None:
    """It calculates the Jaccard distance."""
    x = np.array([True, True, False], bool)
    y = np.array([True, False, True], bool)
    val = jac.distance(x, y)
    np.testing.assert_allclose(val, 2 / 3)


def test_dist_pxpy() -> None:
    """It uses px/py when passed."""
    x = np.array([False, False, False], bool)
    y = np.array([False, False, False], bool)
    val = jac.distance(x, y, px=0.5, py=0.5)
    np.testing.assert_allclose(val, 2 / 3)


def test_boot_all_ones(capsys: capture.CaptureFixture) -> None:
    """It return a p of 1 if all values are True."""
    x = np.array([True, True, True], bool)
    y = np.array([True, False, True], bool)
    val = jac.bootstrap(x, y, n=10)
    out, err = capsys.readouterr()
    assert out == "Calculation is degenerate as at least one vector is all 1s.\n"
    assert err == ""
    np.testing.assert_allclose(val, (2 / 3, 1))


def test_boot_all_zeros(capsys: capture.CaptureFixture) -> None:
    """It return a p of 1 if all values are False."""
    x = np.array([True, True, False], bool)
    y = np.array([False, False, False], bool)
    val = jac.bootstrap(x, y, n=10)
    out, err = capsys.readouterr()
    assert out == "Calculation is degenerate as at least one vector is all 0s.\n"
    assert err == ""
    np.testing.assert_allclose(val, (0, 1))


def test_boot_pxpy(capsys: capture.CaptureFixture) -> None:
    """It defers to px/py, when passed."""
    x = np.array([True, True, False], bool)
    y = np.array([True, False, False], bool)
    val = jac.bootstrap(x, y, n=10, px=1, py=1)
    out, err = capsys.readouterr()
    assert out == "Calculation is degenerate as at least one vector is all 1s.\n"
    assert err == ""
    np.testing.assert_allclose(val, (0.5, 1))


def test_boot() -> None:
    """It calculates the Jaccard distance."""
    x = np.array([True, True, False], bool)
    y = np.array([True, False, True], bool)
    val = jac.bootstrap(x, y, n=10)
    np.testing.assert_allclose(val, (1 / 3, 0.6))
