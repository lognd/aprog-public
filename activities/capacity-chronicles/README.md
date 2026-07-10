# Activity: Capacity Chronicles

`std::vector` tracks two different numbers that are easy to confuse: how
many elements are actually stored (`size()`) and how much room is
currently reserved before the next `push_back` would need to allocate a
bigger buffer (`capacity()`). This activity traces exactly how a sequence
of `reserve()`, `push_back()`, `pop_back()`, `clear()`, `assign()`, and
`resize()` calls moves those two numbers -- and only ever asks you to
predict values the C++ standard actually guarantees.

## Background

`std::vector`'s growth factor (how much bigger the buffer gets when it
runs out of room) is deliberately left **implementation-defined** by the
standard -- different standard libraries pick different factors (commonly
1.5x or 2x), and the standard never promises you a specific number. That
means a snippet that grows a vector purely through repeated `push_back`
calls and then asks you to predict the raw `capacity()` value has no single
correct answer across compilers. Every snippet in this activity avoids that
trap by pinning capacity with `reserve()` first -- `reserve(n)` is
standard-guaranteed to leave `capacity() >= n`, and every capacity this
activity asks about is set that way, so the predicted numbers are exactly
the same on any conforming compiler.

## Concepts covered

- The difference between `size()` (elements actually stored) and
  `capacity()` (room currently reserved)
- `reserve()` pinning an exact, portable capacity
- Which operations change `size()` only (`push_back`, `pop_back`, `clear`,
  `resize`) versus which can change `capacity()` (`reserve`, and a
  `push_back` or `resize` that outgrows the current capacity)
- `clear()` and `pop_back()` never releasing already-allocated capacity
- `resize()` to a smaller size (drops elements) versus a larger size
  (value-initializes new elements, 0 for `int`)

## How it works

Each snippet is a complete, compilable C++ program that reserves, fills,
and mutates a `std::vector<int>`, then prints `size()`/`capacity()` and
sometimes a few element values. Read the code, trace through it by hand,
and type the exact output -- for multi-line output you will be prompted to
enter one line at a time. The launcher compiles and runs each program
itself and checks your prediction against the real, measured output.
Predict every snippet correctly to reveal the passphrase.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly predicted the output of all seven snippets and the
launcher prints the activity's passphrase.

## Hints

<details>
<summary>Hint 1 -- capacity only ever grows, size moves both ways</summary>

Across every snippet in this activity, `capacity()` never decreases on its
own -- only `reserve()` or an internal reallocation (never triggered here,
since every capacity is pre-reserved with room to spare) can raise it.
`size()`, on the other hand, moves up with `push_back`/`assign`/`resize`
(larger) and down with `pop_back`/`clear`/`resize` (smaller).

</details>

<details>
<summary>Hint 2 -- resize() to a larger size zero-fills, it never copies</summary>

When `resize(n)` grows a vector past its current size with no explicit
fill value, the new slots are value-initialized (0 for `int`) -- they are
never copies of an already-existing element.

</details>

## Going further

- Write your own snippet that calls `reserve()` with a SMALLER value than
  the vector's current `capacity()`. What does the standard say `reserve()`
  does in that case? Verify your prediction by compiling it.
- Look up `shrink_to_fit()`. Why is its effect described as
  "non-binding" by the standard, and what does that mean for writing a
  deterministic prediction snippet about it?
- Time (with `std::chrono`) 100,000 `push_back` calls on a vector that was
  `reserve()`d up front versus one that was not. How much does avoiding
  reallocations actually save?
