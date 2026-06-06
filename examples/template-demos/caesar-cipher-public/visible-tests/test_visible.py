"""
Visible tests for Caesar Cipher.

Compile and run locally:
    gcc -std=c11 -Wall -o caesar-cipher caesar-cipher.c
    echo "Hello, World!" | ./caesar-cipher 3
"""

import subprocess
from pathlib import Path


def compile_binary() -> Path:
    src = Path(__file__).parent.parent / "caesar-cipher.c"
    out = Path(__file__).parent / "caesar-cipher"
    subprocess.run(
        ["gcc", "-std=c11", "-Wall", "-o", str(out), str(src)],
        check=True,
    )
    return out


def run(binary: Path, stdin: str, shift: int) -> str:
    result = subprocess.run(
        [str(binary), str(shift)],
        input=stdin,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.stdout


BINARY = compile_binary()


def test_shift_3():
    assert run(BINARY, "Hello, World!\n", 3).strip() == "Khoor, Zruog!"


def test_rot13():
    assert run(BINARY, "Hello\n", 13).strip() == "Uryyb"


def test_shift_0():
    assert run(BINARY, "abc\n", 0).strip() == "abc"
