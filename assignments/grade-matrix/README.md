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

---

## Examples at a glance

To make all six functions concrete, here is **one** small scores matrix --
four students (rows), three assignments (columns), including a negative
score (row 3, an invalid/extra-credit-adjusted score) and a tied,
all-same-value row (row 1) -- and what every function produces for it.
Read this table first; it is the whole assignment in miniature.

```
                assignment0  assignment1  assignment2
student0            80           90           70
student1            60           60           60
student2           100           50          100
student3           -10           40           40
```

```python
>>> m = np.array([[ 80.,  90.,  70.],
...               [ 60.,  60.,  60.],
...               [100.,  50., 100.],
...               [-10.,  40.,  40.]])
```

| Call | Result | Why |
|------|--------|-----|
| `student_means(m)` | `[80.0, 60.0, 83.333..., 23.333...]` | each row's own average, e.g. student 3's is `(-10+40+40)/3` -- the negative score just averages in like any other number |
| `assignment_means(m)` | `[57.5, 60.0, 67.5]` | each column's own average across all four students |
| `curve_to(m, 75.0).mean(axis=0)` | `[75.0, 75.0, 75.0]` | curving adds a per-column offset (here `[17.5, 15.0, 7.5]`) chosen so each column's new mean is exactly `75.0` |
| `drop_lowest(m)` | `[85.0, 60.0, 100.0, 40.0]` | each row's mean after dropping its own single lowest score; row 1 (`60, 60, 60`, a three-way tie for the minimum) still only drops **one** `60`, leaving `(180-60)/2 = 60.0` |
| `passing_mask(m, 60.0)` | `[True, True, True, False]` | student 1's mean is exactly `60.0` -- `>=` means sitting exactly on the threshold still passes |
| `standardize(m)` column 0 | `[0.543, 0.060, 1.025, -1.628]` (approx) | ordinary z-scores: `(value - column_mean) / column_std` |

Row 1's tie and row 3's negative score are the "tricky" inputs worth
tracing by hand once, since they are exactly the cases hidden tests probe.

## Worked example: watch `standardize` run, step by step

`standardize` is the function with the most moving parts -- two reductions
(`mean`, `std`), a broadcasted subtraction and division, and a guard
against dividing by zero -- so it is worth tracing every intermediate
array once. Take a small matrix where one column is constant (its
standard deviation is `0`, the exact case the guard exists for):

```python
>>> m2 = np.array([[70., 50.],
...                [90., 50.],
...                [80., 50.]])
```

| Step | Expression | Result | Why |
|------|------------|--------|-----|
| 1 | `mean = m2.mean(axis=0)` | `[80.0, 50.0]` | the mean of each column, computed independently (`axis=0` reduces down the rows) |
| 2 | `std = m2.std(axis=0)` | `[8.1650, 0.0]` | column 0 varies (`70, 90, 80`); column 1 is constant, so its standard deviation is exactly `0` -- the case that would otherwise divide by zero |
| 3 | `safe_std = np.where(std == 0, 1.0, std)` | `[8.1650, 1.0]` | swap the `0` for a harmless `1.0` so the division in the next step never actually divides by zero (no warning is ever triggered) |
| 4 | `m2 - mean` | `[[-10., 0.], [10., 0.], [0., 0.]]` | broadcasting subtracts the 1-D `mean` from every row of `m2` |
| 5 | `z = (m2 - mean) / safe_std` | `[[-1.2247, 0.], [1.2247, 0.], [0., 0.]]` | dividing by the guarded `safe_std` -- column 1 is `0 / 1.0 = 0.0` for every row, which happens to already be the right answer |
| 6 (final) | `np.where(std == 0, 0.0, z)` | `[[-1.2247, 0.0], [1.2247, 0.0], [0.0, 0.0]]` | explicitly force column 1 (where the real `std` was `0`) to `0.0`; column 0 keeps its real z-scores from step 5 unchanged |

The final result matches calling `standardize(m2)` directly: column 0 gets
real z-scores (`-1.2247, 1.2247, 0.0`), and column 1 -- the constant
column -- is all zeros, with no division-by-zero warning ever printed.
Steps 5 and 6 give the same numbers for column 1 in this particular
example only because `0 / 1.0` already equals `0.0`; step 6 is still
necessary in general, since `safe_std` is a workaround for the division,
not a guarantee that the pre-guard math always comes out right.

---

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

