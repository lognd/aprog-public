# Activity: Broadcast Bureau

numpy is the library nearly every scientific-computing tool in Python
is built on, and its whole value proposition rests on one idea: a
numpy ARRAY is a fixed-shape, fixed-dtype block of numbers packed
contiguously in memory, and arithmetic on arrays runs as pre-compiled
C code operating on that memory directly, not as a Python-level loop.
This activity is ten short code readings that build the mental model
underneath every numpy program you will write: what an array actually
is, how its operators differ from a Python list's operators (a trap
that catches nearly every C++-strong beginner at least once), how
BROADCASTING lets differently-shaped arrays combine, why slicing an
array is completely different from slicing a list, and how boolean
masking and per-axis reductions work.

## Concepts covered

- What a numpy array is, and how it differs from a Python list in
  memory layout and in what its operators mean
- VECTORIZATION: why array operations run as compiled code instead of
  an interpreted Python loop, and why that matters for speed
- BROADCASTING: the axis-by-axis, size-1-or-equal rule for combining
  differently-shaped arrays, and what makes a broadcast illegal
- Views vs. copies: why mutating a slice of an array mutates the
  original array too
- Boolean masking as numpy's filtering idiom
- Per-axis reductions (`sum(axis=0)` vs `sum(axis=1)`) and dtype
  promotion

## How it works

The launcher shows you ten short numpy programs, one at a time, and
asks you to predict exactly what each one prints (or whether it
errors). Type your answer. A correct answer shows a short explanation
and moves you on; a wrong answer shows an explanation of the specific
misconception behind that guess -- read those even when you get a
question right the first time, since several questions build directly
on the one before it.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly predicted the output of all ten programs and the
launcher shows you a passphrase.

## Hints

<details>
<summary>Hint 1 -- watch which type owns the operator</summary>

`*`, `+`, and the comparison operators mean something different on a
numpy array than they do on a plain Python `list`. Before predicting
an output, check the type of every value involved.

</details>

<details>
<summary>Hint 2 -- broadcasting compares shapes from the right</summary>

To check whether two shapes can combine, compare them axis by axis
starting from the LAST (rightmost) axis. Each pair of axes must be
equal, or one of them must be exactly 1.

</details>

<details>
<summary>Hint 3 -- a slice is a view, not a copy</summary>

Unlike a Python list, `array[i:j]` does not copy any elements out of
`array` -- the result shares the same underlying memory. Mutating it
mutates the original.

</details>

## Going further

- Time a vectorized `a * b` on two million-element numpy arrays against
  a Python `for` loop doing the same elementwise multiply into a plain
  list. How many times faster is the vectorized version?
- Read numpy's own broadcasting documentation and find a case with
  three or more dimensions where the rule still applies cleanly.
- What does `a[1:3].copy()` give you instead of `a[1:3]`? Verify with
  code that mutating the copy leaves the original array untouched.
