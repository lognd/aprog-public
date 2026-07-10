# Activity: Type Inspector

Python variables have no declared type at all -- `type(x)` always reports
whatever `x` actually, currently is, and that can change from one
assignment to the next. This activity is eight questions on what that
means in practice: what `type()` reports for plain literals and simple
expressions (including a division operator that always returns a float,
even on two ints); `isinstance()` checked against a tuple of acceptable
types; the surprising fact that `bool` is a genuine subclass of `int`,
not merely convertible to one; and, the centerpiece of the activity, the
fact that type annotations (`def f(x: int) -> int:`) are never checked or
enforced by Python itself while a program runs -- they are documentation,
checked (if at all) by a separate static-analysis tool like `ty` or
`mypy`, before the program ever executes. The last two questions cover
duck typing versus explicit `isinstance` checks, and the real difference
between `type(x) is SomeClass` and `isinstance(x, SomeClass)` once
subclasses enter the picture.

## Concepts covered

- `type()` on literals and expressions, including why `/` always produces
  a `float` in Python 3 even on two `int` operands, while `//` does not
- `isinstance()` with a tuple of types, matching any one of them
- `bool` as a genuine subclass of `int` -- what that implies for
  arithmetic and for `isinstance` checks
- type annotations as pure, unenforced documentation: the difference
  between Python's interpreter (never checks annotations) and a static
  type checker like `ty` or `mypy` (checks them before the program runs,
  by reading the source, not by running it)
- duck typing ("does it support the method I need?") versus an explicit
  `isinstance` check, and which one is idiomatic Python for a given job
- `type(x) is SomeClass` versus `isinstance(x, SomeClass)` once a
  subclass is involved -- one of these correctly recognizes "is-a"
  relationships and one does not

## How it works

The launcher asks eight questions, one at a time, each with a short code
snippet and a hint. Type your answer in your own words (or as the exact
phrase, value, or line of code the question calls for) and press Enter. A
correct answer shows a full explanation and moves you to the next
question; a wrong answer -- if it matches a known misconception -- shows
why that specific answer is wrong, and otherwise asks you to reread the
snippet and try again.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly answered all eight questions and the launcher shows
you a passphrase.

## Hints

<details>
<summary>Hint 1 -- annotations are never checked while the program runs</summary>

Whenever a question involves a type annotation (`x: int`, `-> str`,
`list[int]`), remember that Python's own interpreter never reads or
enforces it during a normal run. Trace what the code would ACTUALLY do
with the ACTUAL values passed in, ignoring the annotation entirely, and
that trace is your answer.

</details>

<details>
<summary>Hint 2 -- bool is an int, not just int-like</summary>

`isinstance(True, int)` is `True` because `bool` genuinely inherits from
`int` -- this is not a special case or a coincidence, it is real
inheritance, and it explains why arithmetic on `True`/`False` values
(`True + True`) works at all.

</details>

<details>
<summary>Hint 3 -- type() ignores inheritance; isinstance() does not</summary>

`type(x) is SomeClass` is a strict, exact-match comparison against a
SINGLE class. `isinstance(x, SomeClass)` walks x's entire inheritance
chain. For any question comparing the two, ask whether the class in
question is x's exact type, or merely one of its ancestors.

</details>

## Going further

- Install `ty` or `mypy` (whichever your course toolchain uses) and run
  it against the `add(a: int, b: int) -> int:` snippet from this activity,
  called with two strings. Confirm it flags the mismatch that Python
  itself silently ran without complaint.
- Write a function with a `list[int]` parameter annotation, then call it
  with a list containing a mix of `int` and `str` values. Predict what
  happens at runtime versus what a static type checker would report,
  before running either check.
- Look up `typing.runtime_checkable` and `Protocol` (part of the standard
  library's `typing` module). How do they let you combine something close
  to duck typing with an explicit `isinstance`-style check?
