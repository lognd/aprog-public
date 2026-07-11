# Sort Suite

Sorting algorithms are usually introduced as a single black-box function
call (`std::sort`), but understanding what that call is actually doing
requires building a few of the classic algorithms yourself, by hand,
once. This assignment asks you to implement selection sort, insertion
sort, and merge sort over a `std::vector<int>`, a stable version of merge
sort over a vector of `(int, std::string)` pairs, and a small
`is_sorted_asc` helper -- with one hard requirement: `merge_sort` has to
actually run in O(n log n) time, not just produce the right numbers. A
correct-looking sort that is secretly quadratic will pass every ordinary
correctness test and still fail this assignment.

---

## Learning goals

- Implement selection sort, insertion sort, and merge sort from scratch,
  entirely by hand
- Understand STABILITY concretely: what it means, and how to build a
  sort that preserves it on purpose
- Recognize the difference between an implementation that is
  FUNCTIONALLY correct and one that is also FAST ENOUGH -- an
  insertion-sort-in-disguise can produce exactly the right sorted array
  and still be O(n^2) instead of the required O(n log n)
- Practice O(n) scratch-array management for merge sort's merge step, as
  the deliberate tradeoff for its O(n log n) worst-case guarantee

---

## Background

### Pass, swap, in-place, and scratch array -- defined

A **pass** is one complete walk through the array by a sorting
algorithm's outer loop. A **swap** exchanges the values at two array
positions. An algorithm is **in-place** if it rearranges its input using
only a small, fixed amount of extra memory (a handful of temporary
variables), no matter how large the input is -- selection sort and
insertion sort are both in-place. A **scratch array** is a separate
block of memory, proportional in size to the data being processed, used
as temporary working space -- merge sort's merge step needs one, because
it cannot safely overwrite either of the two sorted halves it is still
reading values out of.

If you have not already worked through the sort-pass-tracer activity
(tracing bubble sort, selection sort, insertion sort, and one merge
step by hand on concrete arrays) or the sorting-court activity (stability,
worst-case behavior, and what `std::sort` actually is), doing those
first will make this assignment's logic click faster.

### Stability, concretely

A sort is **stable** if it preserves the original relative order of any
two elements that compare equal on the sort key. `stable_sort_pairs`
sorts a vector of `(int, std::string)` pairs by the `int` (`.first`)
only -- if two pairs share the same `.first`, a stable sort guarantees
they keep whatever relative order they started in. Build
`stable_sort_pairs` from the same merge sort logic as `merge_sort`:
during a merge step, when the two halves' current fronts tie on
`.first`, always take from the LEFT half first. That single tie-break
rule is what makes the whole sort stable -- get it backwards (or use an
algorithm like selection sort that does long-range swaps) and equal-key
pairs can end up reordered relative to each other, even though every
individual `.first` value still ends up in the numerically correct
sorted position.

### Why merge_sort has a real time-budget requirement

`merge_sort` is required to run in O(n log n) time. It is entirely
possible to write something NAMED `merge_sort` that is secretly just
insertion sort underneath -- it will produce a perfectly sorted array
every single time, and ordinary correctness tests (checking that the
output is sorted and contains the right elements) cannot tell the
difference. The only way to catch that is to time it on a large enough
input: this assignment's grading includes a PerformanceTest that runs
`merge_sort` on a vector of 1,000,000 random integers inside a generous
time budget that a genuine O(n log n) implementation clears comfortably
and an O(n^2) implementation cannot.

---

## Examples: every function on one array

To make the five functions concrete, here is **one** unsorted array, and
what each function does to it. Read this table first -- it is the whole
assignment in miniature.

```
v = { 5, 3, 8, 1, 4 }
```

| Call | Result (what `v` becomes, or return value) | Why |
|------|---------------------------------------------|-----|
| `selection_sort(v)` | `v` becomes `{1, 3, 4, 5, 8}` | repeatedly finds the minimum of the remaining unsorted region and swaps it into place -- see the worked example below for every swap |
| `insertion_sort(v)` | `v` becomes `{1, 3, 4, 5, 8}` | grows a sorted prefix one element at a time, shifting larger elements right to make room |
| `merge_sort(v)` | `v` becomes `{1, 3, 4, 5, 8}` | splits in half recursively, sorts each half, merges the two sorted halves back together with an O(n) scratch array |
| `is_sorted_asc(v)` (on the ORIGINAL `{5, 3, 8, 1, 4}`) | `false` | `5 > 3`, so the array is not currently in ascending order |
| `is_sorted_asc(v)` (on the SORTED `{1, 3, 4, 5, 8}`) | `true` | every element is `<=` the one after it |

