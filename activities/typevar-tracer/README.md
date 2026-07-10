# Activity: TypeVar Tracer

Annotation Arsenal covered how to read and choose annotations; this
activity proves, by actually running code and watching the output, what
annotations do (and mostly do not do) at runtime. A `TypeVar` looks like
it might behave like a C++ template parameter -- generating specialized
code per type -- but it does not. Every snippet here runs the exact same
underlying Python bytecode no matter what type is involved; the
annotations exist purely for a static checker's benefit. You will watch
`__annotations__` as a plain dictionary, watch an `int`-annotated
parameter cheerfully hold a string with zero complaint, and watch the
mutable-default-argument trap happen live, two calls sharing one
growing list.

## Concepts covered

- `__annotations__`: annotations stored as ordinary, inspectable data on
  a function object, with no runtime effect of their own
- An annotated parameter accepting a mismatched value with no coercion,
  no error, and no special behavior -- annotations are not runtime checks
- A `TypeVar`-generic function's actual runtime behavior versus what a
  static checker concludes about its types
- `isinstance` against a Python 3.10+ union written with `|`
- `get_type_hints`, which resolves a string-form annotation into the
  real type object it names
- The mutable-default-argument trap, observed directly through object
  identity (`is`)

## How it works

The launcher runs seven short Python programs on your own interpreter
and shows you each one's source code. Predict exactly what it prints
(entering each line separately when the output has more than one line),
then type your prediction. A correct guess shows a short explanation and
moves you on; a wrong guess shows the actual output and, for many wrong
answers, an explanation of the specific misconception behind that guess.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly predicted the output of all seven snippets and the
launcher shows you a passphrase.

## Hints

<details>
<summary>Hint 1 -- ask "does the interpreter ever read this annotation?"</summary>

For almost every snippet here, the answer is no. `__annotations__` is
just a dict sitting on the function object; nothing in Python's own
call machinery consults it while the function actually runs.

</details>

<details>
<summary>Hint 2 -- TypeVar changes zero bytecode</summary>

Delete every annotation and every `TypeVar` from a generic function, and
it computes exactly the same results. TypeVar's entire job is to give a
static checker something to reason about -- it has no runtime footprint.

</details>

<details>
<summary>Hint 3 -- `is` checks identity, not just equal contents</summary>

For the mutable-default snippet, remember that two lists can look
identical when printed while still being two different objects -- `is`
is the only way to tell whether they are actually the SAME object.

</details>

## Going further

- Write a function with a `TypeVar` bounded to a specific set of types
  (`TypeVar("T", int, float)`) and use `get_type_hints` to inspect it.
  Does the bound show up anywhere in the resolved dict?
- Time `identity(42)` versus a version of `identity` with no annotations
  at all, over a few million calls. Do the annotations cost anything at
  runtime? What does that tell you about where a static checker's work
  actually happens?
- Predict, then verify, what happens if you build the mutable default
  list INSIDE the function body using the `None`-default idiom, and call
  the fixed function the same way this activity's trap snippet does.
