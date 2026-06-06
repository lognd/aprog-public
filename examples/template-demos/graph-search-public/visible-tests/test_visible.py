"""
Visible tests for Graph Search.

Build and run locally:
    cmake -B build .
    cmake --build build
    echo "..." | ./build/graph-search
"""

import subprocess
from pathlib import Path


def run(stdin: str) -> str:
    result = subprocess.run(
        [str(Path("build") / "graph-search")],
        input=stdin,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.stdout


GRAPH1 = "5 5\n0 1\n0 2\n1 3\n2 3\n3 4\n0\n"
GRAPH2 = "4 2\n0 1\n2 3\n0\n"


def test_connected_graph():
    assert run(GRAPH1).strip() == "0 1 2 3 4"


def test_disconnected_graph():
    assert run(GRAPH2).strip() == "0 1"
