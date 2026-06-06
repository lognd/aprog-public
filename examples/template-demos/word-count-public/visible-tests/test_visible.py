"""
Visible tests for Word Count.

Build locally:
    make
    echo "hello world" | ./word-count
"""

import subprocess
from pathlib import Path


def run(stdin: str) -> str:
    result = subprocess.run(
        [str(Path(__file__).parent.parent / "word-count")],
        input=stdin,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.stdout


def test_three_lines():
    out = run("hello world\nfoo bar baz\none\n")
    assert out.strip() == "Line 1: 2 words\nLine 2: 3 words\nLine 3: 1 word\nTotal: 6 words"


def test_single_line():
    out = run("the quick brown fox\n")
    assert out.strip() == "Line 1: 4 words\nTotal: 4 words"
