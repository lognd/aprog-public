# Const Qualifier Toolkit

`const` is a contract (a promise about behavior that both sides are expected to
honor) between you and your caller. When a function takes
`const char* grid`, it promises: "I will not touch your data." The compiler
enforces this promise -- but the real audience is the next programmer who reads
the signature and decides whether it is safe to pass in their read-only buffer.

In this assignment you implement a flat 2D character grid utility library.
Every function signature is already written for you in `grid.hpp`; your job is
to implement the bodies in `grid.cpp` without breaking the promises the header
makes. You will use this library again in the Connect Four assignment, where
the board is the same flat grid you build here.

---

## Learning goals

- Implement functions whose signatures use `const char*`, `char*`, `const char&`,
  and both const and non-const pointer return types
- Understand that `const` on a parameter is a promise to the caller, not an
  implementation detail
- Distinguish read-only input buffers (`const char*`) from writable output
  buffers (`char*`)
- Return a pointer directly into the original array with the correct const-ness
  (`row_ptr` vs. `row_ptr_mut`)
- Build the grid utility you will reuse in the Connect Four assignment

## Examples: every function on one grid

To make all 13 functions concrete, here is **one** 3x3 grid, with the flat
index of every cell written above it, and what each function does or returns
for it. Read this table first -- it is the whole assignment in miniature.

```
 flat index:   0    1    2    3    4    5    6    7    8
 grid       = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'}

 as a 3x3 grid (row 0 first, then row 1, then row 2):
   row 0:  A B C
   row 1:  D E F
   row 2:  G H I
```

Assume `char grid[9] = {'A','B','C','D','E','F','G','H','I'};` (a plain,
non-const array -- so it can be passed to both `const char*` and `char*`
parameters), and `const char* cg = grid;` (a const-qualified VIEW of the same
9 bytes -- `cg` can only be passed where a `const char*` is expected).

| Call | Result | Why |
|------|--------|-----|
| `cell_at(cg, 3, 0, 0)` | `'A'` | flat index is `0*3 + 0 = 0`, and `grid[0]` is `'A'` |
| `cell_at(cg, 3, 1, 1)` | `'E'` | flat index is `1*3 + 1 = 4`, and `grid[4]` is `'E'` |
| `cell_is(cg, 3, 0, 2, 'C')` | `true` | `grid[0*3+2]` is `'C'`, which equals the target `'C'` |
| `count_cells(cg, 3, 3, 'A')` | `1` | only index 0 holds `'A'` |
| `grids_equal(cg, cg, 3, 3)` | `true` | comparing the grid to itself, cell by cell, always matches |
| `row_contains(cg, 3, 1, 'F')` | `true` | row 1 is `D E F`, and `F` is in it |
| `find_in_row(cg, 3, 2, 'H')` | `1` | row 2 is `G H I`; `H` is at column 1 within that row |
| `find_in_row(cg, 3, 2, 'Z')` | `-1` | row 2 has no `Z` |
| `row_ptr(cg, 3, 1)` | pointer equal to `grid + 3`, pointing at `'D'` | row 1 starts at flat index `1*3 = 3`; the returned pointer is `const char*` because the input was `const char*` |
| `row_ptr_mut(grid, 3, 1)` | pointer equal to `grid + 3`, pointing at `'D'`, WRITABLE | same arithmetic as `row_ptr`, but the return type is `char*` because the input `grid` was non-const |
| `set_cell(grid, 3, 2, 2, 'Q')` | `grid[8]` becomes `'Q'` | flat index `2*3+2 = 8`; `set_cell` needs `char*` because it writes |
| `fill_row(grid, 3, 0, 'X')` | row 0 becomes `X X X` | writes `'X'` into flat indices 0, 1, 2 |
| `fill_grid(grid, 3, 3, '.')` | every one of the 9 cells becomes `'.'` | writes `'.'` into every flat index 0 through 8 |
| `copy_row(cg, 3, 2, dst)` (`dst` a separate 3-char buffer) | `dst` becomes `{'G','H','I'}` | copies row 2 out of the const source `cg` into the writable destination `dst` |
| `copy_grid(cg, dst9, 3, 3)` (`dst9` a separate 9-char buffer) | `dst9` becomes an exact copy of `grid` | reads every cell from const `cg`, writes every cell into non-const `dst9` |
| `set_cell(cg, 3, 0, 0, 'Z')` | **does not compile** | `cg` is `const char*`; `set_cell` requires `char*` because it writes -- passing a const pointer where a non-const one is required is exactly the promise `const` exists to enforce |
| `char* p = row_ptr(cg, 3, 1);` | **does not compile** | `row_ptr` returns `const char*`; you cannot silently drop `const` when assigning to a `char*` variable |