Note that all three sorting functions produce the exact same final array
-- that is the point of the assignment: three different strategies,
one correct answer. What differs between them is not the *result* but
*how they get there* (which elements get compared and swapped, and how
fast that process is as the array grows), which is exactly what the
worked example below makes visible step by step.

## Worked example: watch `selection_sort({5, 3, 8, 1, 4})` run, step by step

This is the single most important thing to understand about selection
sort, so here is every pass spelled out. Selection sort keeps a growing
"sorted region" at the front of the array (initially empty) and a
shrinking "unsorted region" after it. On each pass, it scans the ENTIRE
unsorted region to find its minimum, then swaps that minimum into the
first open slot of the sorted region -- growing the sorted region by
exactly one element per pass.

Starting array: `v = {5, 3, 8, 1, 4}` (indices `0..4`).

| Pass | Unsorted region (indices) | Minimum found (value, index) | Swap performed | `v` after this pass |
|------|---------------------------|-------------------------------|-----------------|----------------------|
| 1 | `0..4` (`5, 3, 8, 1, 4`) | `1` at index 3 | swap index 0 (`5`) with index 3 (`1`) | `{1, 3, 8, 5, 4}` |
| 2 | `1..4` (`3, 8, 5, 4`) | `3` at index 1 | swap index 1 with itself (already the minimum, no-op) | `{1, 3, 8, 5, 4}` |
| 3 | `2..4` (`8, 5, 4`) | `4` at index 4 | swap index 2 (`8`) with index 4 (`4`) | `{1, 3, 4, 5, 8}` |
| 4 | `3..4` (`5, 8`) | `5` at index 3 | swap index 3 with itself (already the minimum, no-op) | `{1, 3, 4, 5, 8}` |
| end | -- | -- | loop stops (only one element, index 4, would be left as its own "unsorted region") | `{1, 3, 4, 5, 8}` |

The loop ends after pass 4 because once the first `n - 1` positions
(indices `0..3`) are known to hold the correct values, the last
remaining position (index 4) has nowhere else to go and must already be
correct -- there is nothing left to compare it against. Final result:
**`{1, 3, 4, 5, 8}`**, matching every other sort function's output above.

---

## Task

Implement every function declared in `sort_suite.hpp`, inside the
`sortsuite` namespace. Every sorting function mutates the vector it is
given directly (in place); none of them return a new vector.

- `selection_sort(v)` -> `void` -- sorts `v` ascending in place using
  selection sort (find the minimum of the remaining unsorted region,
  swap it into place, repeat).
  *Example:* `selection_sort` on `{5, 3, 8, 1, 4}` leaves `v` as
  `{1, 3, 4, 5, 8}` (see the worked example above for every pass);
  on the already-sorted `{1, 2, 3}` it leaves `v` unchanged;
  on the reverse-sorted `{3, 2, 1}` it leaves `v` as `{1, 2, 3}`;
  on the empty `{}` it is a no-op (`v` stays `{}`).
- `insertion_sort(v)` -> `void` -- sorts `v` ascending in place using
  insertion sort (grow a sorted prefix one element at a time, shifting
  larger elements right to make room).
  *Example:* `insertion_sort` on `{5, 3, 8, 1, 4}` leaves `v` as
  `{1, 3, 4, 5, 8}`;
  on the single-element `{42}` it leaves `v` as `{42}` (a documented
  no-op, since a one-element array is already sorted);
  on the duplicate-heavy `{2, 2, 1, 1, 3}` it leaves `v` as
  `{1, 1, 2, 2, 3}` (duplicates are compared with `>`, not `>=`, so
  equal elements are never needlessly shifted past each other).
- `merge_sort(v)` -> `void` -- sorts `v` ascending using merge sort
  (split in half recursively, sort each half, merge the two sorted
  halves back together). May allocate an O(n) scratch array for the
  merge step. Must run in O(n log n) time -- see Background above for
  why this is checked directly, not just inferred from correctness.
  *Example:* `merge_sort` on `{5, 3, 8, 1, 4}` leaves `v` as
  `{1, 3, 4, 5, 8}`;
  on the empty `{}` it is a documented no-op (`v` stays `{}`);
  on the already-sorted `{1, 2, 3, 4, 5}` it leaves `v` unchanged (still
  runs the full split/merge process, but every merge step takes
  entirely from the left half first).
