# Activity: Wrap Court

decorator-x-ray showed you what decorators DO, by running code and
predicting output. Wrap Court puts the underlying mechanics on trial:
what the `@` syntax literally desugars to, exactly when a decorator's own
code runs versus when the function it wraps runs, what happens when a
decorator forgets to return its wrapper, how a parameterized decorator
like `@retry(3)` adds an extra layer of function calls before the
original function ever runs, and why two small details --
`*args`/`**kwargs` and `functools.wraps` -- show up in almost every
real-world decorator you will encounter. Every explanation defines
"closure," "wrapper," and "decoration" from scratch; nothing here assumes
you already know the vocabulary.

## Concepts covered

- the exact desugaring of `@deco` above `def f(): ...`
- decoration time (when a decorator's own code executes) versus call time
  (when the wrapped function actually runs)
- what happens when a decorator's inner function is never returned
- parameterized decorators (`@retry(3)`) and the extra layer of calls they
  introduce before the decorated function is ever invoked
- why `*args` and `**kwargs` let one decorator wrap functions with
  different signatures
- `functools.wraps` and what problem it solves
- closures, defined precisely: an inner function that remembers a
  variable from its enclosing scope after that scope has returned

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
<summary>Hint 1 -- desugar first, reason second</summary>

Whenever a question involves `@something` above a `def`, the fastest way
to reason about it is to rewrite it as the equivalent assignment
statement first (`name = something(name)`), and then trace through that
assignment like any other line of code.

</details>

<details>
<summary>Hint 2 -- ask "whose body is this print statement in?"</summary>

For the decoration-time-versus-call-time questions, find every `print()`
call in the snippet and ask which function's body it lives in directly:
the decorator's own top-level body, or the nested `wrapper` function's
body. That answers when it runs.

</details>

<details>
<summary>Hint 3 -- a parameterized decorator is two function calls, not one</summary>

`@retry(3)` above `def task(): ...` desugars to `task = retry(3)(task)` --
two separate calls, back to back. `retry(3)` runs first, entirely on its
own, and only the function IT returns is then called with `task`.

</details>

## Going further

- Write out, by hand, the full desugaring of a decorator with two
  arguments, like `@retry(times=3, delay=1.0)`. How many nested functions
  does that require, total?
- Look up `functools.lru_cache`. It is a decorator (or a decorator
  factory, if called with arguments) from the standard library -- read
  its documentation and explain, in your own words, what problem it
  solves and how it differs from the decorators in this activity.
- Predict what happens if a decorator's wrapper calls `fn(*args, **kwargs)`
  but the decorator itself is applied to a function that raises an
  exception. Does the decorator "swallow" the exception by default? Try
  it.
