# Activity: Numeric Nuances

C++'s `int`, `float`, and `double` have direct Python counterparts, but
several of the operations you do with them behave differently in ways that
will silently produce a wrong answer if you assume C++'s rules. This
activity is seven questions, each built around a tiny snippet, covering
Python's split of C++'s single `/` into two operators, a rounding rule
that is not "always round up," integers that never overflow, and the one
piece of advice worth memorizing even though you will not fully see why
it matters yet: never use `is` to compare numbers. (`pyobject-autopsy`
covers the C-level reason: the small-int cache is an implementation
detail, not a guarantee, unlike the `None`/`True`/`False` singletons.)

## Concepts covered

- binary floating point (`float` in Python, the same IEEE 754 format as
  C++'s `double`) cannot represent most decimal fractions exactly, so
  `0.1 + 0.2 == 0.3` is `False` -- the same reason it is `False` in C++
- `round()`'s banker's rounding (round-half-to-even) for exact `.5` ties,
  instead of always-round-up
- `/` (true division, always returns a `float`) versus `//` (floor
  division, rounds toward negative infinity) -- and why `//` only matches
  C++'s `int / int` truncation for non-negative operands
- `%`'s sign follows the divisor in Python, not the dividend (the opposite
  of C++'s rule)
- `int()`'s two different jobs: parsing a `str`, and truncating a `float`
  toward zero
- Python's `int` has no fixed width and never overflows
- why `is` should never be used to compare numbers for equality, even when
  it happens to "work" for small values in a quick test

## How it works

The launcher shows you seven short pieces of Python code, one at a time,
along with a hint. Read the code and type your answer -- most questions
ask for a specific printed value, and one asks you to explain, in your own
words, why a particular habit is unsafe. A correct answer shows a short
explanation and moves you on; a wrong answer shows an explanation of the
specific misconception behind that guess. The code is shown for you to
reason about, not executed by the launcher.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly answered all seven questions and the launcher shows
you a passphrase.

## Hints

<details>
<summary>Hint 1 -- floor vs. truncate</summary>

Truncation always rounds toward zero (chops off the fractional part).
Floor always rounds toward negative infinity (down, on a number line).
They agree for positive numbers and disagree for negative ones -- work out
`-7 / 2` as an exact fraction first (`-3.5`), then ask which integer is
below it on a number line versus which integer you'd get by just deleting
everything after the decimal point.

</details>

<details>
<summary>Hint 2 -- % and // are a matched pair</summary>

Python guarantees `(a // b) * b + (a % b) == a` always holds. If you know
`a // b`, you can solve for `a % b` algebraically instead of memorizing a
sign rule.

</details>

<details>
<summary>Hint 3 -- try it yourself, but read the "why" carefully</summary>

For the questions that ask you to predict a printed value, running the
snippet yourself will always give you the right answer. For the question
about `is`, running the snippet will not settle the question by itself --
the point is understanding why the ANSWER YOU SEE can be misleading.

</details>

## Going further

- Look up Python's `decimal` and `fractions` modules. What problem does
  each one solve that plain `float` cannot?
- Predict, then check, what `-7.5 // 2` gives (mixing an `int` and a
  `float` operand). Does `//` still return an `int`, or something else?
- Run `a = 1000; b = 1000; print(a is b)` in a plain interactive Python
  session versus inside a function. Does the answer ever change? (You are
  not expected to fully explain why -- the point is to see that it CAN
  change, which is exactly why `is` is unreliable for numbers.)
