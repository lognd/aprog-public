# Context Keeper

With Wizardry proved that a `with` statement guarantees `__exit__` runs
no matter how the block ends -- normal completion or an exception
unwinding through it -- and that `__exit__` can choose to suppress an
exception by returning `True`. This assignment turns those two facts
into real, useful tools: a workspace that journals every open and
close, a suppressor that only catches the exception type it is told to
catch (not everything), a transaction that only commits on a clean
exit, and a cleanup runner that keeps going even when individual steps
fail. The graded contract is not just "does it produce the right
value" -- it is "does it enter, exit, suppress, commit, and continue
in exactly the order and under exactly the conditions specified,"
proven with hidden tests that watch the exact sequence of events, not
just the final result.

## Learning goals

- Write a class-based context manager (`__enter__`/`__exit__`) and
  understand the unwind guarantee: `__exit__` always runs, exception or
  not
- Use `__exit__`'s return value deliberately to suppress an exception
  only when it matches a specific type (including subclasses), never
  unconditionally
- Write a `@contextlib.contextmanager`-based generator function with
  copy-then-commit semantics, distinguishing a clean exit from an
  exception-driven one
- Practice `try`/`except` as a value-returning fallback mechanism
  (`divide_or`), rather than letting an exception propagate
- Write a loop that keeps running every remaining step even after one
  raises, collecting what went wrong along the way, instead of stopping
  at the first failure

## Examples at a glance

To make all five pieces concrete at once, here is **one** scenario that
touches every function/class in the assignment. Two `Workspace` blocks are
nested inside each other; inside the innermost one, a `Muffle` wraps a
`transaction` block that appends to a working copy and then raises. A
`cleanup_chain` and `divide_or` example follow separately, since they do not
nest inside the `with` blocks above.

```python
journal = []
ledger = [10, 20]
m = Muffle(ValueError)

with Workspace(journal) as outer:      # outer.__enter__ -> journal: ["open"]
    with Workspace(journal) as inner:  # inner.__enter__ -> journal: ["open", "open"]
        with m:                        # Muffle.__enter__ -> returns self, nothing journaled
            with transaction(ledger) as working:
                working.append(30)      # working is now [10, 20, 30]; ledger untouched so far
                raise ValueError("bad entry")
        # execution resumes HERE: Muffle caught the ValueError
```

| Call / attribute | Value after the scenario | Why |
|---|---|---|
| `journal` | `["open", "open", "close", "close"]` | both `Workspace.__enter__` calls fire first (outer, then inner), then both `__exit__` calls fire in reverse order (inner closes before outer) -- `__exit__` always appends `"close"`, exception or not |
| `ledger` | `[10, 20]` (unchanged) | the `ValueError` propagated out of the `transaction` block's body, so `transaction` discards `working` and never mutates `ledger`; the original is left exactly as it was |
| `m.caught` | `["ValueError"]` | `Muffle(ValueError)` matches the raised `ValueError` exactly, so it records the type name and suppresses it (returns `True` from `__exit__`) -- the exception never reaches the `Workspace` blocks above |
| does the `TypeError`-vs-`ValueError` distinction matter here? | yes | if the raised exception were a `TypeError` instead, `Muffle(ValueError)` would NOT match it, so it would propagate up through both `Workspace.__exit__` calls (still journaling `"close"` twice) and out of the whole `with` chain -- see the walkthrough below for this exact case |

```python
steps_log = []
def step_ok():   steps_log.append("step1-ok")
def step_bad():  steps_log.append("step2-attempted"); raise KeyError("missing")
def step_ok2():  steps_log.append("step3-ok")

cleanup_chain([step_ok, step_bad, step_ok2])
```

| Call | Result | Why |
|---|---|---|
| `steps_log` after the call | `["step1-ok", "step2-attempted", "step3-ok"]` | every step runs, including `step_ok2` after `step_bad` raised -- `cleanup_chain` never stops early |
| `cleanup_chain([step_ok, step_bad, step_ok2])` | `["KeyError"]` | only the failing step contributes to the returned list, recorded by its exception type's name |
| `divide_or(9.0, 3.0, -1.0)` | `3.0` | ordinary division succeeds, so the fallback is never used |
| `divide_or(9.0, 0.0, -1.0)` | `-1.0` | dividing by zero raises `ZeroDivisionError`, which `divide_or` catches and replaces with `fallback` |

