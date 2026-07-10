# Activity: With Wizardry

C++'s RAII (Resource Acquisition Is Initialization) guarantees a
destructor runs when an object leaves scope, no matter how it leaves --
normal return, or an exception unwinding the stack. Python's `with`
statement is the closest cousin to that idea: `__enter__` runs before
the block, `__exit__` runs after it, guaranteed, whether the block
finished normally or an exception blew through it. This activity is
nine short Python programs that prove that guarantee directly, alongside
the full `try`/`except`/`else`/`finally` ordering rules and the
`@contextlib.contextmanager` shorthand for writing one without a class
at all.

## Concepts covered

- A class-based context manager's `__enter__`/`__exit__` pair -- the
  RAII bridge, stated explicitly
- What `with ... as` actually binds: `__enter__`'s return value, not
  necessarily the object itself
- The unwind guarantee: `__exit__` still runs when an exception
  propagates through a `with` block
- `__exit__` returning `True` to suppress an exception entirely
- `@contextlib.contextmanager`: writing a context manager as a
  generator function, `yield` marking setup/teardown
- Full `try`/`except`/`else`/`finally` ordering, contrasted with and
  without an exception
- Nested `with` blocks: enter outer-to-inner, exit inner-to-outer
- Exception chaining with `raise ... from ...`

## How it works

The launcher runs nine short Python programs on your own interpreter
and shows you each one's source code. Predict exactly what it prints
(entering each line separately when the output has more than one
line), then type your prediction. A correct guess shows a short
explanation and moves you on; a wrong guess shows the actual output and
an explanation of the misconception behind that guess.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly predicted the output of all nine snippets and the
launcher shows you a passphrase.

## Hints

<details>
<summary>Hint 1 -- __exit__ always runs, exception or not</summary>

This is the whole point of a context manager: whether the `with`
block's body finishes normally or an exception propagates through it,
`__exit__` is guaranteed to run before that exception continues
outward (or the block simply finishes).

</details>

<details>
<summary>Hint 2 -- __exit__ returning True is a deliberate suppression signal</summary>

Unlike a C++ destructor, a Python `__exit__` can choose to swallow the
exception it was just handed, by returning a truthy value. Returning
`False` (or nothing) lets the exception keep propagating.

</details>

<details>
<summary>Hint 3 -- nested with blocks unwind like nested RAII scopes</summary>

Outer enters first, inner enters second; inner exits first, outer exits
last -- last-in-first-out, exactly like nested C++ scopes destroying
their locals in reverse construction order.

</details>

## Going further

- Write your own class-based context manager that logs how long its
  `with` block took to run, using `time.perf_counter()` in `__enter__`
  and `__exit__`.
- Rewrite one of this activity's class-based context managers using
  `@contextlib.contextmanager` instead, and confirm the printed output
  is identical.
- Look up `contextlib.suppress`. What is it, under the hood, in terms
  of `__exit__`'s return value -- and which snippet in this activity
  does its behavior most resemble?
