# Binary Bounds

Binary search is usually taught as "find one element in a sorted array,"
but the more useful skill is the family of small variations built on the
exact same idea: where does the FIRST copy of a repeated value live?
Where does the LAST copy live? How many copies are there? Where would a
value that is not even present need to be inserted to keep everything
sorted? This assignment asks you to implement all of those, as free
functions over an already-sorted `std::vector<int>`, every one of them
required to run in O(log n) time -- no scanning allowed once you leave
`linear_search`.

---

## Learning goals

- Build binary search from its **loop invariant**: the answer, if
  present, is always inside the shrinking candidate range
- Implement `lower_bound`/`upper_bound`-style boundary search by hand,
  without reaching for `std::lower_bound` or `std::upper_bound`
- Handle duplicate values correctly: first occurrence, last occurrence,
  and count, all as different questions with different answers
- Avoid the overflow-prone `(lo + hi) / 2` midpoint formula in favor of
  the overflow-safe alternative
- Recognize the difference between an implementation that is
  FUNCTIONALLY correct and one that is also FAST ENOUGH -- a linear scan
  can produce the exact right answer and still fail this assignment

---

## Background

### The invariant: the answer is always inside [lo, hi)

Binary search works by shrinking a candidate range, `[lo, hi)` -- a
**half-open range**, meaning `lo` is a valid candidate index but `hi` is
one position PAST the last candidate (the same convention `v.end()`
uses for iterators: a fence post that is never itself a real element).
The **loop invariant** -- the fact that stays true every single time you
check the loop's condition -- is this: if the value you are searching
for appears anywhere in the array at all, its index is guaranteed to
still be somewhere inside `[lo, hi)`. Every comparison the loop makes
only ever throws away the half of the range that has been PROVEN not to
contain the answer, never the half that might still hold it. Once `lo`
equals `hi`, the range is empty, and `lo` itself has landed exactly on
the answer's position -- if the value is present, `v[lo]` equals it; if
it is not present, `lo` is exactly where it WOULD go to keep the array
sorted. This one fact -- "the answer, if present, is always inside
`[lo, hi)`" -- is the same invariant walked through in detail in the
invariant-inspector activity's binary search question; if you have not
done that activity yet, working through it first will make this
assignment's logic click faster.

### The overflow-safe midpoint

The textbook formula for the middle of a range is `mid = (lo + hi) / 2`
-- but computing `lo + hi` first can silently overflow `int` for
sufficiently huge arrays (`int` tops out around 2.1 billion; an array
anywhere near a billion elements makes `lo + hi` risk exceeding that).
The fix, used throughout this assignment's reference logic, is
algebraically identical but computed differently: `mid = lo + (hi -
lo) / 2`. `hi - lo` is always the (small, safe) WIDTH of the current
range, so adding it to `lo` never risks the same overflow `lo + hi`
does. Use this form everywhere you compute a midpoint in this
assignment.

### Duplicates: first, last, and count are three different questions

Given a sorted array with a run of repeated values, like `{1, 3, 3, 3,
5, 7, 7, 9}`, an ordinary binary search that stops the instant it finds
`v[mid] == target` might land on ANY of the three `3`s -- which one
depends on exactly how the range happened to narrow. That is fine for
`binary_search_idx` (this assignment's "find some occurrence" function,
which does not promise which one), but it is not good enough for
`first_occurrence` or `last_occurrence`. Those need a search that keeps
narrowing PAST an exact match instead of stopping there -- treating
`v[mid] == target` the same as "too big" when hunting for the first
occurrence (so the range keeps shrinking leftward, toward the earliest
match), or the same as "too small" when hunting for the last occurrence
(shrinking rightward instead). `count_of` should not re-scan anything at
all -- it is built directly from `first_occurrence` and
`last_occurrence` (or the lower-bound/upper-bound logic underneath
them): the count of matching elements is exactly `last_occurrence`'s
index minus `first_occurrence`'s index, plus one.

---

## Examples: every function on one array

To make the six functions concrete, here is **one** sorted array, with the
index of every element written above it, and what each function returns
for it. Read this table first -- it is the whole assignment in miniature.

```
 index:   0   1   2   3   4   5   6   7
 v     = { 1,  3,  3,  3,  5,  7,  7,  9 }
```