## Worked example: watch the nested `with` blocks run, step by step

This is the trickiest part of the assignment -- getting the enter/exit order
and the exception-suppression boundary exactly right -- so here is every step
of the scenario above spelled out, plus the mirror-image case where the
exception does NOT match `Muffle`'s type.

### Case 1: the raised exception matches `Muffle`'s type (suppressed)

| Step | Code executing | What happens | `journal` after this step |
|---|---|---|---|
| 1 | `Workspace(journal)` outer `__enter__` | appends `"open"` | `["open"]` |
| 2 | `Workspace(journal)` inner `__enter__` | appends `"open"` | `["open", "open"]` |
| 3 | `Muffle.__enter__` | returns `self`; nothing journaled (`Muffle` does not touch `journal` at all) | `["open", "open"]` |
| 4 | `transaction(ledger)` generator starts | builds `working = list(ledger)`, i.e. `[10, 20]`, then yields it | `["open", "open"]` |
| 5 | `working.append(30)` | `working` becomes `[10, 20, 30]`; `ledger` itself is still `[10, 20]` | `["open", "open"]` |
| 6 | `raise ValueError("bad entry")` | exception starts propagating out of the `with transaction(...)` block | `["open", "open"]` |
| 7 | `transaction`'s generator resumes at the `yield` with the exception | the `except BaseException: raise` branch fires -- `ledger` is never touched, so the rollback is simply "do nothing and let it propagate" | `["open", "open"]` |
| 8 | `Muffle.__exit__(ValueError, ...)` | `issubclass(ValueError, ValueError)` is true, so it appends `"ValueError"` to `m.caught` and returns `True` -- the exception stops here | `["open", "open"]` |
| 9 | control resumes normally after the `with m:` block (no exception in flight) | | `["open", "open"]` |
| 10 | inner `Workspace.__exit__(None, None, None)` | appends `"close"` (always runs, exception or not) and returns `False` | `["open", "open", "close"]` |
| 11 | outer `Workspace.__exit__(None, None, None)` | appends `"close"` | `["open", "open", "close", "close"]` |

Final state: `journal == ["open", "open", "close", "close"]`, `ledger == [10, 20]`,
`m.caught == ["ValueError"]`. Note the **exit order is the reverse of the
enter order** -- inner closes before outer -- exactly like nested RAII
destructors or a stack unwinding.

### Case 2: the raised exception does NOT match `Muffle`'s type (propagates)

Change step 6 to `raise TypeError("wrong type")` instead. Everything through
step 7 is identical (the `transaction` still discards its working copy and
lets the exception through). But at step 8, `Muffle.__exit__(TypeError, ...)`
checks `issubclass(TypeError, ValueError)`, which is `False` -- so `Muffle`
returns `False` and does NOT suppress. The `TypeError` keeps propagating
through both `Workspace.__exit__` calls (each still appends `"close"`,
because `__exit__` always runs regardless of what is propagating) and out of
the entire nested `with` chain to whatever code called it. Final state:
`journal == ["open", "open", "close", "close"]` (identical to Case 1 --
`Workspace` does not care whether an exception was suppressed further in),
`ledger == [1, 2, 3]` unchanged, `m.caught == []` (nothing was actually
caught), and the `TypeError` is now live and must be caught by an outer
`try`/`except` or it crashes the program.

---

## Task

Implement five pieces of context-manager and exception-handling
machinery in a file named `context_keeper.py`.

### `Workspace`

```python
class Workspace:
    def __init__(self, journal: list[str]) -> None: ...
    def __enter__(self) -> "Workspace": ...
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool: ...
```

A context manager that shares a journal (an ordinary list of strings)
with whoever constructs it. `__enter__` appends `"open"` to that
journal and returns `self`. `__exit__` appends `"close"` to the journal
**always** -- whether the `with` block finished normally or an
exception is propagating through it -- and does **not** suppress:
whatever exception was in flight keeps propagating.

