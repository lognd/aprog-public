# Activity: Binary Search Autopsy

Binary search looks like a handful of simple lines -- a loop, a midpoint
computation, a comparison -- but it is notoriously easy to get subtly
wrong in ways that pass casual testing and only fail on specific inputs.
This activity puts six implementations on the autopsy table. For each
one, diagnose exactly what is wrong: an infinite loop that only triggers
on certain inputs, a bug that silently skips over a present answer, a
read past the end of the array, an integer overflow that only shows up
on enormous arrays -- or confirm that the implementation is, in fact,
completely correct. Every diagnosis is traced back to the specific line
and the specific input shape that triggers it.

## Concepts covered

- Integer overflow from `(lo + hi) / 2` versus the overflow-safe
  `lo + (hi - lo) / 2`
- The infinite-loop-on-two-elements bug from `lo = mid` instead of
  `lo = mid + 1`
- Mixing the half-open `[lo, hi)` and closed-interval `[lo, hi]`
  conventions within a single implementation
- Swapped comparison branches that search in the wrong direction
- Reading a correct implementation and confirming, category by category,
  why none of the above bugs apply to it

## How it works

Each question shows one binary search implementation and asks for a
diagnosis, chosen from five enumerated options (infinite loop on some
inputs, skips the answer, out-of-bounds read, integer overflow on huge
arrays, or correct). Getting a question wrong shows a detailed
explanation tracing exactly which input shape triggers the bug, or
confirming why a correct implementation avoids every failure mode this
activity covers. Answer every question correctly to reveal the
passphrase.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly diagnosed every implementation and the launcher
prints the passphrase.

## Going further

- Take the integer-overflow implementation from this activity and try to
  actually trigger the bug: what is the smallest array size where
  `lo + hi` could theoretically exceed `INT_MAX`? Would you ever
  realistically allocate an array that large?
- Compile the `lo = mid` infinite-loop implementation from this activity
  with a 2-element array and a target that triggers the bug, and run it
  with a timeout. Confirm it actually hangs, then apply the one-character
  fix and confirm it terminates.
- Write your own deliberately broken binary search with a NEW bug not
  covered in this activity (for example, an off-by-one in the initial
  `hi` value combined with a correct loop condition). Trace it by hand
  the way this activity's explanations do, and figure out which category
  your bug falls into.