*Examples:* for `m = [[80,90,70],[60,60,60],[100,50,100],[-10,40,40]]`,
`student_means(m)` is `[80.0, 60.0, 83.333..., 23.333...]` -- the third
student's negative score still just averages in normally (`(100 + 50 +
100) / 3`). A single-row matrix `m = [[5., 5., 5.]]` returns `[5.0]`.
An empty matrix with shape `(0, 3)` (no students at all) returns an
empty array, `array([], dtype=float64)`.

### `assignment_means(m)`

```python
def assignment_means(m: np.ndarray) -> np.ndarray:
```

Returns a 1-D array of length `n_assignments`: each assignment's mean
score across all students.

*Examples:* for the same `m` above, `assignment_means(m)` is `[57.5,
60.0, 67.5]` (column 0 is `(80+60+100-10)/4 = 57.5`). A single-column
matrix `m = [[10.],[20.],[30.]]` returns `[20.0]`. An empty matrix with
shape `(0, 3)` returns `[nan, nan, nan]` -- numpy's mean of zero
values is not a number, and this assignment does not require guarding
against that particular edge case.

### `curve_to(m, target)`

```python
def curve_to(m: np.ndarray, target: float) -> np.ndarray:
```

Returns a **new** matrix, the same shape as `m`, with a per-assignment
(per-column) offset added so that each column's mean becomes exactly
`target`. Every student's score on a given assignment shifts by the
same amount -- the amount that assignment's own column needs to reach
`target`, not a single matrix-wide offset.

*Examples:* for `m` above, `curve_to(m, 75.0)` adds `[17.5, 15.0, 7.5]`
to columns 0/1/2 respectively (`75 - 57.5`, `75 - 60`, `75 - 67.5`), so
row 0 becomes `[97.5, 105.0, 77.5]`; check with
`curve_to(m, 75.0).mean(axis=0) == [75., 75., 75.]`. Curving can push
a score above 100 or below 0 -- row 0's second column becomes `105.0`,
which this function does not clip (see "Going further"). On a
single-row matrix `m = [[50., 50.]]`, every column's mean already
equals its own value, so `curve_to(m, 60.0)` returns `[[60., 60.]]`.

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

*Examples:* for `m` above, `drop_lowest(m)` is `[85.0, 60.0, 100.0,
40.0]`. Row 1, `[60, 60, 60]`, is the all-same-value / tie case: every
entry is the minimum, but only one `60` is dropped, leaving
`(180 - 60) / 2 = 60.0`, the same as the mean it started with -- exactly
the "exclude one occurrence" rule the description calls for. On a
single-column matrix `m = [[5.],[10.]]`, there is nothing left after
dropping the only score, so `drop_lowest(m)` returns `[0.0, 0.0]`
rather than dividing by zero.

### `passing_mask(m, threshold)`

```python
def passing_mask(m: np.ndarray, threshold: float) -> np.ndarray:
```

Returns a 1-D boolean array of length `n_students`: `True` for every
student whose mean score (across all assignments) is greater than or
equal to `threshold`, `False` otherwise.

*Examples:* for `m` above, `passing_mask(m, 60.0)` is `[True, True,
True, False]` -- student 1's mean is exactly `60.0`, and `>=` means
landing exactly on the threshold still counts as passing (the
boundary case). `passing_mask(m, 200.0)` (a threshold nobody can
reach) is `[False, False, False, False]`; `passing_mask(m, -100.0)`
(a threshold everybody clears) is `[True, True, True, True]`.

### `standardize(m)`

```python
def standardize(m: np.ndarray) -> np.ndarray:
```

Returns a new matrix, the same shape as `m`, of per-column z-scores:
`(value - column_mean) / column_std`, computed independently for each
column. A column where every value is identical has a standard
deviation of `0`; for that column, return all zeros instead of
dividing by zero (and without letting numpy emit a division warning).

*Examples:* for `m2 = [[70.,50.],[90.,50.],[80.,50.]]` (column 1 is
constant), `standardize(m2)` is `[[-1.2247, 0.0], [1.2247, 0.0], [0.0,
0.0]]` -- column 0 gets real z-scores, but column 1's zero standard
deviation makes every one of its z-scores `0.0` instead of raising a
division-by-zero warning (see the full trace below). A single-row
matrix `m = [[5., 10., 20.]]` has every column constant (one value
each), so `standardize(m)` is `[[0., 0., 0.]]`.

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
- **Type-annotation bonus (10 pts):** every function must annotate all of its parameters and its return type. The bonus is awarded only when every function is fully annotated; a separate, informational [ty](https://docs.astral.sh/ty/) check then flags any annotation on `matrix_ops.py` that does not hold up.

## Grading

| Component                              | Points |
|-----------------------------------------|--------|
| Loop-keyword and import constraints (gate) | 10     |
| Visible correctness tests               | 30     |
| Hidden correctness tests                | 50     |
| Complete type annotations (bonus)       | 10     |
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
