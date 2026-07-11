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

The board is a 6-row x 7-column grid stored as a flat `char` array in row-major order, the same layout you used in the const-qualifier-toolkit assignment. Empty cells are `'.'`, player one is `'X'`, and the computer (or player two) is `'O'`. You access and modify it with the `grid.hpp` functions -- `cell_at`, `set_cell`, `row_ptr`, and friends -- which you already know how to use. Rows are numbered `0` (top) to `5` (bottom); columns are numbered `0` (left) to `6` (right) -- the same numbers `main.cpp` prints under the board.

---

## Examples: every function on one board

To make the four functions concrete, here is **one** board, with column
numbers written below it (the same header `main.cpp` prints), and what
each function returns for it. Read this table first -- it is the whole
assignment in miniature.

```
row 0:  O . . . . . .
row 1:  X . . . . . .
row 2:  O . X . . . .
row 3:  X . O X . . .
row 4:  O X X O X . .
row 5:  X O O X O O .
        0 1 2 3 4 5 6
```

| Call | Returns | Why |
|------|---------|-----|
| `check_win(board, 6, 7, 'X')` | `false` | `X` has three in a diagonal run -- `(row 2, col 2)`, `(row 3, col 3)`, `(row 4, col 4)` -- but `(row 5, col 5)` is `'O'`, so the run stops at three. A run of exactly three never counts, no matter how promising it looks. |
| `check_win(board, 6, 7, 'O')` | `false` | no four `O`s line up in any of the four directions anywhere on this board |
| `is_full(board, 6, 7)` | `false` | column 6 is entirely `'.'`, and several other columns have empty cells above their filled ones |
| `drop_piece(board, 6, 7, 0, 'X')` | `false` | column 0 is completely full -- the top cell `(row 0, col 0)` is `'O'`, not `'.'` -- so nothing is placed and the board is left unchanged |
| `drop_piece(board, 6, 7, 6, 'O')` | `true` | column 6 is empty, so the piece lands at the very bottom, `(row 5, col 6)` |
| `drop_piece(board, 6, 7, 4, 'X')` | `true` | column 4 already has its bottom two cells filled (`row 4`, `row 5`), so the new piece lands one cell up, at `(row 3, col 4)` -- this does not complete the diagonal above, since that diagonal needs `(row 5, col 5)`, a different cell |

Note that every call above uses `rows = 6` and `cols = 7` (that is the fixed
board size `main.cpp` always builds), even though the examples write the
board itself as a 6-line picture for readability.

### `computer_move` on four small boards

`computer_move` only makes sense to demonstrate on boards built for that
one purpose, so here are four tiny boards, each isolating one branch of
the three-priority procedure. In all four, the computer is `'O'` and the
human is `'X'`.

**A -- computer can win immediately (priority 1):**

```
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . O O O . .
0 1 2 3 4 5 6
```

`computer_move(board, 6, 7, 'O', 'X') == 1`. Two columns would complete
four `O`s in the bottom row -- column 1 (making cols 1-4) and column 5
(making cols 2-5) -- and the rule for ties is "lowest index wins," so the
answer is `1`, not `5`.

**B -- human threatens to win next turn, computer must block (priority 2):**

```
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. X X X . . .
0 1 2 3 4 5 6
```

`computer_move(board, 6, 7, 'O', 'X') == 0`. The computer cannot win this
turn, but `X` could win next turn by playing column 0 (cols 0-3) or
column 4 (cols 1-4). Block the lower-indexed threat first: `0`.

**C -- no win or block available, fall back to the center heuristic (priority 3):**

```
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
0 1 2 3 4 5 6
```

`computer_move(board, 6, 7, 'O', 'X') == 3`. An empty board has no win or
block available, so the computer plays the center column: `cols / 2 == 7
/ 2 == 3` (integer division).

**C2 -- the center column is full, so the heuristic must break a tie:**

```
. . . O . . .
. . . X . . .
. . . O . . .
. . . X . . .
. . . O . . .
. . . X . . .
0 1 2 3 4 5 6
```

