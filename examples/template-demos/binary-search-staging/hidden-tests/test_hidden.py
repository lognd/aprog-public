"""
Hidden tests for Binary Search.

More thorough than visible-tests/; hidden until after the due date.
"""

import importlib.util
import os
import sys
from pathlib import Path

_src = Path(os.environ.get("SUBMISSION_DIR", "/autograder/submission")) / "binary-search.py"
_spec = importlib.util.spec_from_file_location("binary_search_module", _src)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
binary_search = _mod.binary_search


def test_single_element_found():
    assert binary_search([42], 42) == 0


def test_single_element_not_found():
    assert binary_search([42], 7) == -1


def test_large_array():
    arr = list(range(0, 10000, 2))
    assert binary_search(arr, 9998) == 4999
    assert binary_search(arr, 9999) == -1


def test_negative_values():
    assert binary_search([-10, -5, 0, 5, 10], -5) == 1


def test_two_elements_found_first():
    assert binary_search([3, 7], 3) == 0


def test_two_elements_found_second():
    assert binary_search([3, 7], 7) == 1
