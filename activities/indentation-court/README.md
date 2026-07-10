# Activity: Indentation Court

C++ uses `{ }` to mark where a block of code begins and ends; indentation is
just for humans, and the compiler does not care about it at all. Python has
no `{ }` -- indentation itself is the syntax that marks a block. That single
difference has consequences you need to reason about precisely, especially
the biggest one: unlike a C++ `{ }` block, Python's `if`/`for`/`while`
blocks do not create a new variable scope. This activity is a set of
"read the code, name the verdict" questions about exactly how Python's
structural rules work.

## Concepts covered

- indentation as block-membership syntax (no `{ }` in Python at all)
- the mandatory trailing colon (`:`) on every block-opening line
  (`if`, `for`, `while`, `def`, `class`, ...)
- Python has **no block scope** -- a variable assigned inside an `if` or
  `for` is still visible after it ends, unlike a C++ variable declared
  inside `{ }`
- every Python function returns a value, even with no `return` statement
  (it implicitly returns `None`)
- truthiness: which values count as `False` in a condition even though they
  are not literally the boolean `False` (empty containers, `0`, `""`)
- the `is None` convention for checking "no value here," and why it is
  preferred over `== None`

## How it works

The launcher shows you a short piece of Python code and a question about
what it means or what it does, phrased as a specific verdict to name (for
example: does a line run, and if so, when -- or is this a syntax error).
Answer in your own words matching the expected phrasing; wrong answers show
an explanation of the specific misconception behind that guess, then let
you try again. A correct answer shows the full explanation before moving to
the next question.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly answered all eight questions and the launcher shows you
a passphrase.

## Hints

<details>
<summary>Hint 1 -- count the leading spaces</summary>

When a question hinges on indentation, literally count the number of
leading spaces on each line being compared. Python's rule is exact and
mechanical: same indentation depth as the block-opening line means "not
part of that block."

</details>

<details>
<summary>Hint 2 -- "no block scope" is the big one</summary>

If a question involves a variable assigned inside an `if` or `for` and then
used afterward, remember: in Python, only `def` (functions), `class`
bodies, `lambda`, and comprehensions create a new scope. `if`, `for`,
`while`, and `with` do not. A variable assigned inside one of those is a
normal variable in the *enclosing* scope, visible before and after.

</details>

## Going further

- Try running a snippet where a variable is assigned inside an `if` whose
  condition is `False` on every path, then used afterward. What error do
  you get, and how is it different from a C++ "used before declared" error?
- Python's `for` loop has an optional `else` clause (`for ... else:`) that
  runs only if the loop completes without hitting a `break`. It is not part
  of this activity -- look it up and write a five-line program that uses it
  to search a list for a value.
- What does `bool([])`, `bool(0)`, and `bool("")` print if you call them
  directly at a Python prompt, instead of using them inside an `if`?
