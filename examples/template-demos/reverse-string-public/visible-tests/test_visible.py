"""
Visible tests for Reverse String.

Compile and run locally:
    g++ -std=c++17 -Wall -o reverse-string reverse-string.cpp
    echo "hello" | ./reverse-string
"""

import subprocess
from pathlib import Path


def compile_binary() -> Path:
    src = Path(__file__).parent.parent / "reverse-string.cpp"
    out = Path(__file__).parent / "reverse-string"
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


def test_hello():
    assert run(BINARY, "hello\n").strip() == "olleh"


def test_palindrome():
    assert run(BINARY, "racecar\n").strip() == "racecar"


def test_single_char():
    assert run(BINARY, "a\n").strip() == "a"
