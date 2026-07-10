# Study Guide 49: Python Decorators

This module takes apart Python's `@` decorator syntax completely: proving
functions are ordinary first-class objects, building a decorator by hand
with no `@`, and isolating decoration time versus call time, stacking
order, parameterized decorators, and `functools.wraps`.

## Know before you start

- Lambdas and closures capturing surrounding-scope variables, as the C++
  analog for a Python closure [assumed: row 39 -- Function Pointers,
  Functors, Lambdas]
- Functions as callable values passed as parameters [assumed: row 39 --
  Function Pointers, Functors, Lambdas]
- Python's `def` with no return-type annotation, and functions as objects
  [assumed: row 46 -- Python Syntax (including OOP)]

## Taught here

Concept: functions as first-class objects, and decorators built by hand
- Know a Python function is an ordinary object: it can be assigned to a
  new name, passed as an argument, and called through that new name, just
  like any other value.
- Know a closure is an inner function that keeps a live reference to a
  variable from its enclosing function's scope, even after that enclosing
  function has already returned.
- Know a decorator is nothing more than a function that takes a function
  and returns a function.
- Know the exact desugaring: `@deco` written above `def f(): ...` is
  precisely equivalent to `f = deco(f)` executed right after `f`'s
  definition -- no hidden magic beyond that one assignment.

Concept: decoration time vs. call time
- Know a decorator function typically has two layers: its own top-level
  statements, and the body of the inner `wrapper` function it defines and
  returns.
- Know the outer layer runs ONCE, at decoration time -- the moment `@deco`
  is applied (when the `def` is executed, not when the decorated function
  is later called).
- Know the inner `wrapper`'s body runs on EVERY call to the decorated
  function -- call time, potentially many times or never.
- Know a decorator that forgets to `return wrapper` (or forgets to call
  the wrapped function inside `wrapper`) silently breaks the decorated
  function, since the name now refers to whatever the decorator actually
  returned (often `None`) instead of a working callable.

Concept: stacking, parameterization, and correctness details
- Know two stacked decorators (`@outer` above `@inner` above `def f():`)
  desugar to `f = outer(inner(f))` -- closest-to-the-function applies
  first.
- Know a parameterized decorator like `@retry(3)` involves an extra layer
  of calls: `retry(3)` runs first, entirely on its own, producing the
  actual decorator, and only the function IT returns is then called with
  the target function -- `task = retry(3)(task)`.
- Know `*args`/`**kwargs` in a wrapper let one decorator work with
  wrapped functions of any signature, since the wrapper does not need to
  know the wrapped function's exact parameter list.
- Know `functools.wraps` copies metadata (like `__name__` and the
  docstring) from the original function onto the wrapper, fixing what
  would otherwise look like every decorated function having the name and
  docstring of `wrapper` itself.

## Study checklist

- [ ] Rewrite any @deco usage as its equivalent f = deco(f) assignment.
- [ ] For a given decorator snippet, identify which print statements run
      at decoration time vs. call time.
- [ ] Explain what happens if a decorator forgets to return its wrapper.
- [ ] Expand @outer @inner def f(): ... into nested calls and state
      evaluation order.
- [ ] Expand @retry(3) into its two-call desugaring.
- [ ] Explain what functools.wraps fixes and what breaks without it.

## Practiced in

`decorator-x-ray`, `wrap-court`
