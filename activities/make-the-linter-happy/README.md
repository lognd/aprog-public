# Activity: Make the Linter Happy

Real Python teams do not rely on willpower to keep code healthy -- they
run tools. This activity drops you into a small snack-stand ledger
project that is broken in four different ways, one for each tool in the
standard Python quality toolbox: the LINTER complains, the FORMATTER
complains, the TYPE CHECKER complains, and one TEST fails. Your job is
to work the findings down to zero on all four fronts.

None of these tools existed by accident. Each one automates a category
of code review a human used to do by eye: "you never use this import,"
"this file is formatted differently from every other file," "you
promised this function returns an `int` but sometimes it returns
nothing," "this function gives the wrong answer at the boundary." The
tools are faster than the human, never tired, and never embarrassed to
repeat themselves.

## Concepts covered

- What a linter is and how to read a `ruff check` finding
- What a code formatter is and why `ruff format` has no opinions to argue with
- What a static type checker is and how `ty` reads annotations that the
  interpreter ignores (the annotation-arsenal lesson, now with the reader
  attached)
- Reading a pytest failure report: the assertion, the two values, the arrow
- The fix loop discipline: run, read the FIRST error, fix the smallest
  thing, rerun

## Background

The four tools, and what each one is for:

**ruff check** is a LINTER: a program that reads your source code
(without running it) and flags patterns that are legal Python but almost
certainly mistakes -- an import you never use, a name you typo'd, a
default argument that will haunt you. Here is a real finding, annotated:

```
F821 Undefined name `totl`          <- rule code and one-line summary
  --> report.py:13:43               <- file : line : column
   |
13 |     lines.append('gross: ' + format_cents(totl))
   |                                           ^^^^   <- the exact spot
   |
```

Read it inside-out: the caret points at the exact expression, the
`file:line:column` tells you where to open your editor, and the rule
code (`F821`) is searchable if the one-line summary is not enough.

**ruff format** is a FORMATTER: it rewrites layout -- spacing, quotes,
line breaks -- to one canonical style. It never changes what the code
does, only how it looks. `ruff format --check` lists the files it WOULD
rewrite; `ruff format` (no flag) actually rewrites them. There is
nothing to figure out here, and that is the point: formatting is the one
argument a team can make vanish entirely by letting a tool win it.

**ty check** is a STATIC TYPE CHECKER. Remember the punchline of the
annotation-arsenal activity: annotations are inert -- the interpreter
stores them and never looks at them again. They stay inert until a
checker reads them, and ty is the reader. It takes every promise your
annotations make (`cents: int`, `-> int`) and checks, without running
the program, whether the code can break that promise. Annotated:

```
error[invalid-return-type]: Function can implicitly return `None`,
                            which is not assignable to return type `int`
  --> pricing.py:22:38          <- where the broken promise was declared
   |
22 | def shipping_cents(subtotal: int) -> int:
   |                                      ^^^  <- the promise itself
```

"Implicitly return `None`" means some path through the function falls
off the end without a `return` statement -- Python silently returns
`None` there, and `None` is not an `int`. Note that no test in this
project catches that bug: no test calls the function with a small
enough value. The type checker catches what the tests never exercise.

**pytest** runs the project's tests. A failing test prints the
assertion that failed and both sides of the comparison:

```
>       assert bulk_discount_cents(200, 10) == 1800
E       assert 2000 == 1800                       <- actual vs expected
E        +  where 2000 = bulk_discount_cents(200, 10)
```

The test encodes what the menu PROMISES; the code disagrees. When a
test fails, first decide which side is right -- here, read the test's
comment and the function's docstring, then fix the side that is lying.

<details>
<summary>Where do mypy and black fit in?</summary>

`ruff` and `ty` are recent, very fast tools, but the categories are much
older. **black** is the classic Python formatter (`ruff format` is
deliberately black-compatible), and **mypy** is the classic type checker
that first made annotations useful at scale. You have both installed --
after finishing the activity, try `black --check .` and `mypy .` in the
same directory and compare their output with ruff's and ty's. The
findings overlap heavily; the vocabulary differs slightly. The gates in
this activity only check ruff, ty, and pytest, so this comparison is
purely for your own calibration.

</details>

