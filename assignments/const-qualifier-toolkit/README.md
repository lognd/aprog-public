# Const Qualifier Toolkit

`const` is a contract between you and your caller. When a function takes
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

## Task

A 2D grid of `char` is stored as a flat array in row-major order. The element
at row `r` and column `c` in a grid with `cols` columns is:

```
grid[r * cols + c]
```

Implement all 13 functions declared in `grid.hpp`. The header is locked -- do
not modify it. Each function's contract is documented in comments there; read
them before implementing.

The functions split into four groups:

**Read-only** -- take `const char*` grid, never write through it:
`cell_at`, `cell_is`, `count_cells`, `grids_equal`, `row_contains`, `find_in_row`

**Pointer-into-grid** -- return a pointer directly into the array, not a copy.
The return type must match the input's const-ness:
`row_ptr` (returns `const char*` from `const char*`),
`row_ptr_mut` (returns `char*` from `char*`)

**Write** -- take `char*` grid, modify it:
`set_cell`, `fill_grid`, `fill_row`

**Mixed** -- `const char*` source, `char*` destination:
`copy_row`, `copy_grid`

## Files

| File | Purpose |
|------|---------|
| `grid.hpp` | Declarations and contracts -- do not modify |
| `grid.cpp` | Write your implementation here |
| `visible-tests/test_catch.cpp` | Visible Catch2 tests you can run locally |

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
