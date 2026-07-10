# Study Guide 18: Programming Paradigms

This module teaches students to recognize the style -- the paradigm -- of a
piece of code independent of the language it is written in, and then to
articulate what each style actually buys or costs: mutation vs. immutable
values, order-dependence, referential transparency, and hidden state.

## Know before you start

- Imperative C++ basics: loops, accumulators, reassignment [assumed: row 6
  -- Control & Functions]
- A first look at classes with private state (informal exposure only; full
  OOP treatment comes in rows 20-21) [assumed: row 1 -- Ethics, via the
  VectorI class exercise]

## Taught here

Concept: the four paradigms
- Know that a programming paradigm is a style of structuring programs,
  defined by what the code treats as its basic building block.
- Know that imperative code is defined by mutation (variables reassigned,
  their stored value overwritten) plus sequencing (statement order matters
  completely), and that it maps closely onto what the CPU actually does.
- Know that object-oriented code is defined by bundling data with the
  operations allowed to touch it and hiding the data itself (a `private`
  field reachable only through methods), so mutation still happens but is
  controlled.
- Know that functional code is defined by pure functions plus composition:
  no mutation, new values built by feeding one transformation's output
  into the next (`map`, `filter`, `reduce`).
- Know that a pure function always returns the same output for the same
  input and changes nothing outside itself (no side effects), which makes
  it easy to test, safe to parallelize, and easy to reason about in
  isolation.
- Know that declarative code describes the desired result and leaves the
  procedure to an engine (SQL queries, Prolog facts and rules) -- the
  defining trait is "describe what, not how."
- Know that real languages mix paradigms: C++ supports imperative loops,
  object-oriented class design, and (since C++11) a functional style via
  lambdas and `<algorithm>`; even `std::sort(begin, end)` is declarative
  in spirit.
- Be able to classify a snippet by asking, in order: is a variable mutated
  in a sequence of steps? Is state bundled inside a class and guarded by
  methods? Are pure transformations composed? Or does the code only
  describe a result?

Concept: consequences of paradigm choice
- Know that immutability prevents aliasing bugs: when two names refer to
  the same changeable object, either can modify it out from under the
  other, and values that never change make this whole bug category
  impossible.
- Know that an imperative statement sequence is order-dependent (reorder
  two lines and the meaning changes), while a composed expression has no
  statement sequence to get wrong -- which matters for reading,
  refactoring, and parallelism.
- Know the term referential transparency: same input always yields the
  same output with no hidden state involved; an object with an
  accumulating internal counter cannot make this guarantee because its
  answer depends on its call history.
- Be able to check for mutation mechanically: look for reassignment (`=`
  on an existing name, `+=`, `++`/`--`) or methods that modify their
  object (`push_back`, setters); declaring and initializing a fresh
  variable once is not mutation.
- Know that encoding failure in the return value (e.g. `std::optional`,
  which holds either a value or nothing and forces the caller to check)
  is safer than a side channel like a global error flag the caller can
  forget to read.
- Know that no paradigm is simply "better": a single imperative loop can
  compute several statistics in one pass where a composed pipeline needs
  multiple passes, and in-place mutation is often the fastest option --
  each style buys specific guarantees and costs specific things.

## Study checklist

- [ ] Name the defining trait of each of the four paradigms in one phrase
      each.
- [ ] Given a snippet with `+=` inside a private-field class, explain why
      it is object-oriented rather than plain imperative.
- [ ] Distinguish functional from declarative code in one sentence.
- [ ] Define referential transparency and give the "call it twice" test
      for it.
- [ ] Give one concrete cost of the functional style and one concrete cost
      of the imperative style.

## Practiced in

`paradigm-lineup`, `paradigm-refactor-detector`
