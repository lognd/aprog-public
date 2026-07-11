# Activity: Auto Consequences

Deduction Detective asked "what type does `auto` deduce here?" in the
abstract. This activity asks a sharper question: **what does that
deduction actually cost you when the program runs?** Seven small,
fully deterministic programs show `auto`'s rules producing real,
observable differences in printed output -- a copy that silently
diverges from the original it was made from, a range-for (a `for`
loop that visits each element of a container, like a `std::vector`
or `std::map`, in turn without any manual indexing) mutation that
does or does not stick depending on one `&`, and a numeric literal's
exact type changing which arithmetic operation actually executes.

## Concepts covered

- `auto` (value copy) vs. `auto&` (reference) producing two variables
  that diverge after one is modified
- Range-for over a `std::vector<int>` with `auto` (copy, no effect on
  the vector) vs. `auto&` (reference, mutates the vector)
- Range-for over a `std::map` with `auto` vs. `auto&` on
  `std::pair<const K, V>` elements
- Integer division vs. floating-point division, decided by an
  operand's literal type, and reported through `auto`
- The conditional operator `?:` requiring one common result type for
  both branches, even though only one branch's value is ever used
- Why `auto` on a string literal never gives you `.size()`, and using
  `strlen` instead

## How it works

You are shown seven short C++ programs, one at a time. For each one,
predict its exact printed output (or the value of a specific print
statement, when noted) and type your prediction. Each snippet is also
compiled and run for real by the launcher itself -- if your prediction
does not match the program's ACTUAL output, you are shown that actual
output and asked to try again, along with an explanation of the `auto`
consequence you missed. Predict every snippet's output correctly to
reveal the passphrase.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly predicted every snippet's output and the launcher
prints the passphrase.

## Hints

<details>
<summary>Hint 1 -- trace the copy and the reference separately</summary>

Whenever a snippet declares both an `auto` copy and an `auto&`
reference to the same original variable, treat them as two completely
independent storage locations from that point on, except that the
`auto&` one happens to BE the original (same storage, different name).
Track assignments to each one separately, and only the `auto&` one
ever changes the original.

</details>

<details>
<summary>Hint 2 -- integer division truncates toward zero</summary>

`7 / 2` with both operands as plain `int` performs integer division:
it computes the mathematically exact quotient and then discards
(truncates) any fractional remainder, rather than rounding to the
nearest integer. `7 / 2` is `3`, not `4` and not `3.5`. The moment
EITHER operand is a floating-point type (like `2.0` instead of `2`),
the whole expression promotes to floating-point arithmetic and keeps
the exact fractional result instead.

</details>

## Going further

- Take snippet 3 (the map range-for) and add a THIRD range-for loop at
  the end that prints `p.first`, using `auto` (not `auto&`) this time.
  Does using `auto` for a read-only pass like that cost you anything
  besides an unnecessary copy?
- Change snippet 5's conditional operator (informally called a
  "ternary" because it takes three operands) to `false ? i : d`
  instead of `true ? i : d`. Predict the new output before running it
  -- does the expression's overall TYPE change, or only which
  branch's value gets selected?
- Look up `std::is_same_v` (from `<type_traits>`) and use
  `static_assert` to check, at compile time, whether `decltype(copy)`
  in snippet 1 really is `int` and not `int&`.
