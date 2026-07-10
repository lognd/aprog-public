# Activity: Sorting Court

A round of verdicts on sorting algorithms: which one fits a given
workload, what **stability** actually means and which algorithms have
it, why the standard library's `std::sort` exists and what it actually
does under the hood, and when you should just call it instead of
hand-rolling your own. No code here -- every question is a decision or a
definition, phrased as a scenario or a direct question about behavior.

## Background

A sort is **stable** if it preserves the original relative order of any
two elements that compare **equal** on the sort key -- for example, if
you sort a list of orders by date, and two orders share the exact same
date, a stable sort guarantees those two orders keep whatever relative
order they were already in before the sort ran; an unstable sort makes
no such promise. Stability matters most when sorting by one key while
relying on an earlier sort by a different key to still hold for ties --
exactly the pattern the sort-suite assignment's `stable_sort_pairs`
depends on.

**Big-O** here describes how an algorithm's running time grows as the
input size grows: `O(n^2)` (quadratic) means the work grows roughly with
the square of the input size, while `O(n log n)` grows far more slowly.
The gap between the two is small for tiny inputs and enormous for large
ones -- this activity asks you to work out just how enormous.

## Concepts covered

- Defining stability precisely, with a concrete two-key example
- Which of bubble, insertion, selection, and merge sort are stable, and
  why selection sort in particular is not
- Matching a workload (e.g. nearly-sorted data) to the algorithm best
  suited for it
- The real cost gap between O(n^2) and O(n log n) at a realistic scale
- What `std::sort` actually implements (introsort) and why
- When to reach for `std::sort` instead of a hand-written sort in real
  code

## How it works

Each question describes a scenario or asks a direct question about
sorting behavior. Type the exact answer requested by the prompt (a
short phrase, or one of the listed options). Getting a question wrong
shows a detailed explanation of the reasoning you missed; answer every
question correctly to reveal the passphrase.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have answered every scenario correctly and the launcher prints the
passphrase.

## Going further

- Look up the actual size threshold libstdc++ or libc++ uses before
  introsort switches from quicksort to insertion sort for a small
  sub-range. Does it match your intuition for "small"?
- Time `std::sort` versus a hand-written O(n^2) sort on vectors of size
  1,000, 10,000, and 100,000. At what size does the gap become obvious?
- Construct a small example (5-6 records with two keys) and sort it by
  hand two different ways -- once stably, once unstably -- to see the
  difference in the final tie order for yourself.
