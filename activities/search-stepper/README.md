# Activity: Search Stepper

Binary search is easy to describe in words and easy to get subtly wrong
in code -- the best way to build real intuition for it is to trace it by
hand, one comparison at a time, against one fixed implementation you can
hold in your head. Every question in this activity uses the exact same
10-element sorted array and the exact same canonical implementation:
`lo` starts at 0 and `hi` starts at `n` (a half-open range `[lo, hi)` --
`lo` is a valid candidate index, `hi` is one position PAST the last
candidate, the same fence-post convention `end()` uses for iterators),
the loop runs `while (lo < hi)`, `mid` is always computed as
`mid = lo + (hi - lo) / 2` (integer division, rounds down), and the
range narrows toward `lo == hi`, which becomes the final answer position
(present or not). Every answer here is a specific number or pair of
numbers, with the exact format spelled out in the question.

## Concepts covered

- The canonical `[lo, hi)` binary search implementation: initialization,
  loop condition, midpoint formula, and narrowing rule
- Tracing `mid`, `lo`, and `hi` by hand across multiple iterations
- Counting comparisons for a present target, an absent target, and a
  target at each boundary (first and last element)
- The O(log n) versus O(n) comparison-count gap between binary search
  and linear search, made concrete with actual numbers instead of just
  Big-O notation

## How it works

Each question either asks for a specific index, a specific comparison
count, or the `lo`/`hi` pair after one iteration, all against the same
fixed array and implementation. Getting a question wrong shows a
detailed step-by-step trace of the correct computation. Answer every
question correctly to reveal the passphrase.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly traced every step of the search and the launcher
prints the passphrase.

## Going further

- Write the canonical implementation from this activity in actual C++,
  add a comparison counter, and run it against the same 10-element array
  for every target from 0 to 100. Does the comparison count ever exceed
  the worst-case bound of `ceil(log2(10))` you would expect?
- Modify the implementation to early-exit the instant it finds
  `v[mid] == target`, instead of always narrowing to `lo == hi` first.
  How does that change the comparison counts from this activity? Why
  might the non-early-exiting version still be useful (hint: think about
  what happens with duplicate values in the array).
- For an array of one million sorted elements, compute by hand what the
  worst-case comparison counts would be for both linear and binary
  search, the same way this activity did for `n = 1000`. How much bigger
  does the gap get?
