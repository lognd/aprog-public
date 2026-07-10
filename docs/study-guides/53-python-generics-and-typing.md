# Study Guide 53: Python Generics & Typing

This module reads and chooses Python type annotations (generic
containers, `Optional`/`|None`, `Callable[[...], R]`, `TypeVar` vs.
`@overload`) and then proves by running code that none of it has any
runtime effect -- annotations are inspectable data for a static checker,
never enforced by the interpreter.

## Know before you start

- `template<typename T>` as the C++ analogue for a `TypeVar` [assumed:
  row 23 -- Polymorphism]
- `const` as the C++ analogue for the enforcement contrast [assumed: row
  13 -- Const]
- Type annotations existing as unenforced documentation [assumed: row 52
  -- Python Types & Comprehensions]
- Mutable default arguments requiring the general mutable-vs-immutable
  distinction [assumed: row 47 -- Python Data Types]

## Taught here

Concept: reading and choosing annotations
- Know generic container annotations: `list[int]`, `dict[str, int]`,
  `tuple[int, ...]` (variable-length homogeneous tuple), and nested forms
  like `list[list[int]]`.
- Know `Optional[X]` (or its Python 3.10+ equivalent, `X | None`) marks a
  value that may be `X` or may be `None`.
- Be able to read a `Callable[[ParamTypes], ReturnType]` signature
  describing a function value's parameter and return types.
- Know `TypeVar` is Python's closest analogue to a C++ function template
  parameter: a single `TypeVar` used in both a parameter and a return
  type expresses one relationship holding for every possible type at
  once.
- Know `@overload` is closer to C++ overloading: it requires one
  hand-written signature per case, and any case not written gets no
  static-checking benefit.
- Know `Any` is a deliberate, honest tradeoff (opts a value out of static
  checking entirely), not a free win.
- Know a static type checker (`ty`, `mypy`) reports a mismatched call as
  a SEPARATE analysis pass over the source, entirely apart from actually
  running the code.

Concept: annotations have zero runtime effect
- Know `__annotations__` is an ordinary, inspectable dictionary stored on
  a function object -- data that exists, but that nothing in Python's own
  call machinery ever consults while the function actually runs.
- Know an annotated parameter cheerfully accepts a mismatched value (e.g.
  a string where `int` was annotated) with no coercion, no error, and no
  special behavior at call time.
- Know deleting every annotation and every `TypeVar` from a generic
  function changes zero bytecode and produces exactly the same results --
  `TypeVar`'s entire job is to give a static checker something to reason
  about.
- Know `get_type_hints` resolves a string-form annotation into the real
  type object it names, still purely for inspection, never for
  enforcement.
- Be able to use `isinstance` against a Python 3.10+ union written with
  `|`.

Concept: the mutable-default-argument trap
- Know `def f(xs: list[int] = []):` builds that empty list object exactly
  ONCE, at the moment `f` is DEFINED -- not fresh on every call that omits
  `xs` -- so every call sharing the default shares and mutates the SAME
  list object.
- Know `is` (not `==`) is the way to confirm two default-argument results
  from separate calls are literally the same object, since two lists can
  look identical when printed while still being different objects.
- Be able to fix the trap with the `xs: list[int] | None = None` idiom,
  building a fresh list inside the function body when `xs is None`.

## Study checklist

- [ ] Pick the correct annotation (list[int], dict[str,int], Optional/|
      None, Callable[[...],R]) for a described value.
- [ ] Explain the TypeVar-vs-overload distinction using the C++
      template-vs-overload analogy.
- [ ] Explain why an int-annotated parameter can hold a string at
      runtime with no error.
- [ ] Predict output of two calls sharing a mutable default argument.
- [ ] Fix a mutable-default trap using the None-default idiom.
- [ ] Explain what a static checker does that the interpreter does not.

## Practiced in

`annotation-arsenal`, `typevar-tracer`
