# Pointer Matrix

## Overview

You will implement a small 2D matrix library using a flat, one-dimensional
array of integers.  The twist: the subscript operator `[]` is forbidden.
Every element access must go through pointer arithmetic and explicit
dereference (using `*` on a pointer to read or write the value it points to,
rather than the pointer's address itself).

This forces you to confront how 2D data is actually stored in memory,
why "array of pointers" (`int**`) is usually the wrong representation for a
dense matrix, and how `const` on a pointer differs from `const` on the data
the pointer points to.  These are the exact concepts that trip up C++
programmers for years if never addressed head-on.

---

## Learning goals

- Store a 2D matrix in a flat array and derive the row-major offset formula (`r * cols + c`)
- Use pointer arithmetic (`*(ptr + offset)`) as the exclusive alternative to `[]`
- Distinguish the four combinations of `const` and `*` in pointer declarations
- Write functions that signal read-only intent with `const int*` vs mutable intent with `int*`

## Background: what you need to know before you start

### How a 2D matrix is stored in a flat array

A matrix with `rows` rows and `cols` columns contains `rows * cols` integers.
We store them in **row-major order**: all elements of row 0 come first, then
all of row 1, and so on.

```
Matrix (3 rows, 4 cols):
  [ 1  2  3  4 ]   row 0
  [ 5  6  7  8 ]   row 1
  [ 9 10 11 12 ]   row 2

In memory (one flat block):
  index:  0  1  2  3  4  5  6  7  8  9 10 11
  value:  1  2  3  4  5  6  7  8  9 10 11 12
```

Element at row `r`, column `c` lives at **offset `r * cols + c`** from the
start of the array.  That is the one formula you need to derive everything
else.

### Why `int*`, not `int**`?

A beginner might reach for `int**` -- a pointer to a pointer -- to represent
a 2D matrix.  That representation looks like this:

```
int** m  -->  [ ptr0 | ptr1 | ptr2 ]    (array of pointers)
                |       |       |
                v       v       v
              [1 2 3 4] [5 6 7 8] [9 10 11 12]   (separate heap allocations)
```

This works, but it has real costs:

1. **Two levels of indirection.**  To read `m[r][c]` the CPU must first chase
   the outer pointer to find the row pointer, then chase the row pointer to
   find the element.  Two memory fetches, not one.
2. **Poor cache behavior.**  The CPU cache is a small, very fast block of
   memory that automatically keeps a copy of recently used data so the CPU
   does not have to wait on slower main memory every time.  It works best
   when the data you access next is physically close to the data you just
   accessed.  Each row here is a separate heap allocation that can live
   anywhere in memory.  Iterating across rows means jumping around in the
   heap -- a "cache miss" (the CPU cache does not have the data ready and
   must fetch it from slower memory) at every row boundary.
3. **More space.**  You allocate one extra array of `rows` pointers on top of
   the data itself.
4. **More bookkeeping.**  You must allocate and free each row individually.

A flat `int*` is strictly better for a dense, fixed-size matrix:
- One allocation, one free.
- All elements are contiguous -- the CPU prefetcher (hardware that guesses
  which memory you will read next and fetches it ahead of time) loves this.
- No extra pointer indirection.
- The only cost is that you compute `r * cols + c` yourself instead of letting
  `[][]` hide it.

### Pointer arithmetic and why `[]` is sugar

In C++ the expression `arr[i]` is **exactly** equivalent to `*(arr + i)`.
The compiler rewrites one to the other; they produce identical machine code.
`[]` is syntactic sugar, not a different operation.

Since `[]` is just `*( + )` in disguise, forbidding `[]` forces you to write
the pointer arithmetic explicitly, which makes the mental model concrete.

### `const` and pointers -- four combinations

When `const` appears with pointers there are four distinct meanings.  Read
carefully: the position of `const` relative to `*` is what matters.

```cpp
int x = 5;

int*             p1 = &x; // can change where p1 points; can change *p1
const int*       p2 = &x; // can change where p2 points; CANNOT change *p2
int* const       p3 = &x; // CANNOT change where p3 points; can change *p3
const int* const p4 = &x; // CANNOT change either
```

A memory trick: read right-to-left.
- `const int*` -- "pointer to const int" -- the int is const.
- `int* const` -- "const pointer to int" -- the pointer is const.

In this assignment many functions take `const int* m`.  That tells the caller:
"I will only read from your matrix, not modify it."  This is the correct
practice: receive read-only data as `const T*`, not `T*`.

### `const` and references

References have the same two layers of `const`:

```cpp
int x = 5;

int&       r1 = x; // can rebind r1 (well -- you can't, ever); can change x via r1
const int& r2 = x; // can ONLY READ through r2; cannot change x via r2
```

In practice, `const int& r` shows up in function parameters to receive a
large object cheaply (no copy) while promising not to modify it.  For a
single `int` it makes no difference; for a large struct it matters.

### References: aliases, not just "safer pointers"

A reference (`int& r = x`) is an **alias** -- another name for the same
object.  Several things are different from pointers:

- **Cannot be null.**  A reference always refers to a valid object.
- **Cannot be rebound.**  Once `int& r = x` is written, `r = y` does NOT make
  `r` refer to `y` -- it COPIES the value of `y` into `x`.  You cannot make a
  reference point somewhere else after initialization.
- **No `vector<T&>`.**  Because references cannot be rebound (and therefore
  cannot be default-constructed or copy-assigned the way vector elements
  must be), the standard library forbids `vector<T&>`.  Use `vector<T*>` or
  `vector<std::reference_wrapper<T>>` if you need a container of references.

**For the astute:** Under the hood a reference *may* be implemented as a
pointer by the compiler -- but it is not *required* to be.  The C++ standard
says only that a reference is an alias; it says nothing about how that alias is
represented.  The compiler may optimize a reference away entirely (storing
nothing at runtime) or may store it as a pointer.  You cannot take the address
of a reference itself, so you can never observe which representation was chosen.
This is why we call references *aliases* rather than *pointer wrappers*.

### Best practice: no out-parameter pointers

A function that needs to return a value should **return it**, not receive a
`T*` parameter and fill it in.  The out-pointer pattern is error-prone:

```cpp
// Bad: forces caller to create a variable, easy to pass null accidentally
void get_value(int row, int col, int* result);

// Good: just return the value
int get_value(int row, int col);
```

All nine functions in this assignment follow the good pattern.  The only
pointer parameters are the matrices being operated on, not "output slots"
for single values.

---

## Examples at a glance

To make all nine functions concrete, here is **one** representative matrix,
`m`, with 3 rows and 4 columns, and what every function produces for it.
Read this table first -- it is the whole assignment in miniature.

```
Matrix m (rows = 3, cols = 4):
  [ 1  2  3  4 ]   row 0
  [ 5  6  7  8 ]   row 1
  [ 9 10 11 12 ]   row 2

Flat storage:
  index:  0  1  2  3  4  5  6  7  8  9 10 11
  value:  1  2  3  4  5  6  7  8  9 10 11 12
```

| Call | Returns / effect | Why |
|------|-------------------|-----|
| `mat_get(m, 4, 0, 0)`        | `1`  | offset `0*4+0 = 0`, the very first flat element |
| `mat_get(m, 4, 1, 2)`        | `7`  | offset `1*4+2 = 6`, and flat index 6 holds `7` |
| `mat_get(m, 4, 2, 3)`        | `12` | offset `2*4+3 = 11`, the last flat element |
| `mat_set(m, 4, 1, 2, 99)` then `mat_get(m, 4, 1, 2)` | `99` | `mat_set` writes to the same offset formula `mat_get` reads from -- the two functions are mirror images |
| `mat_fill(m, 3, 4, 0)` then any `mat_get(m, 4, r, c)` | `0`  | `mat_fill` overwrites all `rows*cols = 12` flat elements, so every subsequent read returns the fill value |
| `mat_add(m, b, dst, 3, 4)` where `b` is all `100`s | `dst` = `{101,102,...,112}` row-major | element-wise: `dst[i] = m[i] + b[i]` on the flat array, no need to know rows/cols separately from the total count |
| `mat_transpose(m, dst, 3, 4)` | `dst` (4 rows x 3 cols) = rows `{1,5,9}`, `{2,6,10}`, `{3,7,11}`, `{4,8,12}` | `dst` has `cols` rows and `rows` columns -- the ORIGINAL COLUMNS of `m` become the rows of `dst` |
| `mat_row_sum(m, 4, 0)`       | `10` | `1+2+3+4` |
| `mat_row_sum(m, 4, 2)`       | `42` | `9+10+11+12` |
| `mat_col_sum(m, 3, 4, 0)`    | `15` | `1+5+9`, stepping by `cols` each row |
| `mat_col_sum(m, 3, 4, 3)`    | `24` | `4+8+12`, the last column |
| `mat_print(m, 3, 4)`         | prints `1 2 3 4` / `5 6 7 8` / `9 10 11 12` (three lines) | one row per line, single spaces between elements, no trailing space |

`mat_is_symmetric` requires a SQUARE matrix, so `m` above (3x4) does not
qualify -- here is a separate 3x3 matrix `s` for it:

```
s (n = 3):
  [ 1  2  3 ]
  [ 2  4  5 ]
  [ 3  5  6 ]
```

| Call | Returns | Why |
|------|---------|-----|
| `mat_is_symmetric(s, 3)` | `true`  | `s[0][1]==s[1][0]==2`, `s[0][2]==s[2][0]==3`, `s[1][2]==s[2][1]==5` -- every mirrored pair matches |
| `mat_is_symmetric(m2, 2)` where `m2 = {1, 2, 3, 4}` | `false` | `m2[0][1] = 2` but `m2[1][0] = 3` -- they differ, so the function returns `false` on this first mismatched pair |
| `mat_is_symmetric(m3, 1)` where `m3 = {5}` | `true`  | a 1x1 matrix has no off-diagonal pairs to compare, so it is trivially symmetric |

## Worked example: watch `mat_get(m, 4, 2, 3)` turn into an address, step by step

This is the single most important thing to understand in the assignment, so
here is every step spelled out. We are reading row `r = 2`, column `c = 3` of
the same matrix `m` from above (3 rows, 4 columns, flat values `1..12`).
Suppose the flat array starts at address `m = 0x1000`, and (as on almost
every real machine) `sizeof(int) == 4` bytes.

| Step | Expression | Computes to | Why |
|------|------------|-------------|-----|
| 1. Row offset | `r * cols` = `2 * 4` | `8` | rows 0 and 1 have 4 elements each, so row 2's first element is 8 flat positions past the start |
| 2. Column offset | `r * cols + c` = `8 + 3` | `11` | within row 2, column 3 is 3 more positions past that row's start |
| 3. Pointer arithmetic | `m + 11` | address `0x1000 + 11*4` = `0x102C` | `m + 11` in C++ means "11 `int`s past where `m` points," not "11 bytes past" -- the compiler automatically scales the offset by `sizeof(int)`, which is exactly why raw pointer arithmetic is type-aware |
| 4. Dereference | `*(m + 11)` | `12` | reading the 4 bytes stored at address `0x102C` yields the `int` value `12` -- row 2, column 3 of the matrix |

So `mat_get(m, 4, 2, 3)` returns `12`, matching flat index 11 in the array
above. Notice this is exactly the offset formula from the Background
section (`r * cols + c`) computed as pointer arithmetic instead of `[]` --
`*(m + r*cols + c)` and `m[r*cols + c]` produce identical machine code, but
only the pointer-arithmetic form is legal in this assignment's `matrix.cpp`.

---

## Task

Submit a single file `matrix.cpp` that implements the nine functions declared
in `matrix.hpp`.  You may not modify `matrix.hpp`.

### Function contracts

**`int mat_get(const int* m, int cols, int r, int c)`**
Return the value at row `r`, column `c` of matrix `m`.
`cols` is the number of columns per row.
You may assume `r` and `c` are in bounds.
The `const int*` parameter signals that this function is read-only.

- **Example (first element):** for `m = {1,2,3,4,5,6,7,8,9,10,11,12}` (3
  rows, 4 cols), `mat_get(m, 4, 0, 0)` is **`1`**.
- **Example (interior element):** `mat_get(m, 4, 1, 2)` is **`7`**.
- **Example (last element):** `mat_get(m, 4, 2, 3)` is **`12`**.

**`void mat_set(int* m, int cols, int r, int c, int val)`**
Set the element at row `r`, column `c` to `val`.
No return value; the matrix is modified in place.

- **Example (overwrite):** `mat_set(m, 4, 1, 2, 99)` followed by
  `mat_get(m, 4, 1, 2)` returns **`99`** (it overwrote the `7` from the
  example above).
- **Example (negative value):** `mat_set(m, 4, 0, 3, -1)` followed by
  `mat_get(m, 4, 0, 3)` returns **`-1`** -- negative values are stored the
  same way as positive ones, there is nothing special about them.

**`void mat_fill(int* m, int rows, int cols, int val)`**
Set every element in the matrix to `val`.
Both `rows` and `cols` are needed to know the total element count.

- **Example (whole matrix):** `mat_fill(m, 3, 4, 0)` on the 12-element
  matrix above sets **all 12 flat elements to `0`**, so every subsequent
  `mat_get(m, 4, r, c)` returns `0`.
- **Edge case (1x1 matrix):** `mat_fill(m, 1, 1, 7)` on a 1x1 matrix sets
  its single element to `7` -- the smallest possible matrix still works
  since **`rows*cols` is just `1`**.

**`void mat_add(const int* a, const int* b, int* dst, int rows, int cols)`**
Element-wise addition: `dst[r][c] = a[r][c] + b[r][c]` for every cell.
`a` and `b` are read-only; `dst` is written.
All three matrices have the same dimensions.

- **Example (basic add):** `a = {1,2,3,4}`, `b = {10,20,30,40}` (both
  2x2), `mat_add(a, b, dst, 2, 2)` gives **`dst = {11,22,33,44}`**.
- **Edge case (add zero):** if every element of `b` is `0`, `dst` ends up
  **identical to `a`** -- adding zero changes nothing.

**`void mat_transpose(const int* src, int* dst, int rows, int cols)`**
Write the transpose of `src` into `dst`.
`src` has `rows` rows and `cols` columns.
`dst` must have `cols` rows and `rows` columns (the caller allocates it).
Element `(r, c)` of `src` maps to element `(c, r)` of `dst`.

This is the most common wrong-answer trap in this assignment.  Think carefully:
if `src` has 3 rows and 5 columns, `dst` has 5 rows and 3 columns.  The offset
formula for `dst` uses `rows` (the original row count) as its column count,
not `cols`.

- **Example (square case):** `src = {1,2,3,4}` (2x2),
  `mat_transpose(src, dst, 2, 2)` gives `dst = {1,3,2,4}` -- rows
  **`{1,3}`** and **`{2,4}`**.
- **Example (non-square case):** `src = {1,2,3,4,5,6}` (2 rows, 3 cols),
  `mat_transpose(src, dst, 2, 3)` gives `dst = {1,4,2,5,3,6}` -- **3 rows,
  2 cols**: `{1,4}`, `{2,5}`, `{3,6}`.
- **Example (3x4 matrix `m`):** `mat_transpose(m, dst, 3, 4)` gives a
  **4x3 result** with rows `{1,5,9}`, `{2,6,10}`, `{3,7,11}`, `{4,8,12}`
  -- the original COLUMNS of `m` become the rows of `dst`.

**`int mat_row_sum(const int* m, int cols, int r)`**
Return the sum of all elements in row `r`.
Only `cols` is needed, not `rows`, because you only access one row.

- **Example (first row):** for the 3x4 matrix `m` above,
  `mat_row_sum(m, 4, 0)` is **`10`** (`1+2+3+4`).
- **Example (last row):** `mat_row_sum(m, 4, 2)` is **`42`**
  (`9+10+11+12`).

**`int mat_col_sum(const int* m, int rows, int cols, int c)`**
Return the sum of all elements in column `c`.
Both `rows` and `cols` are needed to step from one row to the next.

- **Example (first column):** for the same 3x4 matrix `m`,
  `mat_col_sum(m, 3, 4, 0)` is **`15`** (`1+5+9`).
- **Example (last column):** `mat_col_sum(m, 3, 4, 3)` is **`24`**
  (`4+8+12`).

**`bool mat_is_symmetric(const int* m, int n)`**
`m` is a square `n x n` matrix.
Return `true` if `m[r][c] == m[c][r]` for all `r` and `c`.
Return `false` on the first pair that differs.

- **Example (symmetric):** `s = {1,2,3,2,4,5,3,5,6}` (3x3),
  `mat_is_symmetric(s, 3)` is **`true`**.
- **Example (not symmetric):** `m2 = {1,2,3,4}` (2x2),
  `mat_is_symmetric(m2, 2)` is **`false`** (`m2[0][1] = 2` but
  `m2[1][0] = 3`).
- **Edge case (1x1 matrix):** `m3 = {5}` (1x1), `mat_is_symmetric(m3, 1)`
  is **`true`** -- a single element has no off-diagonal pair to fail, so
  it is trivially symmetric.

**`void mat_print(const int* m, int rows, int cols)`**
Print the matrix, one row per line, elements separated by spaces.
The last element on a line has no trailing space.
Use `printf` or `std::cout`; either is fine.

- **Example (3x4 matrix):** `mat_print(m, 3, 4)` on the 3x4 matrix above
  prints exactly **three lines**, `"1 2 3 4"`, `"5 6 7 8"`,
  `"9 10 11 12"`, each followed by a newline and none with a trailing
  space.
- **Edge case (single row):** `mat_print(row, 1, 3)` on a single-row
  matrix `row = {7,8,9}` prints **one line**, `"7 8 9"`.

Example for a 2x3 matrix with values 1-6:
```
1 2 3
4 5 6
```

---

## Files

| File | What to do |
|------|------------|
| `matrix.hpp` | Provided; do not modify |
| `matrix.cpp` | Write your implementation here |

---

## Constraints

**You may not use `[]` anywhere in `matrix.cpp`.**
The autograder checks this with a source scan.  Every element access must use
pointer arithmetic and explicit dereference: `*(ptr + offset)`.

You may use standard headers (`<cstdio>`, `<iostream>`, `<cstring>`, etc.).
You may not use STL (Standard Template Library) containers (`std::vector`, `std::array`, etc.); all
matrices are passed in as raw `int*` pointers allocated by the caller.

---

## Compilation and testing

```bash
mkdir build && cd build
cmake .. -DSUBMISSION_DIR=$(pwd)/../assets
cmake --build .
./pointer-matrix_tests
```

Or, without CMake:

```bash
g++ -std=c++17 -Wall -Wextra -o tests \
    visible-tests/test_visible.cpp assets/matrix.cpp \
    -I assets
./tests
```

---

## Grading

| Component | Points |
|-----------|--------|
| `mat_get` and `mat_set` | 15 |
| `mat_fill` | 5 |
| `mat_add` | 10 |
| `mat_transpose` (square) | 10 |
| `mat_transpose` (non-square) | 10 |
| `mat_row_sum` and `mat_col_sum` | 15 |
| `mat_is_symmetric` | 10 |
| `mat_print` | 5 |
| No `[]` (source check) | 20 |
| **Total** | **100** |

## Submission

Submit a single file named `matrix.cpp`. Do not rename it and do not submit
`matrix.hpp`.

## Going further

- Add a `mat_multiply(const int* a, const int* b, int* dst, int n)` function
  for square n x n matrices. Benchmark the naive O(n^3) version against a
  cache-friendly loop-reordering (k-j-i instead of i-j-k).
- Implement the same nine functions using `std::vector<int>` with `operator[]`.
  Compare the code. Which version is clearer? Which is safer?
- Compile with `-fsanitize=address` and deliberately pass wrong row/col counts
  to `mat_transpose`. Read the report from ASan (AddressSanitizer, a compiler
  tool that detects out-of-bounds memory accesses at runtime) to understand
  what it catches.
