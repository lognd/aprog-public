# Study Guide 38: Sorting

This module traces bubble/selection/insertion sort pass by pass and
merge sort's merge step by hand, covers sort stability and what
`std::sort` actually is (introsort), and has students implement the
classic O(n^2) sorts plus a genuinely O(n log n) merge sort and its
stable variant.

## Know before you start

- O(n^2) vs. O(n log n) growth and the real cost gap at scale [assumed:
  row 28 -- Complexity Theory]
- Amortized/worst-case reasoning [assumed: row 28 -- Complexity Theory]
- In-place mutation via reference/pointer parameters [assumed: row 11 --
  Pointers]
- The bound-narrowing family and shrinking-range reasoning that recurs in
  merge's two-pointer walk [assumed: row 37 -- Searching]

## Taught here

Concept: passes, swaps, in-place, and scratch memory
- Know a pass is one complete walk through the array by a sorting
  algorithm's outer loop: bubble sort compares every adjacent pair once
  per pass; selection sort finds the minimum of the remaining unsorted
  region and places it; insertion sort inserts exactly one new element
  into the sorted prefix built up so far.
- Know a swap exchanges the values at two array positions.
- Know in-place means an algorithm rearranges input using only a small,
  fixed amount of extra memory regardless of input size -- bubble,
  selection, and insertion sort are all in-place; merge sort is not,
  because its merge step needs a scratch array (memory proportional to
  the data being merged) since it cannot safely overwrite either sorted
  half it is still reading from.
- Be able to trace one pass (not the fully sorted result) of bubble,
  selection, or insertion sort by hand on a concrete array, and count
  swaps/comparisons.
- Be able to trace merge sort's merge step: comparing two sorted halves'
  fronts and advancing one pointer at a time into a scratch array.

Concept: stability
- Know a sort is stable if it preserves the original relative order of
  any two elements that compare equal on the sort key -- an unstable sort
  makes no such promise.
- Know stability matters most when sorting by one key while relying on an
  earlier sort by a different key to still hold for ties.
- Know selection sort is NOT stable (its long-range swaps can reorder
  equal-key elements); bubble sort, insertion sort, and merge sort (with
  a left-favoring tie-break) are stable.
- Know the stability tie-break rule for merge: when the two halves'
  current fronts tie on the sort key, always take from the LEFT half
  first -- that single rule is what makes the whole sort stable.

Concept: choosing and trusting a sort
- Know the concrete O(n^2) vs. O(n log n) cost gap grows enormous at
  realistic scale, not just "worse" in the abstract.
- Know `std::sort` implements introsort (a hybrid: quicksort with a
  depth-limit fallback to heapsort, switching to insertion sort for small
  sub-ranges) and is the correct default to reach for in real code instead
  of a hand-written sort.
- Be able to match a workload (e.g. nearly-sorted data, tie-preserving
  multi-key sort) to the algorithm best suited for it.

Concept: implementing sorts with a real performance requirement
- Be able to implement `selection_sort`/`insertion_sort` in place, from
  scratch.
- Be able to implement `merge_sort` (split recursively, sort each half,
  merge with an O(n) scratch array) and recognize that a "correct-looking"
  sort can secretly be O(n^2) underneath (e.g. insertion sort renamed) --
  ordinary correctness tests cannot catch this, only a timed test on a
  large input can, which is exactly what the assignment's performance
  test does.
- Be able to build `stable_sort_pairs` from the same merge-sort logic,
  sorting only by `.first` with the left-favors-ties rule.
- Be able to implement `is_sorted_asc` as a single linear pass checking
  no adjacent inversion.

## Study checklist

- [ ] Trace one pass each of bubble, selection, and insertion sort on a
      concrete array.
- [ ] Trace one merge step of two sorted halves into a scratch array.
- [ ] Define stability and explain why selection sort lacks it.
- [ ] State the merge tie-break rule that makes merge sort stable.
- [ ] Name what std::sort actually implements.
- [ ] Explain why a correctness test alone cannot catch a disguised
      O(n^2) merge_sort.

## Practiced in

`sort-pass-tracer`, `sorting-court`, `sort-suite`