*Examples:*
- `journal = []`; `with Workspace(journal): pass` -> `journal == ["open", "close"]` (clean exit still journals both).
- `journal = []`; `with Workspace(journal): raise ValueError("boom")` -> `journal == ["open", "close"]` **and** the `ValueError` still propagates out of the `with` block (`Workspace` never suppresses).
- Two `Workspace`s nested, inner one raises: `journal == ["open", "open", "close", "close"]` -- exits happen in reverse order of entries, and the exception still escapes both.
- `ws = Workspace(journal)`; after `with ws: pass`, `ws.journal is journal` -- it is the *same* list object, not a copy, so appends are visible to the caller immediately.



### `Muffle`

```python
class Muffle:
    def __init__(self, exc_type: type[BaseException]) -> None: ...
    def __enter__(self) -> "Muffle": ...
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool: ...
```

A context manager that suppresses **only** exceptions whose type is
exactly `exc_type`, or a subclass of it. Any other exception type
propagates normally, unsuppressed. Every exception it actually
suppresses gets its type's name (e.g. `"ValueError"`) appended, in
order, to a `.caught` list attribute (an empty list at construction).

*Examples:*
- `with Muffle(ValueError): raise ValueError("boom")` -> nothing escapes the `with` block; `m.caught == ["ValueError"]` (exact type match).
- `class MyValueError(ValueError): pass`; `with Muffle(ValueError): raise MyValueError("boom")` -> also suppressed, because `MyValueError` is a *subclass* of `ValueError`; `m.caught == ["MyValueError"]`.
- `with Muffle(ValueError): raise TypeError("nope")` -> the `TypeError` is NOT suppressed and keeps propagating; `m.caught` stays `[]` (only exceptions actually caught get recorded).
- `m = Muffle(ValueError)`; `with m: pass` (nothing raised) -> `m.caught == []`; `__exit__` still runs and returns `False`, but there is nothing to suppress or record.

### `transaction`

```python
@contextmanager
def transaction(ledger: list) -> Iterator[list]:
```

