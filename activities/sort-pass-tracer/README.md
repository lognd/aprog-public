# Activity: Sort Pass Tracer

Sorting algorithms are usually described in words ("it repeatedly swaps
adjacent out-of-order elements"), but the fastest way to actually
understand one is to trace it by hand, one concrete step at a time, on a
real array of numbers. This activity does exactly that for bubble sort,
selection sort, insertion sort, and merge sort's core merge step -- every
question states the exact implementation being traced (so there is never
any ambiguity about which version of "bubble sort" produced a given
answer) and asks you to work out precisely what happens after one pass,
or how many operations a full sort performs, or where a single element
ends up.

## Background

A **pass** is one complete walk through the array by a sorting
algorithm's outer loop -- for bubble sort, one pass compares every
adjacent pair once; for selection sort, one pass finds the minimum of
the remaining unsorted region and places it; for insertion sort, one
pass inserts exactly one new element into the already-sorted prefix
built up so far. Most of these algorithms need several passes back to
back before the whole array is sorted -- this activity asks about
individual passes, not just the final sorted result, because that is
where the actual mechanics live.

A **swap** exchanges the values at two positions in the array. A
**comparison** is a single check of which of two values is smaller (or
whether they are equal) -- every question that asks "how many
comparisons" is asking you to count these checks one at a time. An
**in-place** algorithm rearranges the array using only a small, fixed
amount of extra memory (a few temporary variables), no matter how large
the array is -- bubble sort, selection sort, and insertion sort are all
in-place. Merge sort is different: it works by repeatedly taking two
already-sorted arrays (halves of the original) and combining them into
one sorted array, one element at a time, by comparing the front of each
half and outputting whichever is smaller -- this combining process is
called a **merge step**. A merge step needs a **scratch array**, a
separate block of memory (proportional in size to the data being
merged) to build the merged result in, because it cannot safely
overwrite either of the two sorted halves it is still reading from.

## Concepts covered

- Bubble sort, selection sort, and insertion sort, traced pass by pass
- The distinction between "one pass" and "the fully sorted result"
- Counting operations (swaps, comparisons) by hand for a fixed-size input
- Merge sort's merge step: comparing two sorted halves' fronts and
  advancing one pointer at a time
- Why a tie-breaking rule (favor the left half on equal values) makes a
  merge step stable
- Concrete groundwork for the sort-suite assignment's O(n log n)
  merge_sort implementation

## How it works

Every question shows the exact canonical implementation being traced
(as a short code snippet) directly above the question, plus a hint.
Answers are either a comma-separated array (format is stated in the
question, with no spaces after commas) or a single integer. Getting a
question wrong shows a detailed explanation of exactly where the trace
went wrong; answer every question correctly to reveal the passphrase.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have answered every trace correctly and the launcher prints the
passphrase.

## Going further

- Pick one of the arrays traced in this activity and extend the trace
  by hand to the FULLY sorted result for all three of bubble, selection,
  and insertion sort. Do they all take the same number of passes to
  finish?
- Write a tiny C++ program that prints the array after every single
  pass of bubble sort, and run it on a reverse-sorted array of 10
  elements. How many passes does it actually take?
- Trace a merge step on two sorted halves that are very different
  lengths (e.g. a 1-element half and a 5-element half). Does the
  algorithm still work correctly?