| Call | Returns | Why |
|------|---------|-----|
| `linear_search(v, 7)`      | `5`  | the first `7` sits at index 5 (found by scanning left to right) |
| `binary_search_idx(v, 3)`  | `1`, `2`, or `3` | any index holding a `3` is acceptable -- this function does not promise which |
| `first_occurrence(v, 3)`   | `1`  | of the three `3`s (indices 1, 2, 3), the FIRST is at index 1 |
| `last_occurrence(v, 3)`    | `3`  | of the three `3`s, the LAST is at index 3 |
| `count_of(v, 3)`           | `3`  | there are three `3`s; note `3 - 1 + 1 = 3` (last index - first index + 1) |
| `count_of(v, 4)`           | `0`  | there are no `4`s at all |
| `insert_position(v, 4)`    | `4`  | a `4` would go between the last `3` (index 3) and the first `5` (index 4), i.e. at index 4 |
| `insert_position(v, 0)`    | `0`  | `0` is smaller than everything, so it goes at the very front |
| `insert_position(v, 10)`   | `8`  | `10` is larger than everything, so it goes at the very end (`v.size()` is 8) |
| `first_occurrence(v, 4)`   | `-1` | `4` is not present, so every search function returns `-1` |

## Worked example: watch `first_occurrence(v, 3)` run, step by step

This is the single most important thing to understand in the assignment, so
here is every step spelled out. We are searching the same array
`v = {1, 3, 3, 3, 5, 7, 7, 9}` for the FIRST index holding a `3`.

We track a half-open range `[lo, hi)` (`lo` is a real candidate index, `hi`
is one past the last candidate) and repeat while `lo < hi`. The trick for
"first occurrence": whenever `v[mid]` is **greater than or equal to** the
target, the earliest match must be at `mid` or to its left, so we move `hi`
down to `mid`; otherwise (`v[mid]` is smaller) the match must be to the
right, so we move `lo` up to `mid + 1`. The midpoint is always
`mid = lo + (hi - lo) / 2`.

| Step | `lo` | `hi` | `mid` | `v[mid]` | Compare to target `3` | Action |
|------|------|------|-------|----------|-----------------------|--------|
| start | 0 | 8 | 4 | `v[4] = 5` | `5 >= 3` -> match is at `mid` or left | `hi = 4` |
| 2 | 0 | 4 | 2 | `v[2] = 3` | `3 >= 3` -> match is at `mid` or left | `hi = 2` |
| 3 | 0 | 2 | 1 | `v[1] = 3` | `3 >= 3` -> match is at `mid` or left | `hi = 1` |
| 4 | 0 | 1 | 0 | `v[0] = 1` | `1 < 3`  -> match is to the right    | `lo = 1` |
| end | 1 | 1 | -- | -- | `lo == hi`, loop stops | `lo` is `1` |

The loop ends with `lo == 1`. Now check: is `v[1]` actually equal to `3`?
Yes (`v[1] == 3`), so `first_occurrence` returns **`1`**. (If `v[lo]` had
NOT equaled the target -- or if `lo` had run off the end of the array --
that would mean the target is absent, and the function returns `-1`.)

Notice the loop kept shrinking even after it first saw a `3` at index 2,
instead of stopping there. That is the entire difference between
`first_occurrence` and `binary_search_idx`: the plain search is allowed to
stop at the first `3` it stumbles on; `first_occurrence` must keep going
left to prove it has the earliest one. `last_occurrence` is the mirror
image -- it treats `v[mid] == target` as "too small" and moves `lo` up,
chasing the rightmost match instead.

---

## Task

Implement every function declared in `binary_bounds.hpp`, inside the
`bbounds` namespace. `v` is always already sorted in ascending order for
every function below (nothing in this assignment sorts anything itself).
Each bullet ends with a concrete example using the array
`v = {1, 3, 3, 3, 5, 7, 7, 9}` from above.

- `linear_search(v, x)` -> `long` -- the index of the first element
  equal to `x`, found by an ordinary O(n) front-to-back scan (this one
  does not need to be O(log n) -- it exists as the baseline contrast for
  the rest of the assignment), or `-1` if absent.
  *Example:* `linear_search(v, 7) == 5`; `linear_search(v, 2) == -1`.
- `binary_search_idx(v, x)` -> `long` -- the index of SOME element equal
  to `x`, found in O(log n) time, or `-1` if absent. If `x` appears more
  than once, any one matching index is acceptable.
  *Example:* `binary_search_idx(v, 5) == 4`; `binary_search_idx(v, 3)` is
  any of `1`, `2`, `3`; `binary_search_idx(v, 8) == -1`.