## Worked example: watch const-correctness get checked, step by step

This is the single most important thing to understand in the assignment, so
here is every step spelled out, using the same 9-byte grid from above.

```cpp
char grid[9] = {'A','B','C','D','E','F','G','H','I'};
const char* cg = grid;   // cg is a read-only VIEW of the same bytes
```

| Step | Code | Compiles? | Why |
|------|------|-----------|-----|
| 1 | `char a = cell_at(cg, 3, 0, 0);` | Yes | `cell_at` takes `const char*`; a `const char*` argument satisfies a `const char*` parameter -- reading never needs write access |
| 2 | `char a = cell_at(grid, 3, 0, 0);` | Yes | a plain (non-const) `char*` can ALSO be passed anywhere a `const char*` is expected -- non-const is always a superset of what const requires. This is why the read-only functions accept `grid` directly, no cast needed |
| 3 | `set_cell(cg, 3, 0, 0, 'Z');` | **No** | `set_cell` takes `char*` because it writes through the pointer; `cg`'s type is `const char*`, and C++ will not silently let you promise-break by widening a const pointer into a non-const one |
| 4 | `set_cell(grid, 3, 0, 0, 'Z');` | Yes | `grid` is genuinely non-const, so `set_cell` may write through it; after this line `grid[0]` is `'Z'` |
| 5 | `const char* r = row_ptr(cg, 3, 1);` | Yes | `row_ptr` takes and returns `const char*`; the types line up exactly |
| 6 | `r[0] = 'Y';` (continuing from step 5) | **No** | `r` is `const char*` -- the pointer itself promises not to write through it, so indexing into it for a write is rejected at compile time, even though the underlying `grid` array is not const |
| 7 | `char* rm = row_ptr_mut(grid, 3, 1);` | Yes | `row_ptr_mut` takes `char*` and returns `char*`; `grid` is non-const, so this matches exactly |
| 8 | `rm[0] = 'Y';` (continuing from step 7) | Yes | `rm` is `char*`, a genuinely writable pointer into `grid`; after this line `grid[3]` (row 1's first cell) is `'Y'` |
| 9 | `char* rm2 = row_ptr(grid, 3, 1);` | **No** | even though `grid` is non-const, `row_ptr` still RETURNS `const char*` (that is its declared return type, always) -- you cannot assign a `const char*` result into a plain `char*` variable without a cast |

The pattern across every failing step (3, 6, 9): `const` on a pointer is a
one-way street. A non-const pointer can always be used where a const one is
expected (steps 2 and 4), because that never breaks the "I will not write
through this" promise. Going the other direction -- using a const pointer, or
a function's const-typed return value, somewhere a non-const one is required
-- is exactly the mistake `const` exists to catch, and the compiler refuses
it every time (steps 3, 6, 9). All nine steps above were compiled against the
reference solution's `grid.cpp` to confirm this: steps 1, 2, 4, 5, 7, 8
compile and run as described; steps 3, 6, 9 fail to compile with
`invalid conversion from 'const char*' to 'char*'` (steps 3 and 9) or
`assignment of read-only location` (step 6).

---

## Task

A 2D grid of `char` is stored as a flat (one-dimensional) array in row-major
order -- meaning each row's characters are laid out one after another in
memory, row 0 in full, then row 1 in full, and so on. The element at row `r`
and column `c` in a grid with `cols` columns is:

```
grid[r * cols + c]
```

Implement all 13 functions declared in `grid.hpp`. The header is locked -- do
not modify it. Each function's contract is documented in comments there; read
them before implementing. Every example below reuses the same 3x3 grid
`{'A','B','C','D','E','F','G','H','I'}` (row 0 = `A B C`, row 1 = `D E F`,
row 2 = `G H I`) from the table above, with `grid` as a plain (non-const)
array and `cg` as a `const char*` pointing at the same bytes.

The functions split into four groups:

**Read-only** -- take `const char*` grid, never write through it:
`cell_at`, `cell_is`, `count_cells`, `grids_equal`, `row_contains`, `find_in_row`

- **Example:** `cell_at(cg, 3, 1, 1) == 'E'`. These functions accept
  either `cg` (`const char*`) or `grid` (`char*`) as their first
  argument -- a non-const pointer can always be passed where const is
  expected, so `cell_at(grid, 3, 1, 1)` compiles too.
- **No writing tricky case here** -- these functions never take a
  `char*` parameter at all.

**Pointer-into-grid** -- return a pointer directly into the array, not a copy.
The return type must match the input's const-ness:
`row_ptr` (returns `const char*` from `const char*`),
`row_ptr_mut` (returns `char*` from `char*`)

- **Example:** `row_ptr(cg, 3, 1)` returns a `const char*` equal to
  `grid + 3` (row 1's start); `row_ptr_mut(grid, 3, 1)` returns a
  `char*` equal to the same address, but **writable**.
- **Error case (dropping const):** `char* p = row_ptr(cg, 3, 1);` does
  **not** compile -- `row_ptr` always returns `const char*`, and you
  cannot assign that into a plain `char*` variable without a cast (and
  this assignment forbids `const_cast`, so there is no legal way
  around it -- call `row_ptr_mut` on a non-const grid instead if you
  need a writable row pointer).

**Write** -- take `char*` grid, modify it:
`set_cell`, `fill_grid`, `fill_row`

- **Example:** `set_cell(grid, 3, 0, 0, 'Z')` sets `grid[0]` to `'Z'`.
- **Error case (const source):** `set_cell(cg, 3, 0, 0, 'Z')` does
  **not** compile -- `cg` is `const char*`, and `set_cell` needs
  `char*` to legally write; passing a const pointer where a write is
  required is precisely the violation `const` is designed to catch.
- **Error case (same rule, `fill_row`):** `fill_row(grid, 3, 0, 'X')`
  sets row 0 to `X X X`; `fill_row(cg, 3, 0, 'X')` fails to compile for
  the identical reason.

**Mixed** -- `const char*` source, `char*` destination:
`copy_row`, `copy_grid`

- **Example:** `copy_row(cg, 3, 2, dst)` (with `dst` a separate
  writable 3-char buffer) reads row 2 (`G H I`) from the const source
  `cg` and writes it into `dst`, leaving `dst == {'G','H','I'}`.
- **Error case (swapped arguments):** `copy_row(dst, 3, 2, cg)` does
  **not** compile, because `cg`'s type, `const char*`, cannot be used
  as the fourth (`char* dst`) parameter, which must be writable.

## Files

| File | Purpose |
|------|---------|
| `grid.hpp` | Declarations and contracts -- do not modify |
| `grid.cpp` | Write your implementation here |
| `visible-tests/test_catch.cpp` | Visible tests you can run locally, written with Catch2 (a C++ library for writing and running automated test cases) |

## Compilation and Testing

Build and run the visible tests locally:

```bash
g++ -std=c++17 -Wall -Wextra -Werror \
    -I. grid.cpp visible-tests/test_catch.cpp \
    -o grid_tests
./grid_tests
```

You will need Catch2 installed, or you can fetch it via CMake. The grader
uses CMake internally; see `visible-tests/CMakeLists.txt` for details.

## Constraints

- Do not modify `grid.hpp`.
- Do not use `const_cast` anywhere in `grid.cpp`.
- `row_ptr` must return a pointer directly into `grid` -- not a copy of the
  data. The test suite verifies this with pointer comparison.
- `row_ptr_mut` performs the same pointer arithmetic as `row_ptr`; only the
  types differ.
- Do not use `std::string` or `std::vector`.

---

## Grading

| Component | Points |
|-----------|--------|
| Compilation clean at `-Wall -Wextra -Werror` | 0 (required to proceed) |
| No `const_cast` (source check) | 15 |
| Const-correctness at call site (compile-check) | 20 |
| Visible tests (Catch2) | 25 |
| Hidden tests (Catch2) | 40 |
| **Total** | **100** |

The compilation check is a gate: if your code does not compile, no further
tests run.

## Submission

Submit a single file named `grid.cpp`. Do not rename it.

---

## Going further

- Open a hex editor (or use `xxd`) and look at a raw `char` array in memory.
  Does the flat row-major layout match what you expect?
- Write a function `print_grid(const char* grid, int rows, int cols)` that
  prints the grid with spaces between columns. Note the parameter type.
- Compare `row_ptr` and `row_ptr_mut`. The bodies are identical -- only the
  types differ. Why does C++ require two separate functions instead of one?
  (Hint: look up function overloading on `const`.)
- In the Connect Four assignment, `check_win` will take `const char*` because
  checking for a win never mutates the board. Before you get there, write the
  signature on paper and check which of these 13 functions you would call inside
  it.
