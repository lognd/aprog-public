# Connect Four

You have a flat character grid and a full set of grid operations. Now put them to work. This assignment asks you to implement the logic layer of a playable Connect Four game -- drop pieces, detect four-in-a-row in all directions, and drive a deterministic computer opponent.

`main.cpp` is provided and already handles all input/output. Your job is `board.cpp`.

## Learning goals

- Practice using a flat row-major grid (`char*`) as a real data structure, not a tutorial toy
- Write a four-direction run-detection algorithm (horizontal, vertical, both diagonals)
- Implement a simple but correct decision procedure (win > block > heuristic --
  a rule-of-thumb move that is not guaranteed optimal but is cheap to compute)
- Understand the difference between mutating functions (`char*`) and read-only functions (`const char*`)

---

## Background

The board is a 6-row x 7-column grid stored as a flat `char` array in row-major order, the same layout you used in the const-qualifier-toolkit assignment. Empty cells are `'.'`, player one is `'X'`, and the computer (or player two) is `'O'`. You access and modify it with the `grid.hpp` functions -- `cell_at`, `set_cell`, `row_ptr`, and friends -- which you already know how to use.

---

## Task

Implement the four functions declared in `board.hpp`.

### `drop_piece`

Find the lowest empty row in `column` and place `piece` there. Return `true` on success, `false` if the column is already full (the top cell, row 0, is not `'.'`).

### `check_win`

Return `true` if `piece` has four consecutive copies anywhere on the board. Check all four directions: horizontal, vertical, diagonal (top-left to bottom-right), and anti-diagonal (top-right to bottom-left). A run of exactly four is sufficient; longer runs also count.

### `is_full`

Return `true` if no cell on the board equals `'.'`.

### `computer_move`

Return the column the computer should play. Use this three-priority decision procedure, in order:

1. If the computer can win immediately by playing some column, play that column (lowest index wins if multiple columns work).
2. If the human can win next turn by playing some column, block that column (lowest index wins ties).
3. Otherwise, play the non-full column closest to center (`cols / 2`). Among columns equally close to center, prefer the lower-indexed one.

To check whether a column leads to a win, simulate: call `drop_piece` on a copy of the board, then call `check_win`. Do not use randomness -- the AI must be fully deterministic (given the same board, it must always choose the same move).

---

## Output format

`main.cpp` handles all output, but the tests are written against its exact format. Make sure your implementation produces the right board state so the display is correct.

**Board display** (printed before each turn and after the final move):

```
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
0 1 2 3 4 5 6

```

Cells are separated by single spaces. Column numbers appear on the row below the board. A blank line follows the column numbers.

**Prompts:**

```
Player X's turn (0-6): 
Player O's turn (0-6): 
Your turn (0-6): 
Computer plays column 3.
```

**End-of-game messages:**

```
Player X wins!
Player O wins!
It's a draw!
```

---

## Files

| File | Purpose |
|------|---------|
| `board.hpp` | Function declarations -- do not modify |
| `board.cpp` | Write your implementation here |
| `grid.hpp` | Grid helper declarations -- do not modify |
| `grid.cpp` | Grid helper implementation (copy from const-qualifier-toolkit or reuse yours) |
| `main.cpp` | Game loop and I/O -- provided, do not modify |
| `CMakeLists.txt` | Build file -- do not modify |

---

## Compilation and Testing

```bash
cmake -B build .
cmake --build build
```

Run two-player mode:

```bash
./build/connect_four --two-player
```

Run vs. computer:

```bash
./build/connect_four --vs-computer
```

Run visible tests (from the project root) with pytest, a Python test-running
tool that discovers and executes test functions and reports pass/fail for each:

```bash
python -m pytest visible-tests/test_visible.py -v
```

---

## Constraints

- Do not modify `board.hpp`, `grid.hpp`, `main.cpp`, or `CMakeLists.txt`.
- Do not use dynamic allocation (`new`, `malloc`, `std::vector`, etc.). Use local arrays.
- Do not use global variables.
- `computer_move` must be deterministic -- no random number generators.
- Use the `grid.hpp` functions where possible instead of raw pointer arithmetic.

---

## Grading

A "gate" component below means the requirement must pass before any other
points are awarded -- if your code does not compile, none of the other rows
count.

| Component | Points |
|-----------|--------|
| Compilation | gate |
| `drop_piece` and `is_full` | 20 |
| `check_win` -- all four directions | 30 |
| `computer_move` -- all three priorities | 20 |
| Integration: full game scripted tests | 20 |
| No dynamic allocation | 10 |
| **Total** | **100** |

---

## Submission

Submit two files: `board.cpp` and `grid.cpp`. Do not rename them.

If you wrote your own `grid.cpp` in the const-qualifier-toolkit assignment, submit that same file here -- the `grid.hpp` interface is identical.

---

## Going further

- Add a fourth priority to `computer_move`: after the center heuristic, prefer columns adjacent to existing pieces of your own color to build toward future fours.
- Implement a depth-2 lookahead (checking two moves ahead instead of one): avoid columns that hand the opponent a winning move on their next turn.
- Benchmark your `check_win` implementation with a full board and a piece that does not win. How many cell reads does it perform? Can you reduce that number?