- `first_occurrence(v, x)` -> `long` -- the index of the FIRST (lowest
  index) element equal to `x`, in O(log n) time, or `-1` if absent.
  *Example:* `first_occurrence(v, 3) == 1`; `first_occurrence(v, 7) == 5`;
  `first_occurrence(v, 4) == -1`.
- `last_occurrence(v, x)` -> `long` -- the index of the LAST (highest
  index) element equal to `x`, in O(log n) time, or `-1` if absent.
  *Example:* `last_occurrence(v, 3) == 3`; `last_occurrence(v, 7) == 6`;
  `last_occurrence(v, 4) == -1`.
- `count_of(v, x)` -> `long` -- how many elements equal `x`, built from
  `first_occurrence`/`last_occurrence` (or the same underlying bound
  logic) in O(log n) time -- not a scan. `0` if `x` is absent or `v` is
  empty.
  *Example:* `count_of(v, 3) == 3`; `count_of(v, 7) == 2`;
  `count_of(v, 4) == 0`.
- `insert_position(v, x)` -> `long` -- the index `x` would need to be
  inserted at to keep `v` sorted, in O(log n) time. Works for values not
  present in `v` too: `0` if `x` is smaller than every element,
  `v.size()` if `x` is larger than every element. If `x` is already
  present, this matches `first_occurrence`'s answer.
  *Example:* `insert_position(v, 4) == 4`; `insert_position(v, 0) == 0`;
  `insert_position(v, 10) == 8`; `insert_position(v, 3) == 1`.

Every function on an empty `v` (`v = {}`) returns the documented
empty-input value: `-1` for the search functions, `0` for `count_of` and
`insert_position` -- see the comment above each declaration in
`binary_bounds.hpp` for the exact contract.

---

## Files

| File | Purpose |
|------|---------|
| `binary_bounds.hpp` | Declarations -- implement every function here (header-only, no matching .cpp) |

## Compilation and Testing

```bash
cd visible-tests
mkdir build && cd build
cmake .. -DSUBMISSION_DIR=<path-to-your-binary_bounds.hpp-directory>
cmake --build .
./binary-bounds_tests
```

---

## Constraints

- Do not use exceptions (`throw`/`try`/`catch`) anywhere in
  `binary_bounds.hpp`.
- Do not use `std::lower_bound`, `std::upper_bound`, `std::binary_search`,
  or `std::equal_range` anywhere in `binary_bounds.hpp` -- implement the
  bound-narrowing logic yourself. The whole point of this assignment is
  building that logic by hand once, so reaching for the standard library's
  version defeats it.
- Do not modify the public interface (function signatures) declared in
  `binary_bounds.hpp`.
- `count_of` must run in O(log n) time -- build it from
  `first_occurrence`/`last_occurrence` or shared bound logic, never a
  scan over matching elements.

---

## Grading

| Component | Points |
|-----------|--------|
| Source constraints (no `std::lower_bound`/`upper_bound`/`binary_search`/`equal_range`) | 10 |
| Compilation | 0 |
| Visible correctness (Catch2) | 30 |
| Hidden correctness (Catch2) | 45 |
| `count_of` performance (O(log n), not a scan) | 15 |
| **Total** | **100** |

The performance component calls `count_of` 200,000 times against a
sorted vector of one million elements with heavy duplicate runs, inside
a generous time budget. A correct O(log n) implementation finishes
comfortably inside that budget; an implementation that scans linearly to
count matches does not, even though it produces exactly the right
numeric answer every time.

## Submission

Submit a single file named `binary_bounds.hpp`. Do not rename it.

## Going further

- Extend the assignment with a `range_of(v, x)` function that returns
  both `first_occurrence` and `last_occurrence` as a `std::pair<long,
  long>`, computed with a single pass through the shared bound logic
  instead of two separate calls.
- Benchmark `linear_search` against `binary_search_idx` yourself, on
  arrays of increasing size (1,000, 10,000, 100,000, 1,000,000
  elements), and plot the comparison counts. Does the gap match what you
  would predict from O(n) versus O(log n)?
- Look up how `std::lower_bound` and `std::upper_bound` are actually
  specified in the C++ standard library, once you have implemented your
  own versions here. Do their exact parameter and return conventions
  match what you built, or differ in some detail?
