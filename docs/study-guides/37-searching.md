# Study Guide 37: Searching

This module builds real binary search intuition by hand-tracing the
canonical `[lo, hi)` implementation index by index, diagnosing the classic
ways it breaks, and implementing the full first/last/count/insert-position
family on top of it -- all required to run in O(log n), never a scan.

## Know before you start

- The loop-invariant reasoning technique and the binary search invariant
  in particular ("the answer, if present, is always inside the shrinking
  range") [assumed: row 36 -- Proofs & Invariance]
- O(log n) vs. O(n) growth and estimating log2 by hand [assumed: row 28 --
  Complexity Theory]
- Integer overflow on `int` [assumed: row 5 -- Variables & Type]
- The fence-post `[lo, hi)` half-open range convention shared with
  `end()` [assumed: row 35 -- Iterators]

## Taught here

Concept: the canonical binary search implementation
- Know the canonical form: `lo` starts at 0, `hi` starts at `n` (a
  half-open range `[lo, hi)` where `lo` is a valid candidate index and
  `hi` is one position PAST the last candidate), the loop runs `while (lo
  < hi)`, and the range narrows toward `lo == hi`, the final answer
  position whether or not the target is present.
- Know the overflow-safe midpoint formula `mid = lo + (hi - lo) / 2`
  (integer division, rounds down) versus the overflow-prone
  `mid = (lo + hi) / 2`, whose intermediate sum `lo + hi` can silently
  exceed `INT_MAX` on sufficiently huge arrays even though the true
  midpoint is nowhere near overflow.
- Be able to trace `lo`, `hi`, and `mid` by hand across multiple
  iterations and count comparisons for a present target, an absent
  target, and a target at each boundary.
- Know the concrete O(log n) vs. O(n) comparison-count gap between binary
  and linear search grows dramatically with n, even though both are
  "just" different Big-O classes.

Concept: the classic binary search bugs
- Know the infinite-loop bug: using `lo = mid` instead of `lo = mid + 1`
  on the "too small" branch can leave `lo`/`hi` unchanged forever when the
  range narrows to two elements.
- Know the skip-the-answer bug: mixing the half-open `[lo, hi)` and
  closed-interval `[lo, hi]` conventions within one implementation
  (inconsistent initialization or narrowing) can silently step past a
  present target.
- Know the out-of-bounds-read bug and the swapped-comparison-branches bug
  (searching in the wrong direction) as two more diagnosable failure
  categories.
- Be able to diagnose which of these categories (or "correct") a given
  implementation falls into, tracing the specific input shape that
  triggers each one.

Concept: the bound-narrowing family
- Know that an ordinary "stop at first match" binary search does not
  promise WHICH occurrence of a duplicated value it lands on -- fine for
  "find some occurrence," not fine for "find the first/last occurrence."
- Be able to implement `first_occurrence`/`last_occurrence` by narrowing
  PAST an exact match instead of stopping there: treating `v[mid] ==
  target` as "too big" (keep shrinking leftward) when hunting for the
  first occurrence, or as "too small" (keep shrinking rightward) when
  hunting for the last.
- Be able to implement `count_of` as `last_occurrence - first_occurrence +
  1` (built from the two bound functions, never a re-scan) to keep it
  O(log n).
- Be able to implement `insert_position`: the index a value would need to
  keep the array sorted, 0 if smaller than everything, `v.size()` if
  larger than everything, and equal to `first_occurrence` if the value is
  already present.

## Study checklist

- [ ] Trace lo/hi/mid for a binary search on a fixed sorted array against
      a present target, an absent target, and a boundary target.
- [ ] Explain why lo + (hi - lo) / 2 avoids overflow that (lo + hi) / 2
      risks.
- [ ] Diagnose the lo = mid infinite-loop bug on a 2-element array.
- [ ] Explain how first_occurrence's narrowing differs from an ordinary
      "stop on match" binary search.
- [ ] Derive count_of from first_occurrence/last_occurrence without
      scanning.
- [ ] State insert_position's answer for a value smaller than everything
      and larger than everything.

## Practiced in

`search-stepper`, `binary-search-autopsy`, `binary-bounds`
