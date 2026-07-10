# Study Guide 39: Function Pointers, Functors, Lambdas

This module introduces the three species of C++ callable -- function
pointer, functor, and lambda -- and lambda capture semantics in depth,
then has students generalize merge sort into a template that accepts any
of the three as a comparator.

## Know before you start

- Pointer syntax and declarations [assumed: row 11 -- Pointers]
- Operator overloading (`operator()` is just another overloadable
  operator) [assumed: row 21 -- OOP Implementation in C++]
- Templates as compile-time code generation [assumed: row 23 --
  Polymorphism]
- Merge sort and stability [assumed: row 38 -- Sorting]
- Dangling references/pointers to out-of-scope locals [assumed: row 11 --
  Pointers]

## Taught here

Concept: the three callable species
- Know a callable is anything invocable with `()`, the way a function is.
- Know a function pointer is a variable holding the address of a
  function, called through it -- `bool (*pred)(int)` declares `pred` as a
  pointer to a function `(int) -> bool`; the parentheses around `*pred`
  are required (`bool *pred(int)` declares something else entirely, a
  function returning `bool*`).
- Know a functor is a struct or class with an `operator()` member, so an
  object of that type can be called like a function -- and, unlike a bare
  function, can carry state across calls via its own member data.
- Know a lambda is an inline, unnamed callable written directly where it
  is needed, optionally with a capture list pulling variables in from the
  surrounding scope.
- Know the payoff: once behavior can be passed as a value (any of the
  three species), an algorithm like a sort can be written ONCE and reused
  with any comparison rule the caller supplies, instead of being
  rewritten per rule.

Concept: closures and capture semantics
- Know a closure is the concrete object a lambda expression builds at the
  exact point it is written, bundling the compiled body together with its
  captured variables.
- Know `[x]` captures by value: a frozen private copy taken at creation
  time, disconnected from the original afterward.
- Know `[&x]` captures by reference: a live link to the original,
  reflecting its current value including changes made after the lambda
  was created.
- Know `[=]` and `[&]` are default-capture markers, automatically
  capturing every variable the lambda body actually uses, by value or by
  reference respectively.
- Know a capture list is only for reaching out to variables already
  existing in the enclosing scope -- a lambda's own parameters are
  supplied fresh on every call and are not captures at all.
- Know `[y = x + 1]` is an init-capture: a brand-new captured variable,
  initialized once at creation time to whatever expression is written.
- Know `mutable` lifts the default restriction that a value-captured
  lambda's own copies are read-only, letting internal state change across
  repeated calls.
- Know the dangling reference-capture trap: capturing a local by
  reference in a lambda that outlives that local's scope is undefined
  behavior, for the same underlying reason a dangling pointer is.

Concept: generic algorithms over any callable
- Know a template `Compare` parameter does not require any particular
  named type -- only that `cmp(a, b)` compiles and returns something
  usable as `bool` (compile-time duck typing), letting a free function, a
  functor, and a lambda's closure all satisfy the same template with no
  shared base type.
- Know why a template comparator (not a function-pointer parameter) lets
  the compiler generate a specialized, fully inlined version per
  comparator type -- as fast as hand-writing the comparison in, unlike an
  opaque indirect call through a function pointer.
- Know the strict weak ordering contract a comparator must satisfy:
  consistent (`cmp(a,b)` and `cmp(b,a)` never both true), irreflexive
  (`cmp(a,a)` always false), and never true for elements considered
  equal (using `<=` instead of `<` breaks irreflexivity and can misorder
  or infinite-loop a sort).
- Know that when two elements tie under `cmp`, it is the SORT's job (not
  the comparator's) to preserve their original relative order -- exactly
  the stability requirement.

## Study checklist

- [ ] Read bool (*pred)(int) aloud correctly and explain the required
      parentheses.
- [ ] Predict output for capture-by-value vs. capture-by-reference
      lambdas after the captured variable changes.
- [ ] Distinguish a capture list entry from a lambda parameter.
- [ ] Explain the dangling-capture trap in terms already known from
      dangling pointers.
- [ ] State the three strict-weak-ordering rules a comparator must obey.
- [ ] Explain why a template comparator can outperform a function-pointer
      parameter.

## Practiced in

`callable-lineup`, `capture-court`, `sort-with-anything`
