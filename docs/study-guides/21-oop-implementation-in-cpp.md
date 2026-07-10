# Study Guide 21: OOP Implementation in C++

This module moves from OOP vocabulary to C++ mechanics: exactly when
constructors and destructors run, what a well-encapsulated class looks like
in code, how a class enforces an invariant across its whole interface
(Fraction), and how RAII ties a resource's cleanup to an object's lifetime
(FileGuard).

## Know before you start

- The five pillars vocabulary, especially encapsulation and invariants
  [assumed: row 20 -- OOP Vocab & Theory]
- `const` member functions and `const T&` parameters [assumed: row 13 --
  Const]
- POSIX `open`/`close`, the fd table, and the partial-write loop [assumed:
  row 15 -- Basic OS Theory]
- The Euclidean GCD algorithm [assumed: row 6 -- Control & Functions]
- Scope and stack-frame lifetime rules [assumed: row 10 -- Memory Model]

## Taught here

Concept: object lifetime
- Know that a constructor is a special function that runs automatically the
  moment an object is created (to set up initial state), and a destructor
  (`~ClassName`) runs automatically the moment its lifetime ends (to clean
  up).
- Know that a local variable's destructor runs when execution reaches the
  closing brace of the scope it was declared in -- whether that brace
  belongs to a function, an `if`, a loop body, or a bare `{ }` block.
- Know that objects declared in the same scope are constructed in
  declaration order and destroyed in exactly the reverse order, so anything
  a later object might depend on is still alive while it is being cleaned
  up.
- Know that a class's member objects are constructed before the containing
  class's own constructor body runs, and destroyed after its destructor
  body runs, in declaration order (and reverse for destruction).
- Know that a temporary is an unnamed object (e.g. `A()` written inline as
  an argument) whose lifetime ends at the end of the full expression -- the
  statement up to the semicolon -- not at the end of the function it was
  passed into.
- Know that an early `return` still runs the destructors of every local
  already constructed in the scopes being exited -- the guarantee that
  makes RAII possible.

Concept: encapsulation done right (and its failure modes)
- Know that an invariant is a rule about an object's internal state that
  must always hold (e.g. "denominator is always positive"), and that
  private fields alone do not enforce invariants -- a setter that accepts
  any value without validating still lets the object reach an invalid
  state.
- Know the "leaky getter" trap: returning a non-const reference to a
  private field hands outside code a live alias to the actual data,
  bypassing every validation the class performs; returning a copy or a
  `const` reference closes the hole.
- Know that a member function that does not modify the object must be
  marked `const` -- otherwise it cannot be called through a `const Type&`
  or `const Type*`, breaking otherwise-correct read-only call sites.
- Be able to audit a small class and classify it as: public data with no
  invariant enforcement, missing const, leaky getter, or nothing wrong --
  recognizing a correctly encapsulated class is as important as spotting a
  broken one.

Concept: invariant-preserving class design (Fraction)
- Know that a class is "a promise about what state is reachable": every
  instance, from every constructor and every operation, satisfies the
  invariants.
- Be able to establish invariants once, in the constructor (reduce by the
  GCD; flip both signs if the denominator came in negative so sign lives
  in the numerator; normalize zero to 0/1), so every other method can
  simply trust them without re-checking.
- Know the pattern of arithmetic methods that never mutate `*this` but
  construct and return a brand-new object, re-establishing invariants for
  the result through the same constructor.
- Know why unreduced storage breaks equality (1/2 vs 2/4 comparing unequal)
  and why an unnormalized sign breaks every sign check -- invariants exist
  so callers never have to remember these rules themselves.
- Know that a precondition (e.g. "denominator is nonzero") is part of the
  function's contract that the caller must guarantee; violating it makes
  behavior unspecified rather than something the class must handle.

Concept: RAII (Resource Acquisition Is Initialization)
- Know that RAII binds a resource's lifetime to an object's lifetime: the
  constructor acquires (e.g. calls `::open()`), the destructor releases
  (e.g. calls `::close()`), and no other code manages the resource's
  existence.
- Know that the destructor is the only code guaranteed to run on every exit
  path out of a scope -- normal end, early `return`, `break`, or exception
  unwinding -- which is exactly why manual `close()` before every return is
  a bug factory and RAII is not.
- Know that the process fd table is finite, that leaked fds are reclaimed
  only at process exit, and that a long-running program leaking one fd per
  loop iteration eventually makes every `open()` in the process fail.
- Know the double-close hazard: if two objects both believe they own the
  same fd, the second destructor closes an fd number the OS may have
  already reassigned to unrelated code -- closing someone else's file.
- Know that deleting the copy constructor and copy assignment (`= delete`)
  turns the double-close hazard into a compile error, which is why an
  owning type like FileGuard is always passed by reference, never by
  value.
- Know that an explicit `close()` method must be idempotent (safe to call
  repeatedly): the destructor must detect an already-closed fd and do
  nothing rather than close a reused fd number.
- Know that `std::fstream` is itself an RAII wrapper over a file, and that
  the same acquire-in-constructor/release-in-destructor shape manages heap
  memory, locks, and sockets.

## Study checklist

- [ ] Predict the construction/destruction print order for two locals, a
      member object, and a temporary in one program.
- [ ] Explain why destruction order is the reverse of construction order.
- [ ] Diagnose a class with a getter returning `std::vector<T>&` -- what is
      wrong and what are the two fixes?
- [ ] List Fraction's three invariants and where each is established.
- [ ] Explain why FileGuard deletes its copy operations, in terms of the
      double-close hazard.
- [ ] Explain why an early return does not leak the fd when a FileGuard is
      in scope.

## Practiced in

`ctor-dtor-tracer`, `encapsulation-audit`, `fraction-arithmetic`, `raii-file-guard`