- `stable_sort_pairs(v)` -> `void` -- sorts `v` (a vector of
  `std::pair<int, std::string>`) ascending by `.first` ONLY, built from
  the same merge sort logic as `merge_sort`. Must be stable: pairs with
  equal `.first` keep their original relative order.
  *Example:* `stable_sort_pairs` on
  `{(2, "b"), (1, "x"), (2, "a"), (1, "y")}` leaves `v` as
  `{(1, "x"), (1, "y"), (2, "b"), (2, "a")}` -- notice `(2, "b")` still
  comes before `(2, "a")`, and `(1, "x")` still comes before `(1, "y")`,
  because both pairs in each tied group kept their ORIGINAL relative
  order (an unstable sort would be allowed to swap `"b"` and `"a"`, or
  `"x"` and `"y"`, since both orderings are equally valid by `.first`
  alone);
  on the empty `{}` it is a documented no-op.
- `is_sorted_asc(v)` -> `bool` -- returns whether `v` is currently sorted
  in ascending order. Does not modify `v`.
  *Example:* `is_sorted_asc({1, 2, 2, 5, 9}) == true` (duplicates are
  fine -- ascending allows `<=` between neighbors, not strict `<`);
  `is_sorted_asc({1, 5, 2}) == false` (`5 > 2`, so it is not ascending);
  `is_sorted_asc({}) == true` and `is_sorted_asc({7}) == true` (an
  empty array and a single-element array are both documented as
  trivially sorted -- there are no neighboring pairs to violate
  ascending order).

Every function on an empty or single-element `v` is a documented no-op
(for the four sorting functions) or returns `true` (for
`is_sorted_asc`) -- see the comment above each declaration in
`sort_suite.hpp` for the exact contract.

---

## Files

| File | Purpose |
|------|---------|
| `sort_suite.hpp` | Declarations -- implement every function here (header-only, no matching .cpp) |

## Compilation and Testing

```bash
cd visible-tests
mkdir build && cd build
cmake .. -DSUBMISSION_DIR=<path-to-your-sort_suite.hpp-directory>
cmake --build .
./sort-suite_tests
```

---

## Constraints

- Do not use exceptions (`throw`/`try`/`catch`) anywhere in
  `sort_suite.hpp`.
- Do not use `std::sort`, `std::stable_sort`, `std::partial_sort`, or
  `qsort` anywhere in `sort_suite.hpp` -- implement every algorithm
  yourself. The whole point of this assignment is building these
  algorithms by hand once, so reaching for the standard library's
  version defeats it.
- Do not modify the public interface (function signatures) declared in
  `sort_suite.hpp`.
- `merge_sort` must run in O(n log n) time -- an algorithm that produces
  a correctly sorted array but does so by scanning or shifting
  quadratically (e.g. insertion sort or selection sort under a
  different name) does not satisfy this requirement, even though it
  passes every ordinary correctness check.
- `stable_sort_pairs` must be stable -- equal-`.first` pairs must keep
  their original relative order.

---

## Grading

| Component | Points |
|-----------|--------|
| Source constraints (no `std::sort`/`std::stable_sort`/`std::partial_sort`/`qsort`) | 10 |
| Compilation | 0 |
| Visible correctness (Catch2) | 25 |
| Hidden correctness (Catch2) | 45 |
| `merge_sort` performance (O(n log n), not quadratic) | 20 |
| **Total** | **100** |

The performance component calls `merge_sort` once on a vector of
1,000,000 random integers, inside a generous time budget. A correct
O(n log n) implementation finishes comfortably inside that budget; an
implementation that is secretly quadratic (e.g. insertion sort under
the `merge_sort` name) does not, even though it produces exactly the
right sorted array every time.

## Submission

Submit a single file named `sort_suite.hpp`. Do not rename it.

## Going further

- Add a `quick_sort(v)` function (in-place, using a pivot-partition
  scheme) and benchmark it against your `merge_sort` on random,
  already-sorted, and reverse-sorted inputs of increasing size. Does its
  performance ever fall back to something closer to O(n^2)?
- Modify `stable_sort_pairs` to sort by `.second` (the string) instead
  of `.first`, and verify by hand on a small example that ties still
  break in original-relative-order.
- Time `selection_sort`, `insertion_sort`, and `merge_sort` against each
  other on arrays of increasing size (1,000, 10,000, 100,000 elements).
  At what size does the O(n^2)-versus-O(n log n) gap become impossible
  to ignore?
- Look up how `std::stable_sort` is actually implemented (it is
  typically an in-place-adjacent merge sort variant, sometimes falling
  back to an out-of-place merge when enough scratch memory is
  available). How does that compare to what you built here?
