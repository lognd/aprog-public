"""
Visible tests for Log Analyzer.

Compile and run locally:
    g++ -std=c++17 -Wall -o log-analyzer log-analyzer.cpp
    ./log-analyzer visible-tests/logs/basic_two.log

These tests are also run by the autograder and shown immediately.
"""

import subprocess
from pathlib import Path

LOGS_DIR = Path(__file__).parent / "logs"


def compile_binary() -> Path:
    src = Path(__file__).parent.parent / "log-analyzer.cpp"
    out = Path(__file__).parent / "log-analyzer"
    subprocess.run(
        ["g++", "-std=c++17", "-Wall", "-o", str(out), str(src)],
        check=True,
    )
    return out


def run(binary: Path, logfile: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [str(binary), str(logfile)],
        capture_output=True,
        text=True,
        timeout=10,
    )


BINARY = compile_binary()


def test_basic_two_levels():
    result = run(BINARY, LOGS_DIR / "basic_two.log")
    assert result.returncode == 0
    assert result.stdout == (
        "LEVEL     COUNT  MOST RECENT\n"
        "ERROR         1  disk full on /dev/sda1\n"
        "INFO          2  request handled\n"
    )


def test_single_entry():
    result = run(BINARY, LOGS_DIR / "single.log")
    assert result.returncode == 0
    assert result.stdout == (
        "LEVEL     COUNT  MOST RECENT\n"
        "ERROR         1  catastrophic failure in subsystem A\n"
    )


def test_missing_file_exits_nonzero():
    result = run(BINARY, LOGS_DIR / "does_not_exist.log")
    assert result.returncode == 1
    assert "error: cannot open" in result.stderr
