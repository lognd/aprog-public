# Study Guide 23: Polymorphism (Interfaces, Templating)

This module contrasts C++'s two ways of writing one piece of code that
works with many types: runtime polymorphism through a virtual interface and
the vtable, and compile-time polymorphism through templates and duck
typing. The text-filters assignment implements the same four filters both
ways so the trade-offs are experienced, not just read about.

## Know before you start

- Static vs. dynamic type, virtual dispatch, and the vtable [assumed:
  row 22 -- Inheritance]
- Abstract base classes and pure virtual functions [assumed: row 22 --
  Inheritance]
- Object slicing on by-value copies [assumed: row 22 -- Inheritance]
- `std::string` manipulation (scanning, replacing, case conversion)
  [assumed: row 7 -- Standard Library Types]

## Taught here

Concept: when a call is bound
- Know that every function call must resolve to actual code, and the
  resolution happens either at compile time (static dispatch: the compiler
  picks the target by reading source) or at run time (dynamic dispatch:
  the target is picked by inspecting the real object).
- Know that only `virtual` functions called through a reference or pointer
  use dynamic dispatch; without `virtual`, the call is resolved purely by
  static type with no vtable involvement.
- Know the classic gotcha: default arguments on virtual functions are bound
  statically (from the static type's declaration), even when the function
  body itself dispatches dynamically -- so a derived override can run with
  the base's default argument.
- Know that overload resolution is always a compile-time mechanism,
  separate from virtual dispatch.
- Know that slicing (copying a derived object by value into a base-typed
  slot) happens regardless of whether any function involved is virtual,
  and a sliced object dispatches as a pure base object.

Concept: interfaces vs. duck typing
- Know that the interface approach uses an abstract base class with pure
  virtual functions; code written against `const TextFilter&` works with
  any derived class, resolved per call through the vtable at run time.
- Know that duck typing via a function template requires no shared base
  class at all: the template only requires that the expressions in its
  body (e.g. `f.apply(s)`) compile for the actual type substituted in --
  "if it walks like a filter and quacks like a filter, it's a filter."
- Know that template instantiation means the compiler generates a
  separate, concrete copy of the function for each distinct type it is
  called with, entirely at compile time.
- Be able to answer "does this compile?" for a template by mentally
  substituting the concrete type into the body and reading it as
  hand-written code; and for an interface by checking whether the actual
  inheritance relationship exists (a matching method name alone is not
  enough).
- Know the trade-off table: the interface approach supports heterogeneous
  storage (one container holding mixed concrete types through base
  pointers) and does not require recompilation for new types, but costs
  one vtable indirection per call and forces every type to inherit; the
  template approach has zero per-call dispatch cost and needs no
  inheritance, but generates one function copy per type, cannot directly
  store mixed types in one container, and reports type errors only at
  instantiation time.

Concept: implementing the same behavior both ways
- Be able to implement a pure-virtual interface (virtual destructor plus
  `virtual ... = 0` methods) and several classes overriding it with
  `const override`.
- Be able to write function templates over a placeholder type `F` that
  apply a filter, chain several filters, or test a property -- never
  naming the interface type.
- Be able to implement string filters precisely: uppercase alphabetic
  characters only; trim leading/trailing whitespace by `std::isspace`;
  replace every non-overlapping occurrence of a stored word with
  same-length asterisks scanning left to right (empty word returns input
  unchanged); collapse runs of two or more spaces into one, leaving tabs
  and newlines alone.

## Study checklist

- [ ] For a given snippet, state whether each call is resolved at compile
      time or run time, and why.
- [ ] Explain the default-argument-on-virtual gotcha.
- [ ] Explain why a template needs no base class but an interface does.
- [ ] State which approach allows one container of mixed concrete types
      and which avoids per-call indirection.
- [ ] Given a type with a matching method but no inheritance, say which of
      the two `run` versions accepts it.

## Practiced in

`dispatch-detective`, `duck-or-vtable`, `text-filters`
