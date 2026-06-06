"""
Hidden tests for Add Two Numbers.

These run on Gradescope after the due date.
"""

import subprocess
import sys
from pathlib import Path

SUBMISSION = Path("/autograder/submission/add-two-numbers.py")


def run(stdin: str) -> str:
    result = subprocess.run(
        [sys.executable, str(SUBMISSION)],
        input=stdin,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.stdout


def test_hidden_large():
    assert run("1000000000\n-1000000000\n").strip() == "0"


def test_hidden_negative():
    assert run("-100\n-200\n").strip() == "-300"


def test_hidden_both_positive():
    assert run("42\n58\n").strip() == "100"
