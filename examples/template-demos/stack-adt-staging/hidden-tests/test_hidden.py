"""
Hidden tests for Stack ADT.

Imported by PytestTest at grading time.
"""

import importlib.util
import os
import pytest
from pathlib import Path

_src = Path(os.environ.get("SUBMISSION_DIR", "/autograder/submission")) / "stack-adt.py"
_spec = importlib.util.spec_from_file_location("stack_adt_module", _src)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
Stack = _mod.Stack


def test_hidden_push_pop_interleaved():
    s = Stack()
    s.push(1)
    s.push(2)
    assert s.pop() == 2
    s.push(3)
    assert s.pop() == 3
    assert s.pop() == 1
    assert s.is_empty()


def test_hidden_size_after_push_pop():
    s = Stack()
    for i in range(10):
        s.push(i)
    assert s.size() == 10
    for _ in range(5):
        s.pop()
    assert s.size() == 5


def test_hidden_peek_unchanged():
    s = Stack()
    s.push(42)
    s.push(99)
    for _ in range(5):
        assert s.peek() == 99
    assert s.size() == 2


def test_hidden_various_types():
    s = Stack()
    s.push("hello")
    s.push(3.14)
    s.push([1, 2])
    assert s.pop() == [1, 2]
    assert s.pop() == 3.14
    assert s.pop() == "hello"
    assert s.is_empty()


def test_hidden_pop_raises_after_emptied():
    s = Stack()
    s.push(1)
    s.pop()
    with pytest.raises(IndexError):
        s.pop()
