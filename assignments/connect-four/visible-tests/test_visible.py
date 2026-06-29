"""
Visible tests for Connect Four.

Build first:
    cmake -B build .
    cmake --build build

Then run from the project root:
    python -m pytest visible-tests/test_visible.py -v
"""

import subprocess
from pathlib import Path


def _run(mode: str, stdin: str, timeout: int = 10) -> str:
    binary = Path("build") / "connect_four"
    result = subprocess.run(
        [str(binary), mode],
        input=stdin,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result.stdout


def test_initial_board_is_all_dots():
    # Send EOF immediately -- game prints the initial board then exits.
    out = _run("--two-player", "")
    lines = out.splitlines()
    # First 6 lines should be ". . . . . . ."
    board_lines = [l for l in lines if set(l.replace(" ", "")) <= set("XO.")]
    assert len(board_lines) >= 6
    assert board_lines[0] == ". . . . . . ."
    assert board_lines[5] == ". . . . . . ."


def test_column_numbers_row():
    out = _run("--two-player", "")
    assert "0 1 2 3 4 5 6" in out


def test_two_player_x_wins_horizontal():
    # X plays 0,1,2,3; O plays 4,5,6 -> X wins in bottom row.
    moves = "0\n4\n1\n5\n2\n6\n3\n"
    out = _run("--two-player", moves)
    assert "Player X wins!" in out


def test_two_player_o_wins_vertical():
    # O stacks column 0 four times while X wastes moves elsewhere.
    # X: 1,2,3,6  O: 0,0,0,0
    moves = "1\n0\n2\n0\n3\n0\n6\n0\n"
    out = _run("--two-player", moves)
    assert "Player O wins!" in out


def test_vs_computer_computer_plays():
    # Human plays col 0 once, then EOF. Computer should respond.
    out = _run("--vs-computer", "0\n")
    assert "Computer plays column" in out
