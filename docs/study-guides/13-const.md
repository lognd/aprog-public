# Study Guide 13: Const

This module treats `const` as a contract, not decoration: it distinguishes
`const`, `constexpr`, `consteval`, and `constinit`, then drills reading
compiler errors caused by broken const promises and propagating const
through an entire call chain until a small library is fully const-correct.

## Know before you start

- `const int*` vs `int* const` read right-to-left, and `const int&` as a
  read-only reference [assumed: row 11 -- Pointers]
- Pointer arithmetic and manual C-string manipulation [assumed: row 12 --
  C-Style Strings & Arrays]

## Taught here

Concept: the four const-family keywords
- Know that `const` marks a variable, parameter, or member function as
  read-only after initialization; its initializer may be a compile-time or
  a runtime value.
- Know that `constexpr` requires a value computable at compile time; for
  variables it always implies `const` (read-only), and a `constexpr`
  function may run at compile time or runtime depending on whether its
  arguments are compile-time constants.
- Know that `consteval` (C++20) declares an immediate function: every call
  must produce a compile-time constant, and passing a runtime value is a
  compile error.
- Know that `constinit` (C++20) requires a static/thread-duration variable
  to be initialized with a compile-time constant, but -- unlike `const` and
  `constexpr` -- does NOT make the variable read-only; it can still be
  assigned to later.
- Know that `constinit` exists to prevent the static initialization order
  fiasco (undefined initialization order between global variables in
  different translation units that depend on each other) by guaranteeing no
  dynamic initialization is needed.

Concept: const and pointers/references
- Know the right-to-left reading rule for pointer const: `const int* p`
  ("pointer to const int") lets you reassign `p` but not write `*p`; `int*
  const p` ("const pointer to int") lets you write `*p` but not reassign
  `p`; `const int* const p` locks both.
- Know that `const` on a function parameter is a binding promise to the
  caller about what the function will and will not do to the data behind
  that pointer or reference.
- Know that a `const` reference (`const T&`) is the idiomatic way to pass a
  large object into a function without copying it, while still promising
  read-only access.

Concept: propagating const correctly and diagnosing violations
- Be able to read a compiler error caused by a const mismatch (for example,
  passing `const char*` where `char*` is expected) and identify which
  promise was broken.
- Know that const-ness must be preserved through a function's return type:
  a function that returns a pointer into `const char*` input data must
  itself return `const char*`, or it would silently strip the caller's
  read-only guarantee.
- Know that fixing const on one function's signature can force a matching
  fix in that function's callers, because const propagates through the
  call chain -- this is intentional, not a quirk, since the contract must
  stay consistent end to end.
- Know that `const_cast` forcibly strips `const` from a pointer or
  reference so code can write through it anyway, and that using it to
  silence a compiler error defeats the purpose of the const contract rather
  than fixing the underlying type mismatch.
- Be able to design a small library's signatures so that read-only
  functions take `const char*`, write functions take `char*`, and "mixed"
  functions (like copy) take a `const char*` source alongside a `char*`
  destination.

## Study checklist

- [ ] Distinguish `const`, `constexpr`, `consteval`, and `constinit` in one
      sentence each.
- [ ] Given `const int* p` and `int* const p`, state what each allows and
      forbids.
- [ ] Explain why a function returning a pointer into `const char*` input
      must itself return `const char*`.
- [ ] Explain why fixing const on one function can force changes in its
      callers.
- [ ] Explain why using `const_cast` to silence an error is not a real fix.

## Practiced in

`const-maze`, `const-contract`, `const-refactor`, `const-qualifier-toolkit`
