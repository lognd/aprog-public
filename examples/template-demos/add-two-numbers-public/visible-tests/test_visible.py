"""
Visible tests for Add Two Numbers.

Run locally:
    python -m pytest test_visible.py -v

These tests call your program as a subprocess and compare its stdout
against the expected output for each sample case.
"""

import subprocess
import sys
from pathlib import Path

SUBMISSION = Path(__file__).parent.parent / "add-two-numbers.py"


def run(stdin: str, args: list[str] | None = None) -> str:
    result = subprocess.run(
        [sys.executable, str(SUBMISSION)] + (args or []),
        input=stdin,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.stdout


def test_example_1():
    assert run("3\n7\n").strip() == "10"


def test_example_2():
    assert run("-5\n3\n").strip() == "-2"


def test_zeros():
    assert run("0\n0\n").strip() == "0"
