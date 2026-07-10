"""Visible tests for Grade Matrix.

Run locally:
    python -m pytest visible-tests/test_visible.py -v
"""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.environ["SUBMISSION_DIR"])

from matrix_ops import (  # noqa: E402
    assignment_means,
    curve_to,
    drop_lowest,
    passing_mask,
    standardize,
    student_means,
)


_M = np.array(
    [
        [80.0, 90.0, 70.0],
        [60.0, 50.0, 100.0],
        [100.0, 100.0, 100.0],
    ]
)


def test_student_means_basic():
    result = student_means(_M)
    assert result == pytest.approx([80.0, 70.0, 100.0])


def test_student_means_shape():
    result = student_means(_M)
    assert result.shape == (3,)


def test_assignment_means_basic():
    result = assignment_means(_M)
    assert result == pytest.approx([80.0, 80.0, 90.0])


def test_assignment_means_shape():
    result = assignment_means(_M)
    assert result.shape == (3,)


def test_curve_to_hits_target_mean():
    curved = curve_to(_M, 90.0)
    assert curved.mean(axis=0) == pytest.approx([90.0, 90.0, 90.0])


def test_curve_to_preserves_relative_differences():
    curved = curve_to(_M, 90.0)
    # Curving adds a constant per column, so within-column differences
    # between students are unchanged.
    original_diff = _M[0, 0] - _M[1, 0]
    curved_diff = curved[0, 0] - curved[1, 0]
    assert curved_diff == pytest.approx(original_diff)


def test_drop_lowest_basic():
    result = drop_lowest(_M)
    assert result == pytest.approx([85.0, 80.0, 100.0])


def test_drop_lowest_single_assignment():
    m = np.array([[5.0], [7.0]])
    result = drop_lowest(m)
    assert result == pytest.approx([0.0, 0.0])


def test_passing_mask_basic():
    result = passing_mask(_M, 80.0)
    assert list(result) == [True, False, True]


def test_passing_mask_dtype_bool():
    result = passing_mask(_M, 80.0)
    assert result.dtype == bool


def test_standardize_basic():
    result = standardize(_M)
    assert result.mean(axis=0) == pytest.approx([0.0, 0.0, 0.0], abs=1e-9)
    assert result.std(axis=0) == pytest.approx([1.0, 1.0, 1.0])


def test_standardize_zero_std_column():
    m = np.array([[5.0, 1.0], [5.0, 2.0], [5.0, 3.0]])
    result = standardize(m)
    assert result[:, 0] == pytest.approx([0.0, 0.0, 0.0])
