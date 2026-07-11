# Grade Matrix

Broadcast Bureau introduced the numpy mental model: an ARRAY is a
fixed-shape block of numbers, arithmetic operators are elementwise,
and BROADCASTING lets differently-shaped arrays combine without an
explicit loop. This assignment puts that model to work on a real,
if small, data-processing task: a scores matrix, one row per student
and one column per assignment, and six operations a grading tool
would actually need -- averages, curving, dropping a low score,
finding who passed, and standardizing. The catch is the constraint:
every one of the six functions must be written using numpy's
vectorized operations. Writing the same logic with a Python `for` or
`while` loop is not just discouraged here, it is mechanically
forbidden and checked before your code is even graded for
correctness -- because writing loop-free, vectorized numpy code is
the actual skill this assignment exists to build.

## Learning goals

- Distinguish a numpy array's row axis (`axis=0`) from its column
  axis (`axis=1`) and use `axis=` correctly in reductions like `.sum`,
  `.mean`, and `.std`
- Use broadcasting to add a per-column offset to every row of a matrix
  in one expression, with no explicit loop over rows
- Use boolean masking (comparison operators on arrays) to build a
  pass/fail mask without an `if` inside a loop
- Recognize and avoid a division-by-zero pitfall (`np.where` to guard
  a column with zero standard deviation) instead of reaching for a
  loop with a conditional inside it
- Practice reading and satisfying a hard, mechanically-enforced
  constraint (no loop keywords) rather than a style guideline

## Task

Implement six functions over a scores matrix (a 2-D numpy array,
`m`, with `m.shape == (n_students, n_assignments)`) in a file named
`matrix_ops.py`.

### `student_means(m)`

```python
def student_means(m: np.ndarray) -> np.ndarray:
```

Returns a 1-D array of length `n_students`: each student's mean score
across all of their assignments.

### `assignment_means(m)`

```python
def assignment_means(m: np.ndarray) -> np.ndarray:
```

Returns a 1-D array of length `n_assignments`: each assignment's mean
score across all students.

### `curve_to(m, target)`

```python
def curve_to(m: np.ndarray, target: float) -> np.ndarray:
```

Returns a **new** matrix, the same shape as `m`, with a per-assignment
(per-column) offset added so that each column's mean becomes exactly
`target`. Every student's score on a given assignment shifts by the
same amount -- the amount that assignment's own column needs to reach
`target`, not a single matrix-wide offset.

### `drop_lowest(m)`

```python
def drop_lowest(m: np.ndarray) -> np.ndarray:
```

Returns a 1-D array of length `n_students`: each student's mean score
computed **excluding their single lowest score**. If a student has a
tie for the lowest score, exclude exactly one occurrence of that
value's contribution (equivalent to: subtract the minimum once from
the row's sum, then divide by one fewer assignment). If `m` has only
one assignment (one column), there would be nothing left to average
after dropping the only score -- return `0.0` for every student in
that case, instead of dividing by zero.

### `passing_mask(m, threshold)`

```python
def passing_mask(m: np.ndarray, threshold: float) -> np.ndarray:
```

Returns a 1-D boolean array of length `n_students`: `True` for every
student whose mean score (across all assignments) is greater than or
equal to `threshold`, `False` otherwise.

### `standardize(m)`

```python
def standardize(m: np.ndarray) -> np.ndarray:
```

Returns a new matrix, the same shape as `m`, of per-column z-scores:
`(value - column_mean) / column_std`, computed independently for each
column. A column where every value is identical has a standard
deviation of `0`; for that column, return all zeros instead of
dividing by zero (and without letting numpy emit a division warning).

### Examples

```python
>>> import numpy as np
>>> m = np.array([[80., 90., 70.], [60., 50., 100.], [100., 100., 100.]])
>>> student_means(m)
array([ 80.,  70., 100.])
>>> assignment_means(m)
array([80., 80., 90.])
>>> curve_to(m, 90.0).mean(axis=0)
array([90., 90., 90.])
>>> drop_lowest(m)
array([ 85.,  80., 100.])
>>> passing_mask(m, 80.0)
array([ True, False,  True])
```

## Files

| File | Purpose |
|------|---------|
| `matrix_ops.py` | Write your implementation here |

## Compilation and Testing

```bash
python -m pytest visible-tests/test_visible.py -v
```

## Constraints

- Do not rename `matrix_ops.py`, or rename/remove any function.
- Type hints are required on every function's parameters and return
  type, matching the signatures above. Plain `np.ndarray` hints are
  fine -- `numpy.typing.NDArray` is not required.
- `numpy` is the only third-party import allowed, plus `typing` and
  anything from the standard library **except** `math`, `itertools`,
  `functools`, and `collections.abc` -- those are blocked so you solve
  this with numpy's own vectorized operations, not a workaround
  borrowed from another module.
- **No `for` or `while` keyword may appear anywhere in `matrix_ops.py`.**
  This is checked mechanically before your correctness tests even run.
  Every function must be written using numpy's own vectorized
  operations (`.sum`, `.mean`, `.min`, `.std`, broadcasting, boolean
  comparisons, `np.where`) instead of an explicit loop.
- `standardize` must not raise or print a division-by-zero warning for
  a constant column; use `np.where` (or an equivalent guard) to avoid
  ever actually dividing by zero.
- A clean run of [ty](https://docs.astral.sh/ty/) (a fast, modern
  Python type checker, run over `matrix_ops.py`) earns a bonus.

## Grading

| Component                              | Points |
|-----------------------------------------|--------|
| Loop-keyword and import constraints (gate) | 10     |
| Visible correctness tests               | 30     |
| Hidden correctness tests                | 50     |
| Clean `ty` type-check (bonus)           | 10     |
| **Total**                               | **100** |

Hidden tests cover: single-student and single-assignment matrices,
all-equal columns (`standardize`'s zero-std case), negative scores,
ties at the minimum for `drop_lowest`, and boundary behavior at the
exact passing threshold.

## Submission

Submit your implementation as `matrix_ops.py`. Do not rename it.

## Going further

- Rewrite `drop_lowest` to drop each student's two lowest scores
  instead of one, still with no loop. What has to change about the
  single-assignment (now single-or-double-assignment) edge case?
- `curve_to` shifts every score in a column by the same amount, which
  can push some students above 100. Write a variant, `curve_to_capped`,
  that clips the result to `[0, 100]` using `np.clip`, with no loop.
- Benchmark `standardize` on a `10000 x 50` random matrix against a
  hand-written version using nested Python loops. How much faster is
  the vectorized version, and why?