A `@contextlib.contextmanager`-based generator function. It yields a
**working copy** of `ledger` (built once, at the start, before the
`with` block's body runs). If the `with` block's body finishes
cleanly, `transaction` commits: it mutates the original `ledger` in
place so its contents match the working copy exactly. If an exception
propagates out of the `with` block's body instead, `transaction`
discards the working copy entirely -- `ledger` is left exactly as it
was before the `with` block started -- and the exception continues
propagating (this function never suppresses anything).

*Examples:*
- `ledger = [1, 2, 3]`; `with transaction(ledger) as working: working.append(4)` -> after the block, `ledger == [1, 2, 3, 4]` (clean exit commits).
- `ledger = [1, 2, 3]`; `with transaction(ledger) as working: working.append(4); raise ValueError` -> after the block (caught by an outer `try`/`except`), `ledger == [1, 2, 3]` unchanged -- the exception rolled the working copy back before it ever reached `ledger`.
- `with transaction(ledger) as working: assert working is not ledger` -- `working` is always a fresh copy (`list(ledger)`), never the same object, so mutating it never touches `ledger` until commit.
- `ledger = []`; `with transaction(ledger) as working: pass` -> `ledger == []` still -- committing an unchanged empty copy onto an empty ledger is a no-op, not an error.

### `divide_or`

```python
def divide_or(a: float, b: float, fallback: float) -> float:
```

Returns `a / b`. If that division raises `ZeroDivisionError` (i.e.
`b == 0`), returns `fallback` instead. No other exception type is
caught here.

*Examples:*
- `divide_or(10.0, 2.0, -1.0) == 5.0` -- ordinary division, no error, `fallback` unused.
- `divide_or(10.0, 0.0, -1.0) == -1.0` -- `b == 0` raises `ZeroDivisionError`, caught and replaced with `fallback`.
- `divide_or(0.0, 5.0, -1.0) == 0.0` -- dividing zero by a nonzero number is not an error; the real result (`0.0`) is returned, not `fallback`.

### `cleanup_chain`

```python
def cleanup_chain(steps: list[Callable[[], None]]) -> list[str]:
```

Calls every callable in `steps`, in order, with no arguments. If a step
raises any `Exception`, `cleanup_chain` does **not** stop -- it
continues on to every remaining step regardless -- and records that
exception's type name (e.g. `"ValueError"`) in a returned list, in the
order the failures happened. Steps that succeed contribute nothing to
the returned list.

*Examples:*
- `cleanup_chain([lambda: None, lambda: None])` -> `[]` -- both steps ran and succeeded, so nothing is recorded.
- `cleanup_chain([ok, bad, ok])` where `bad` raises `ValueError` -> `["ValueError"]`, and `ok` (both copies) still ran -- one failure does not stop the chain.
- Two failing steps, e.g. `bad1` raises `KeyError` then `bad2` raises `TypeError` -> `["KeyError", "TypeError"]`, in the exact order the failures happened, not the order the steps appear if some are skipped.
- `cleanup_chain([])` -> `[]` -- an empty step list is not an error, it just returns an empty list immediately.

### Examples

```python
>>> journal = []
>>> with Workspace(journal):
...     journal.append("work")
>>> journal
['open', 'work', 'close']

>>> m = Muffle(ValueError)
>>> with m:
...     raise ValueError("boom")
>>> m.caught
['ValueError']

>>> ledger = [1, 2, 3]
>>> with transaction(ledger) as working:
...     working.append(4)
>>> ledger
[1, 2, 3, 4]

>>> divide_or(10.0, 0.0, -1.0)
-1.0

>>> def ok(): pass
>>> def bad(): raise ValueError("boom")
>>> cleanup_chain([ok, bad, ok])
['ValueError']
```

## Files

| File | Purpose |
|------|---------|
| `context_keeper.py` | Write your implementation here |

## Compilation and Testing

```bash
python -m pytest visible-tests/test_visible.py -v
```

## Constraints

- Do not rename `context_keeper.py`, or rename/remove any class or
  function.
- Type hints are required on every function/method's parameters and
  return type, matching the signatures above.
- Stdlib only (`contextlib` is explicitly allowed -- it is the standard
  tool for `transaction`'s `@contextmanager` decorator).
- `Muffle.__exit__` must suppress exact-or-subclass matches of its
  `exc_type` only; every other exception type must propagate normally.
- `transaction` must never mutate the original `ledger` argument except
  at the moment of a clean commit.
- **Type-annotation bonus (10 pts):** every method and function must annotate all of its parameters (except a leading `self`/`cls`) and its return type. The bonus is awarded only when everything is fully annotated; a separate, informational [ty](https://docs.astral.sh/ty/) check then flags any annotation on `context_keeper.py` that does not hold up.

## Grading

| Component                           | Points |
|--------------------------------------|--------|
| Import constraints (gate)            | 5      |
| Visible correctness tests            | 35     |
| Hidden correctness tests             | 50     |
| Complete type annotations (bonus)    | 10     |
| **Total**                            | **100** |

Hidden tests cover: exit-on-exception ordering (including nested
`Workspace` blocks), `Muffle`'s exact-type vs. subclass vs.
non-matching passthrough behavior, `transaction`'s commit and rollback
both observed directly through the ledger's own state, `cleanup_chain`
continuing past multiple failures while preserving their order, and
exact journal sequences across nesting.

## Submission

Submit your implementation as `context_keeper.py`. Do not rename it.

## Going further

- Add a `retry(fn, attempts)` helper that calls `fn` up to `attempts`
  times, returning on the first success and re-raising the last
  exception if every attempt fails. How does it relate to
  `cleanup_chain`'s "keep going" philosophy?
- Rewrite `Workspace` using `@contextlib.contextmanager` instead of a
  class. Does a `try`/`finally` inside the generator body reproduce the
  "close always runs" guarantee exactly?
- What would have to change about `transaction` to support nested
  transactions, where an inner transaction's rollback should not
  discard an outer transaction's already-committed changes?
