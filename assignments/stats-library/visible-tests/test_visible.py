"""
Visible tests for Stats Library.

Build and run locally:
    cmake -B build .
    cmake --build build
    echo "TODO" | ./build/stats-library
"""

import subprocess
from pathlib import Path


def run(stdin: str) -> str:
    result = subprocess.run(
        [str(Path("build") / "stats-library")],
        input=stdin,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.stdout


# FILL IN: visible test cases.
def test_example_1():
    output = run("TODO\n")
    assert output.strip() == "TODO"