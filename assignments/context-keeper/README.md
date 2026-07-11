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

### `divide_or`

```python
def divide_or(a: float, b: float, fallback: float) -> float:
```

Returns `a / b`. If that division raises `ZeroDivisionError` (i.e.
`b == 0`), returns `fallback` instead. No other exception type is
caught here.

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
