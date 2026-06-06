"""
Visible tests for Stack ADT.

Run locally:
    python -m pytest test_visible.py -v
"""

import importlib.util
import pytest
from pathlib import Path

_src = Path(__file__).parent.parent / "stack-adt.py"
_spec = importlib.util.spec_from_file_location("stack_adt_module", _src)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
Stack = _mod.Stack


def test_push_and_size():
    s = Stack()
    s.push(1)
    s.push(2)
    assert s.size() == 2


def test_pop_lifo():
    s = Stack()
    s.push(10)
    s.push(20)
    assert s.pop() == 20
    assert s.pop() == 10


def test_peek_does_not_remove():
    s = Stack()
    s.push(5)
    assert s.peek() == 5
    assert s.size() == 1


def test_is_empty():
    s = Stack()
    assert s.is_empty()
    s.push(1)
    assert not s.is_empty()


def test_pop_raises_on_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()


def test_peek_raises_on_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()