`computer_move(board, 6, 7, 'O', 'X') == 2`. Column 3 (the true center) is
full, so the next-closest columns are 2 and 4, both at distance 1. The
tie-break rule is "prefer the lower-indexed one," so the answer is `2`,
not `4`.

### Wins in every direction

`check_win` must catch a run of four in all four directions. Here is one
positive example of each:

```
Horizontal (row 5, cols 0-3):     Vertical (col 2, rows 2-5):
X X X X . . .                     . . . . . . .
. . . . . . .                     . . . . . . .
. . . . . . .                     . . O . . . .
. . . . . . .                     . . O . . . .
. . . . . . .                     . . O . . . .
. . . . . . .                     . . O . . . .

Diagonal, top-left to bottom-right   Anti-diagonal, top-right to bottom-left
(cols 0-3, rows 4-1):                (cols 3-6, rows 4-1):
. . . . . . .                        . . . . . . .
X . . . . . .                        . . . . . . X
. X . . . . .                        . . . . . X .
. . X . . . .                        . . . . X . .
. . . X . . .                        . . . X . . .
. . . . . . .                        . . . . . . .
```

`check_win(board, 6, 7, 'X')` is `true` for the diagonal and anti-diagonal
boards above; `check_win(board, 6, 7, 'O')` is `true` for the vertical board.
Notice both diagonals run for exactly four cells -- one fewer, and
`check_win` must correctly return `false` instead (see the main example
board above, where a diagonal run of three does not count).

---

## Worked example: watch a full game play out, move by move

This traces the exact two-player game
`./build/connect_four --two-player` plays when fed the column sequence
`0, 4, 1, 5, 2, 6, 3` (X moves first, then O, alternating). Only the
bottom row (`row 5`) changes in this particular game, since every move
lands on an empty column and nothing stacks -- watch how `X` quietly
builds a four-in-a-row across columns 0-3 while `O` plays elsewhere.

| Move | Column | Player | Piece placed at | Bottom row (`row 5`) after the move | Why |
|------|--------|--------|------------------|--------------------------------------|-----|
| 1 | 0 | X | `(row 5, col 0)` | `X . . . . . .` | column 0 was empty, so `X` lands at the bottom |
| 2 | 4 | O | `(row 5, col 4)` | `X . . . O . .` | column 4 was empty; no four-in-a-row yet for either player |
| 3 | 1 | X | `(row 5, col 1)` | `X X . . O . .` | `X` now has two in a row (cols 0-1), still short of four |
| 4 | 5 | O | `(row 5, col 5)` | `X X . . O O .` | `O` now has two in a row (cols 4-5), still short of four |
| 5 | 2 | X | `(row 5, col 2)` | `X X X . O O .` | `X` now has three in a row (cols 0-2) -- one more in column 3 would win |
| 6 | 6 | O | `(row 5, col 6)` | `X X X . O O O` | `O` now has three in a row too (cols 4-6), but column 3 is not adjacent to it, so `O` cannot complete a four with this move |
| 7 | 3 | X | `(row 5, col 3)` | `X X X X O O O` | `check_win(board, 6, 7, 'X')` becomes `true`: cols 0-3 are all `X` -- the game ends here with `Player X wins!` |

This was confirmed by actually running the compiled reference binary with
that exact input and reading its stdout -- it is not a hand-simulated
guess.

---

## Task

Implement the four functions declared in `board.hpp`.

### `drop_piece`

Find the lowest empty row in `column` and place `piece` there. Return `true` on success, `false` if the column is already full (the top cell, row 0, is not `'.'`). `main.cpp` already validates that `column` is in range (`0` to `cols - 1`) before calling `drop_piece`, so you do not need to guard against an out-of-range column yourself.

**Examples** (using the main example board above, `rows = 6`, `cols = 7`):

- **Example (empty column):** `drop_piece(board, 6, 7, 6, 'O') == true`,
  landing at **`(row 5, col 6)`** since column 6 is completely empty.
