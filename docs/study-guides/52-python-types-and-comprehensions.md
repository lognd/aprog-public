# Study Guide 52: Python Types & Comprehensions

This module shows that a comprehension is exactly a compact rewrite of a
loop-and-collect pattern (list/dict/set/generator, filtering vs.
transforming, nesting, scoping), and that Python variables have no
declared type at all: `type()`/`isinstance()` semantics, `bool` as a
genuine `int` subclass, and why annotations are never enforced at
runtime.

## Know before you start

- Loop mechanics and `for` syntax [assumed: row 6 -- Control & Functions]
- list/dict/set choice reasoning [assumed: row 48 -- Python Data
  Structures]
- Lazy iteration and pipeline-style consumption as background for
  generator expressions [assumed: row 39 -- Function Pointers, Functors,
  Lambdas (callables passed around), and Python's own lack-of-static-
  typing groundwork from row 45]
- `isinstance`/duck typing distinction groundwork [assumed: row 46 --
  Python Syntax (including OOP)]

## Taught here

Concept: comprehensions as loop rewrites
- Know a list comprehension is exactly equivalent to an explicit `for`
  loop plus `.append()` -- any comprehension can be unfolded into that
  loop form to check its output.
- Know an `if` written AFTER the `for` clause is a FILTER (it can drop
  elements entirely); an `if`/`else` written BEFORE the `for` clause is a
  transforming EXPRESSION (it keeps every element, choosing a value for
  each) -- position, not the word "if," decides which one it is.
- Know dict comprehensions (`{key: value for ...}`) and set comprehensions
  (`{value for ...}`, with automatic deduplication) follow the same
  loop-and-collect equivalence.
- Know a nested comprehension with two `for` clauses reads left to right
  like nested loops -- the first `for` clause is the outermost loop --
  used for flattening a 2D structure.
- Know generator expressions (`(...)` instead of `[...]`) are lazy: they
  evaluate one value at a time on demand and never materialize a full
  list in memory.
- Know a comprehension's loop variable is private to the comprehension
  and does not leak into the surrounding code, unlike a plain `for`
  loop's variable, which remains visible afterward (Python's no-block-
  scope rule from row 45 has this one exception).
- Be able to use `zip()` inside a comprehension to walk two sequences
  together.

Concept: dynamic typing, type(), and isinstance()
- Know Python variables have no declared type at all -- `type(x)` always
  reports whatever `x` currently, actually is, and that can change from
  one assignment to the next.
- Know `/` always produces a `float` in Python 3 even on two `int`
  operands, while `//` does not.
- Know `isinstance(x, (A, B))` checked against a tuple of types matches
  if `x` is an instance of ANY one of them.
- Know `bool` is a genuine subclass of `int`, not merely convertible to
  one -- `isinstance(True, int)` is `True` by real inheritance, which is
  exactly why arithmetic like `True + True` works at all.
- Know `type(x) is SomeClass` is a strict, exact-match comparison against
  a single class (ignores inheritance); `isinstance(x, SomeClass)` walks
  `x`'s entire inheritance chain -- they diverge the moment a subclass is
  involved.
- Know duck typing ("does it support the method I need?") is the
  idiomatic Python default over an explicit `isinstance` check for many
  jobs, though `isinstance` is still the right tool when the exact type
  genuinely matters.

Concept: type annotations are unenforced documentation
- Know a type annotation (`def f(x: int) -> int:`) is never checked or
  enforced by Python's own interpreter while a program runs -- the
  interpreter runs the code exactly as written regardless of what the
  annotation claims.
- Know annotations are documentation, checked (if at all) by a separate
  STATIC analysis tool (like `ty` or `mypy`) that reads the source code
  before the program ever executes, never by running it.

## Study checklist

- [ ] Unfold a given comprehension into its equivalent explicit for loop.
- [ ] Distinguish a filtering if from a transforming if/else expression
      by position alone.
- [ ] Predict output of a nested comprehension flattening a 2D grid.
- [ ] Explain why a generator expression never builds a full list.
- [ ] Explain why isinstance(True, int) is True.
- [ ] Explain why a mistyped annotation does not raise at runtime, and
      what tool would catch it instead.
- [ ] Distinguish type(x) is C from isinstance(x, C) with a subclass
      example.

## Practiced in

`comprehension-decathlon`, `type-inspector`