## How it works

The launcher unpacks a fresh copy of the project and drops you into a
shell inside it. The project has three modules (`inventory.py`,
`pricing.py`, `report.py`), a `tests/` directory, and a `pyproject.toml`
that configures ruff and pytest. Seeded into it are roughly:

- five `ruff check` findings (one typo produces TWO of them -- fixing
  the undefined name also removes the "assigned but never used" finding)
- two files `ruff format --check` wants to rewrite
- four `ty check` diagnostics (one overlaps with the ruff typo finding;
  tools sometimes catch the same bug in different vocabularies)
- one failing test

When you `exit` the shell, the launcher reruns all four commands itself
in your working directory -- it trusts the tools, not you -- and unlocks
the passphrase only when every gate passes.

## Getting started

The tools must be installed first. If any of `ruff`, `ty`, or `pytest`
is missing, revisit the env-setup-python activity; each installs with
`uv tool install <name>`.

```bash
python3 launch.py
```

A shell opens inside a fresh copy of the project.

### Step 1 -- make the linter happy

```bash
ruff check .
```

Now the discipline that makes this activity worth doing: read the FIRST
finding only. Ignore everything below it. Fix the smallest thing the
caret points at, then run `ruff check .` again. Findings sometimes
cause each other, so the list can shrink by more than one -- which is
exactly why fixing from the top and rerunning beats trying to fix the
whole list from one reading. Repeat until: `All checks passed!`

### Step 2 -- make the formatter happy

```bash
ruff format --check .
```

It names the files it would rewrite. Let it:

```bash
ruff format .
ruff format --check .
```

Look at what changed (`diff` against your memory, or just reread the
file) -- the formatter fixed layout only, never behavior.

### Step 3 -- make the type checker happy

```bash
ty check .
```

Same loop: first diagnostic, smallest fix, rerun. Fix the code so it
keeps the promise, or fix the annotation so it tells the truth --
never delete the annotation just to silence the checker.

### Step 4 -- make pytest happy

```bash
pytest -q
```

One test fails. Read the assertion, decide whether the test or the code
is lying (the comment in the test and the docstring on the function
agree with each other), and fix the liar. Rerun until all tests pass.

### Step 5 -- exit

```bash
exit
```

The launcher reruns all four gates itself. If one fails, it shows you
that tool's output and offers to drop you back in.

## You will know you are done when...

All four commands pass inside the shell, and after you `exit`, the
launcher's own run of all four gates is green and it prints the
passphrase.

## Hints

<details>
<summary>Hint 1 -- the mutable default argument</summary>

`extra: list[str] = []` builds ONE list when the function is defined,
not a fresh list per call -- every call that omits `extra` shares that
same list. This is the trap from the annotation-arsenal activity. The
idiomatic fix is the `None` default: annotate `list[str] | None = None`
and build a fresh list inside the body when the argument is `None`.

</details>

<details>
<summary>Hint 2 -- ty says a function "can implicitly return None"</summary>

Trace every path through the function. An `if` chain with no final
`return` falls off the end for any input that matches none of the
conditions, and falling off the end returns `None`. The docstring says
what that last path should return.

</details>

<details>
<summary>Hint 3 -- the failing test</summary>

The menu promise is "10 or more." The comparison in the code is strict
(`>`). Boundary bugs live exactly on the boundary: quantity 10 should
get the discount and does not.

</details>

## Going further

- Run `black --check .` and `mypy .` on your finished, all-green
  project. Do the classic tools agree with ruff and ty? Where does the
  wording differ for the same idea?
- Break one thing on purpose (re-add the unused import) and watch which
  gates catch it. Then break the shipping function's annotation instead
  (`-> int` to `-> None`) and see what NEW errors ty reports at the call
  sites -- a wrong annotation is worse than no annotation, because the
  checker believes it.
- Look up the rule code B006 in ruff's documentation and read the other
  "bugbear" rules. Each one is a bug some team shipped often enough
  that someone automated the review comment.
- Add `--fix` to `ruff check` on a fresh copy (rerun `python3 launch.py`)
  and see which findings ruff repairs automatically and which it
  refuses to touch. Why can a tool safely auto-remove an unused import
  but not auto-fix an undefined name?