- **Error case (full column):** `drop_piece(board, 6, 7, 0, 'X') == false`,
  since column 0's top cell `(row 0, col 0)` is already `'O'` -- **the
  board is left unchanged**.
- **Tricky case (stacking):** `drop_piece(board, 6, 7, 4, 'X') == true`,
  landing at **`(row 3, col 4)`** -- column 4 already has two pieces
  stacked, so the new one lands on top of them, not at the bottom.

### `check_win`

Return `true` if `piece` has four consecutive copies anywhere on the board. Check all four directions: horizontal, vertical, diagonal (top-left to bottom-right), and anti-diagonal (top-right to bottom-left). A run of exactly four is sufficient; longer runs also count.

**Examples:**

- **Example (horizontal/diagonal/anti-diagonal wins):** on the four
  positive win boards above, `check_win(board, 6, 7, 'X')` is **`true`**
  for the horizontal board (`X X X X` at cols 0-3 of row 5), the
  diagonal board, and the anti-diagonal board.
- **Example (vertical win):** `check_win(board, 6, 7, 'O')` is **`true`**
  for the vertical board (`O` stacked at rows 2-5 of column 2).
- **Tricky case (three-in-a-row is not enough):** on the main example
  board, `check_win(board, 6, 7, 'X') == false` even though `X` has a
  three-long diagonal run at `(row 2, col 2)`, `(row 3, col 3)`,
  `(row 4, col 4)` -- a run of three is not enough, and the cell that
  would extend it to four, `(row 5, col 5)`, is `'O'`.

### `is_full`

Return `true` if no cell on the board equals `'.'`.

**Examples:**

- **Empty-input case:** on a freshly created board (every cell `'.'`),
  `is_full(board, 6, 7) == false`.
- **Example:** on the main example board above,
  `is_full(board, 6, 7) == false` (column 6 is entirely empty).
- **Edge case (full vs. won are independent):** only a board where every
  one of the 42 cells has been played on returns `true` -- `main.cpp`
  always checks `check_win` before `is_full`, so a full board that also
  happens to contain four-in-a-row is reported as **a win, not a draw**.

### `computer_move`

Return the column the computer should play. Use this three-priority decision procedure, in order:

1. If the computer can win immediately by playing some column, play that column (lowest index wins if multiple columns work).
2. If the human can win next turn by playing some column, block that column (lowest index wins ties).
3. Otherwise, play the non-full column closest to center (`cols / 2`). Among columns equally close to center, prefer the lower-indexed one.

To check whether a column leads to a win, simulate: call `drop_piece` on a copy of the board, then call `check_win`. Do not use randomness -- the AI must be fully deterministic (given the same board, it must always choose the same move).

**Examples** (see the four scenario boards above for the full boards):

- **Example (board A, win available):** `computer_move` on board A (`O`
  three-in-a-row with two ways to complete it) `== 1` -- priority 1
  fires, and of the two winning columns (`1` and `5`), **the lower
  index wins**.
- **Example (board B, must block):** `computer_move` on board B (`X`
  three-in-a-row, no computer win available) `== 0` -- priority 1 finds
  nothing, priority 2 blocks the lower-indexed of the two threats (`0`
  and `4`).
- **Edge case (empty board):** `computer_move` on an empty board `== 3`
  -- priorities 1 and 2 find nothing (no pieces at all), so priority 3's
  center heuristic picks `cols / 2 == 3`.
- **Tricky case (center full, tie-break):** `computer_move` on board C2
  (center column full, alternating pieces, no win available for either
  side) `== 2` -- priority 3 falls back to the closest remaining column
  to center; columns 2 and 4 are equally close, and the tie goes to the
  lower index.

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
| `drop_piece` | 15 |
| `is_full` | 10 |
| `check_win` -- all four directions | 25 |
| `computer_move` -- all three priorities | 30 |
| Integration: full game scripted tests | 10 |
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
