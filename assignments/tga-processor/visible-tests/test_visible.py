"""
Visible tests for Tga Processor.

Build locally:
    make
    echo "TODO" | ./tga-processor
"""

import subprocess
from pathlib import Path


def run(stdin: str) -> str:
    result = subprocess.run(
        [str(Path(__file__).parent.parent / "tga-processor")],
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