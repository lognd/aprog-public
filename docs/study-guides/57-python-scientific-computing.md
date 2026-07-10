# Study Guide 57: Python Scientific Computing

This module builds the numpy mental model from first principles: an
array is a fixed-shape, fixed-dtype block of numbers packed
contiguously in memory, its operators are elementwise (not the same
operators a Python list overloads), broadcasting lets differently
shaped arrays combine by a strict axis-by-axis rule, and slicing
returns a view instead of a copy. `grade-matrix` then forces that
model into practice by mechanically forbidding `for`/`while` loops,
so all six grading functions must be written as vectorized numpy
expressions.

## Know before you start

- List slicing copies out elements into a new list, as the contrast
  case for why a numpy slice behaving differently (a view, not a
  copy) is surprising [assumed: row 48 -- Python Data Structures]
- `bool` is a subclass of `int` in Python, relevant to numpy's dtype
  and boolean-mask behavior [assumed: row 52 -- Python Types &
  Comprehensions]
- Type hints are promises the runtime never checks, and how to read
  a type-hinted function signature [assumed: row 53 -- Python
  Generics & Typing]
- Writing an explicit `for`/`while` loop over a collection, as the
  baseline being replaced by vectorized operations [assumed: row 6
  -- Control & Functions]

## Taught here

Concept: what a numpy array is
- Know a numpy array is a fixed-shape, fixed-dtype block of numbers
  stored contiguously in memory, closer to a C++ `int[]` or
  `std::vector<double>` than to a Python `list`, which is really an
  array of pointers to separately allocated objects.
- Know arithmetic operators (`+`, `-`, `*`, `/`) on two numpy arrays
  are elementwise: they pair up corresponding positions and combine
  them, running as pre-compiled C code over both underlying memory
  buffers rather than an interpreted Python-level loop.
- Know the same operator symbol means something different by type:
  `*` on two numpy arrays is elementwise multiplication, but `*` on
  a Python `list` and an `int` is repetition (concatenating N copies
  of the list), not arithmetic.
- Know VECTORIZATION is expressing a computation as one operation
  over a whole array instead of an explicit loop over its elements,
  letting compiled code do the iterating instead of the Python
  interpreter.
- Know every numpy array has one fixed dtype for all of its
  elements, unlike a Python list, which can mix types because each
  slot is a pointer to a separately typed object.
- Know DTYPE PROMOTION: combining two arrays of different numeric
  dtypes (e.g. `int` and `float64`) in an arithmetic operation
  produces a result in a single dtype able to represent both without
  losing information (e.g. promoting to `float64` rather than
  truncating the float side).

Concept: broadcasting
- Know BROADCASTING is numpy's rule for combining arrays of
  different but compatible shapes in an elementwise operation
  without an explicit loop or manual resizing.
- Know the broadcasting rule compares two shapes axis by axis
  starting from the rightmost (last) axis: each pair of axes must be
  either equal or one of them must be exactly 1 (the size-1 axis is
  conceptually stretched to match, with no memory actually copied).
- Know a broadcast fails (raises an error) at the first axis pair,
  scanning from the right, that is neither equal nor has a 1 on
  either side -- it does not fall back to either operand's shape.
- Be able to predict the resulting shape of a broadcasted operation
  by comparing two shape tuples axis by axis from the right.
- Know a `(3, 1)` array times a `(1, 4)` array broadcasts to `(3,
  4)`, stretching one column across four columns and one row across
  three rows before combining -- an outer-product-like pattern with
  no nested loop.

Concept: views vs. copies, boolean masking, per-axis reductions
- Know slicing a numpy array (`a[1:3]`) returns a VIEW: a new array
  object sharing the same underlying memory as the original, with no
  element data copied -- the opposite of Python list slicing, which
  copies. Mutating a view mutates the original array.
- Know `a[1:3].copy()` is required to get an independent copy of a
  numpy slice.
- Know comparison operators (`>`, `<`, `==`, etc.) on a numpy array
  are also elementwise, producing a same-shaped array of booleans
  called a BOOLEAN MASK.
- Know indexing an array with a same-shaped boolean mask
  (`scores[mask]`) keeps only the positions where the mask is
  `True`, dropping the rest entirely (not zeroing them) -- numpy's
  standard filtering idiom, replacing an explicit append-if loop.
- Know AXIS numbering starts at 0: for a 2-D array, axis 0 is the
  row axis and axis 1 is the column axis.
- Know `.sum(axis=0)` (or `.mean`, `.std`) collapses axis 0,
  producing one result per remaining column (summing/averaging down
  each column); `axis=1` collapses the column axis instead,
  producing one result per row.
- Know `.sum()` with no `axis` argument collapses every axis to a
  single number.

Concept: writing loop-free numpy code under a hard constraint
- Be able to compute a per-row or per-column mean/std with `.mean`/
  `.std` and the correct `axis=` instead of an explicit loop.
- Be able to add a per-column offset to every row of a matrix in one
  broadcasted expression (a `(n,)` or `(1, n)` array added to an
  `(m, n)` matrix).
- Be able to build a pass/fail boolean mask from a comparison
  operator on a reduction's result, with no `if` inside a loop.
- Be able to guard a division by a per-column value that may be zero
  using `np.where` (or an equivalent guard) instead of a loop with a
  conditional inside it, avoiding both a `ZeroDivisionError`-style
  crash and a silent numpy division warning.
- Be able to use `.min(axis=...)` combined with a sum and a
  broadcasted subtraction to compute a "drop the lowest value" mean
  without a loop, handling the single-column edge case (nothing left
  to average) as a special-cased return value rather than a division
  by zero.

## Study checklist

- [ ] Explain why `a * b` on two numpy arrays differs from `lst * 3`
      on a Python list, given the same `*` symbol.
- [ ] State the broadcasting rule and use it to predict whether two
      given shapes combine, and if so, what shape results.
- [ ] Explain why `a[1:3]` on a numpy array is a view while `lst[1:3]`
      on a Python list is a copy, and what that implies for mutation.
- [ ] Trace `scores > threshold` and `scores[scores > threshold]` as
      two separate elementwise steps: comparison, then mask indexing.
- [ ] Given a 2-D array, state which axis `axis=0` vs `axis=1`
      collapses in a reduction, and predict the output shape.
- [ ] Explain what dtype promotion does when adding an int array and
      a float array.
- [ ] Rewrite a simple loop-based row/column computation (mean,
      threshold mask, per-column offset) as a vectorized numpy
      expression with no `for`/`while`.
- [ ] Explain how `np.where` avoids a division-by-zero warning on a
      constant column, versus a loop with an `if` guard.

## Practiced in

`broadcast-bureau`, `grade-matrix`
