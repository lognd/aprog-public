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

## Task

Implement every function declared in `binary_bounds.hpp`, inside the
`bbounds` namespace. `v` is always already sorted in ascending order for
every function below (nothing in this assignment sorts anything itself).

- `linear_search(v, x)` -> `long` -- the index of the first element
  equal to `x`, found by an ordinary O(n) front-to-back scan (this one
  does not need to be O(log n) -- it exists as the baseline contrast for
  the rest of the assignment), or `-1` if absent.
- `binary_search_idx(v, x)` -> `long` -- the index of SOME element equal
  to `x`, found in O(log n) time, or `-1` if absent. If `x` appears more
  than once, any one matching index is acceptable.
- `first_occurrence(v, x)` -> `long` -- the index of the FIRST (lowest
  index) element equal to `x`, in O(log n) time, or `-1` if absent.
- `last_occurrence(v, x)` -> `long` -- the index of the LAST (highest
  index) element equal to `x`, in O(log n) time, or `-1` if absent.
- `count_of(v, x)` -> `long` -- how many elements equal `x`, built from
  `first_occurrence`/`last_occurrence` (or the same underlying bound
  logic) in O(log n) time -- not a scan. `0` if `x` is absent or `v` is
  empty.
- `insert_position(v, x)` -> `long` -- the index `x` would need to be
  inserted at to keep `v` sorted, in O(log n) time. Works for values not
  present in `v` too: `0` if `x` is smaller than every element,
  `v.size()` if `x` is larger than every element. If `x` is already
  present, this matches `first_occurrence`'s answer.

Every function on an empty `v` returns the documented empty-input
value (`-1` for the search functions, `0` for `count_of` and
`insert_position`) -- see the comment above each declaration in
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
