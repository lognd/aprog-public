# Study Guide 56: Python Contexts & Error Handling

This module builds Python's `with` statement as the closest cousin to
C++'s RAII: `__enter__`/`__exit__` guaranteed to run regardless of normal
completion or exception, `__exit__`'s power to suppress an exception by
returning `True`, and full `try`/`except`/`else`/`finally` ordering.
`context-keeper` builds real journaling, selective-suppression,
copy-then-commit, and failure-tolerant-cleanup tools on top of it.

## Know before you start

- RAII and destructors guaranteed to run on scope exit, including during
  stack unwinding [assumed: row 21 -- OOP Implementation in C++; row 44
  -- Exception Handling]
- `throw`/`try`/`catch` mechanics and catch-type matching as the C++
  analogue for `try`/`except` [assumed: row 44 -- Exception Handling]
- Generator functions and `yield` as the mechanism behind
  `@contextlib.contextmanager` [assumed: row 54 -- Python Generators]

## Taught here

Concept: the with statement as Python's RAII cousin
- Know a class-based context manager defines `__enter__` (runs before
  the block, its return value is what `with ... as x` binds to `x` --
  not necessarily the context manager object itself) and `__exit__`
  (runs after the block).
- Know the unwind guarantee: `__exit__` is guaranteed to run whether the
  `with` block's body finished normally OR an exception propagated
  through it -- directly analogous to a C++ destructor running during
  stack unwinding.
- Know `__exit__` can deliberately suppress the exception it was just
  handed by returning a truthy value (`True`); returning `False` or
  nothing lets the exception keep propagating -- a power a C++ destructor
  does not have.
- Know `@contextlib.contextmanager` writes a context manager as a
  generator function instead of a class: code before the `yield` is
  `__enter__`'s body, the yielded value is what `with ... as x` binds,
  and code after the `yield` is `__exit__`'s body (with an exception, if
  any, raised at the `yield` point inside the generator).
- Know nested `with` blocks enter outer-to-inner and exit inner-to-outer
  -- last-in-first-out, exactly like nested C++ scopes destroying locals
  in reverse construction order.

Concept: try/except/else/finally, and exception chaining
- Know the full ordering: `try` runs first; `except` runs only if a
  matching exception was raised; `else` runs only if the `try` block
  completed with NO exception; `finally` always runs last, exception or
  not.
- Know `raise ... from ...` chains one exception as the explicit cause of
  another, preserving the original traceback context.

Concept: applying the guarantee to real tools
- Be able to write a class-based context manager (`Workspace`-style) that
  journals an open/close event unconditionally in `__enter__`/`__exit__`
  without ever suppressing.
- Be able to write a selective suppressor (`Muffle`-style) whose
  `__exit__` checks the actual exception type against a target type (or
  its subclasses) before deciding whether to suppress, never
  unconditionally swallowing everything.
- Be able to write a `@contextlib.contextmanager`-based generator with
  copy-then-commit semantics: build a working copy before yielding,
  commit changes back to the original only on a clean exit, discard the
  copy entirely if an exception propagated through the block.
- Be able to use `try`/`except` as a value-returning fallback mechanism
  (catching one specific exception type and returning a fallback value)
  rather than letting the exception propagate.
- Be able to write a cleanup loop that keeps running every remaining step
  even after one raises, collecting failure information along the way
  instead of stopping at the first failure.

## Study checklist

- [ ] Explain the with statement's unwind guarantee and its C++ RAII
      parallel.
- [ ] Predict output for a with block whose body raises, tracing
      __enter__/__exit__ calls.
- [ ] Explain how __exit__ suppresses an exception and how that differs
      from a C++ destructor's capabilities.
- [ ] Trace try/except/else/finally ordering with and without an
      exception.
- [ ] Write a selective suppressor that only catches one exception type
      (and its subclasses).
- [ ] Write a copy-then-commit context manager using
      @contextlib.contextmanager.

## Practiced in

`with-wizardry`, `context-keeper`
