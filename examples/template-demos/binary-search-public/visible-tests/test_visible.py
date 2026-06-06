"""
Visible tests for Binary Search.

Run locally:
    python -m pytest test_visible.py -v
"""

import importlib.util
import sys
from pathlib import Path

_src = Path(__file__).parent.parent / "binary-search.py"
_spec = importlib.util.spec_from_file_location("binary_search_module", _src)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
binary_search = _mod.binary_search


def test_found_middle():
    assert binary_search([1, 3, 5, 7, 9], 5) == 2


def test_found_first():
    assert binary_search([1, 3, 5, 7, 9], 1) == 0


def test_found_last():
    assert binary_search([1, 3, 5, 7, 9], 9) == 4


def test_not_found():
    assert binary_search([1, 3, 5, 7, 9], 4) == -1


def test_empty():
    assert binary_search([], 1) == -1
