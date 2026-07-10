# Activity: Invariant Inspector

A **loop invariant** is a statement about a program's variables that is
true right before a loop starts, stays true after every single time the
loop body runs, and -- combined with the loop's **exit condition** (the
thing that becomes false and makes the loop stop) -- tells you exactly
what the loop has accomplished once it is done. This is the informal,
engineering-flavored version of an invariant: not a formal mathematical
proof, just a disciplined habit of naming "what stays true here, every
single time control passes through this point," so you can trust a
loop's correctness by inspection instead of by guessing and hoping. Nine
small, real loops are on the table here -- a running sum, a max-so-far
tracker, binary search's shrinking range, a two-pointer reversal, one
step of quicksort's partition, the Euclidean GCD algorithm, an
early-exit search, and a two-array merge -- and for each one you pick,
from three or four enumerated options, which statement IS the loop
invariant, as opposed to a statement that is only the **postcondition**
(true just at the end) or only happens to be true sometimes.

## Concepts covered

- The three-part definition of a loop invariant: true before the loop,
  preserved by every iteration, and combined with the exit condition to
  give the postcondition
- Distinguishing an invariant from the postcondition (true only at exit)
  and from the loop's own condition (the test that decides whether to
  keep looping, not a fact about the data)
- Off-by-one traps in invariant statements (`v[0..i-1]` versus `v[0..i]`)
- Tracing the invariant chain for a shrinking-range algorithm (binary
  search), a three-region algorithm (partition), and a mathematical
  algorithm (GCD) that leans on an outside number-theory fact

## How it works

Each question shows a short loop and a specific point in it (usually the
top of the loop body, right before that pass's work happens), then asks
which of three or four enumerated statements is the TRUE loop invariant
at that point. Getting a question wrong shows a detailed explanation
that walks the full chain -- true before, preserved by every iteration,
and what it becomes at exit -- for that specific loop. Answer every
question correctly to reveal the passphrase.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly identified the loop invariant for every scenario and
the launcher prints the passphrase.

## Going further

- Pick any loop you have already written for a past assignment. Write
  down its invariant in your own words, then check: is it true before
  the loop, preserved by every iteration, and does it combine with the
  exit condition to give you the postcondition you actually wanted?
- For the partition-step question in this activity, try writing out the
  invariant for quicksort's outer recursive structure (not just one
  inner loop) -- what has to be true about the whole array once
  partitioning and both recursive calls are finished?
