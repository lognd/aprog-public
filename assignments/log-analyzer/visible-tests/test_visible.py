"""
Visible tests for Log Analyzer.

Compile and run locally:
    g++ -std=c++17 -Wall -o log-analyzer log-analyzer.cpp
    echo "TODO" | ./log-analyzer

These tests are also run by the autograder and shown immediately.
"""

import subprocess
from pathlib import Path


def compile_binary() -> Path:
    src = Path(__file__).parent.parent / "log-analyzer.cpp"
    out = Path(__file__).parent / "log-analyzer"
    subprocess.run(
        ["g++", "-std=c++17", "-Wall", "-o", str(out), str(src)],
        check=True,
    )
    return out


def run(binary: Path, stdin: str) -> str:
    result = subprocess.run(
        [str(binary)],
        input=stdin,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.stdout


BINARY = compile_binary()


# FILL IN: visible test cases matching the examples in README.md.
def test_example_1():
    output = run(BINARY, "TODO\n")
    assert output.strip() == "TODO"