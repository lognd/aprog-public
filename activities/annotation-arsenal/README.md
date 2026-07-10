# Activity: Annotation Arsenal

You already know a much stricter version of this idea from C++:
`template<typename T>` lets one function work for many types, and `const`
tells the compiler (and every reader) what is not allowed to change.
Python has its own version of both ideas -- type annotations and generic
type variables -- but with a critical difference: nothing in the Python
language itself ever enforces them. An annotation, in Python, is a piece
of documentation, not a rule the interpreter checks. This activity is
nine questions on reading, choosing, and reasoning about annotations
correctly, including exactly where that "documentation, not a rule"
distinction bites -- and where a checker like `ty` or `mypy` steps in to
catch what the interpreter itself will not.

## Concepts covered

- Generic container annotations: `list[int]`, `dict[str, int]`,
  `tuple[int, ...]`, and nested containers like `list[list[int]]`
- `Optional[X]` and its Python 3.10+ equivalent, `X | None`
- Reading a `Callable[[ParamTypes], ReturnType]` signature
- `TypeVar` as Python's closest analogue to a C++ function template
  parameter, contrasted with `@overload` (closer to C++ overloading)
- What a static type checker (`ty`, `mypy`) actually reports for a
  mismatched call, and why that check is separate from running the code
- `Any` as a deliberate, honest tradeoff -- not a free win
- The mutable-default-argument trap (`def f(xs: list[int] = []):`)

## How it works

The launcher shows you nine short code snippets or signatures, one at a
time, each with a specific question: pick the correct annotation, decide
what a checker would report, or reason about a tradeoff. Type your
answer and press Enter. A correct answer shows a short explanation and
moves you on; a wrong answer explains the specific misconception behind
that guess and asks you to try again. All nine must be answered
correctly to receive the passphrase.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly answered all nine questions and the launcher shows
you a passphrase.

## Hints

<details>
<summary>Hint 1 -- annotations describe, they do not enforce</summary>

Python's own interpreter never reads a parameter or return annotation
while actually running your code. Only a separate tool -- `ty`, `mypy`,
your editor -- reads annotations, and only as a static analysis pass,
before (or entirely apart from) the program running.

</details>

<details>
<summary>Hint 2 -- TypeVar is the template, overload is the switch statement</summary>

A single `TypeVar` used in both a parameter and a return type expresses
one relationship that holds for every possible type at once -- exactly
like `template<typename T>`. `@overload` instead requires one hand-written
signature per case; anything you did not write a case for gets no
checking benefit at all.

</details>

<details>
<summary>Hint 3 -- the mutable default is built once, not once per call</summary>

`def f(xs: list[int] = []):` builds that empty list a single time, when
`f` is DEFINED -- not fresh on every call that omits `xs`. Every call
sharing the default shares the same list object.

</details>

## Going further

- Run `ty` or `mypy` over a small script with a deliberately mismatched
  call (like `double("hi")` in this activity's question 6) and read its
  actual error message. Does it point at the call site, the function
  definition, or both?
- Write your own generic function with two TypeVars, `T` and `U`, that
  takes a `dict[T, U]` and returns a `list[tuple[T, U]]`. What would the
  equivalent C++ function template signature look like?
- Fix the mutable-default trap from question 7 yourself: rewrite
  `add_item` using the `bucket: list[str] | None = None` idiom, and
  confirm with a couple of calls that each one now gets its own list.
