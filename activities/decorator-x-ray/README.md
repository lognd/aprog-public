# Activity: Decorator X-Ray

The `@` syntax above a Python function definition looks like a small
annotation, but it is actually a full function call happening behind the
scenes, at a very specific moment. This activity takes that syntax apart,
snippet by snippet: first by proving that Python functions are ordinary
objects you can pass around like any other value, then by building a
decorator by hand with no `@` at all, then by putting the `@` form and the
hand-written form side by side to show they produce identical results.
The last few snippets isolate the single biggest "aha" moment for
decorators -- that a decorator's own code runs once, at the moment a
function is defined, while the wrapper it builds runs again on every
call -- plus what happens when two decorators are stacked, and why
`functools.wraps` exists.

## Concepts covered

- functions as first-class objects: assigning a function to a new name,
  passing it as an argument, and calling it through that new name
- closures: an inner function that keeps a live reference to a variable
  from its enclosing function's scope, even after that enclosing function
  has already returned
- writing a decorator by hand (a function that takes a function and
  returns a function) and the exact equivalence between `@deco` and
  `f = deco(f)`
- the difference between decoration time (when a decorator's own code
  runs) and call time (when the function it wraps is actually invoked)
- stacking two decorators, and the "closest to the function applies
  first" ordering rule
- `functools.wraps`, and what a decorated function's `__name__` looks
  like without it

## How it works

The launcher shows you nine short Python programs, one at a time. Read
the code, predict exactly what it prints (entering each line separately
if the output has more than one line), and type your prediction. A
correct guess shows a short explanation and moves you on; a wrong guess
shows the actual output and, for many wrong answers, an explanation of
the specific misconception behind that particular guess. Every snippet
actually runs on your own Python interpreter -- nothing here is scripted
or faked.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly predicted the output of all nine snippets and the
launcher shows you a passphrase.

## Hints

<details>
<summary>Hint 1 -- a decorator is just a function, nothing more</summary>

Every decorator in this activity is an ordinary function that happens to
take another function as its argument and return a function as its
result. If a snippet confuses you, try mentally replacing `@deco` above
`def f(): ...` with the explicit line `f = deco(f)`, written right after
`f`'s definition -- that line is exactly what `@deco` does.

</details>

<details>
<summary>Hint 2 -- separate a decorator's own body from its wrapper's body</summary>

A decorator function usually contains two layers of code: its own
top-level statements, and the body of the inner `wrapper` function it
defines and returns. The outer layer runs once, when `@deco` is applied.
The inner layer (`wrapper`'s body) runs every time the decorated function
is actually called. Ask which layer a given `print()` line lives in
before predicting when it fires.

</details>

<details>
<summary>Hint 3 -- for the stacking snippet, expand it into nested calls</summary>

`@outer` above `@inner` above `def f(): ...` desugars to
`f = outer(inner(f))`. Work out which call happens first by reading that
expression the way you would evaluate any nested function call in
C++ or Python: innermost first.

</details>

## Going further

- Write a `timer` decorator using `time.perf_counter()` that prints how
  long the wrapped function took to run. Does it need `functools.wraps`
  to work correctly? Does it need it to be well-behaved?
- Take the parameterized `@retry(3)` idea from wrap-court and actually
  implement it: a decorator factory that retries a function up to N times
  if it raises an exception, only re-raising after all attempts fail.
- Remove `functools.wraps` from a decorator you have written and call
  `help()` on the decorated function. What does the docstring show, and
  why?
