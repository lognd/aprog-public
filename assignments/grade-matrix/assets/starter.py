# grade-matrix -- starter file.
#
# Implement six functions over a scores matrix (rows = students, columns
# = assignments). See README.md for the exact spec of each.
#
# numpy is the only third-party import allowed. LOOPS ARE FORBIDDEN:
# no "for" and no "while" keyword may appear anywhere in this file --
# every function must be written using numpy's vectorized operations
# (reductions, broadcasting, boolean masking) instead.
#
# The signatures below are left UNANNOTATED on purpose: the type-annotation
# bonus asks you to add the hints yourself (the exact types are in the
# README -- a numpy array is spelled `np.ndarray`).

from __future__ import annotations

import numpy as np


def student_means(m):
    """Return each student's (row's) mean score, as a 1-D array of length n_students."""
    raise NotImplementedError


def assignment_means(m):
    """Return each assignment's (column's) mean score, as a 1-D array of length n_assignments."""
    raise NotImplementedError


def curve_to(m, target):
    """Return a new matrix with a per-assignment (per-column) offset added so each column's mean equals target."""
    raise NotImplementedError


def drop_lowest(m):
    """Return each student's mean score excluding their single lowest score.

    With only one assignment, "excluding the lowest score" would leave
    zero scores to average -- defined as 0.0 for that edge case rather
    than dividing by zero.
    """
    raise NotImplementedError


def passing_mask(m, threshold):
    """Return a boolean mask (length n_students) marking which students' mean score meets or exceeds threshold."""
    raise NotImplementedError


def standardize(m):
    """Return per-column z-scores: (value - column mean) / column std. Columns with zero std become all zeros."""
    raise NotImplementedError
