# Study Guide 43: Modern C++ (C++11-C++17 features)

This module names the small, targeted C++11/C++14/C++17 features that
replace older, riskier idioms with the same result and fewer footguns, and
then compiles/runs six programs that exercise the C++17 subset (structured
bindings, if-with-initializer, optional, string_view) directly.

## Know before you start

- Iterators and range-for's desugaring [assumed: row 35 -- Iterators]
- `auto`'s strip-then-requalify deduction rule [assumed: row 42 -- auto &
  Type Deduction]
- `std::array` vs. raw C-style arrays [assumed: row 32 -- Standard
  Containers p1]
- Scoped vs. unscoped enums [assumed: row 19 -- Structs (DOD & OOP intro)]
- Constructors, delegating construction, and `= default`/`= delete` on
  special member functions [assumed: row 21 -- OOP Implementation in
  C++; row 25 -- Dynamic Memory]

## Taught here

Concept: pre-C++11 idioms and their modern replacements
- Know `nullptr` is a real null-pointer type replacing `NULL`/`0`, which
  are just integer values that happen to work for null checks but can
  cause overload-resolution ambiguity a real null-pointer type avoids.
- Know range-based `for` replaces a manually written iterator loop
  (`for (auto it = v.begin(); ...)`), removing an entire class of
  fence-post and iterator-management bugs.
- Know `enum class` (scoped enum) requires qualifying every enumerator
  with its enum name and does not implicitly convert to `int`, unlike an
  old-style unscoped `enum`.
- Know `auto` replaces long, spelled-out iterator/container types.
- Know structured bindings (C++17) unpack a `std::pair` (or map element)
  directly into named variables instead of reaching through `.first`/
  `.second`.
- Know `using` alias-declarations replace `typedef` with clearer,
  left-to-right-readable syntax, and support templated aliases `typedef`
  cannot.
- Know uniform (brace) initialization `{}` avoids the "most vexing
  parse" -- a declaration that looks like it default-constructs an object
  but the compiler actually parses as a function declaration.
- Know delegating constructors let one constructor call another
  constructor of the same class in its initializer list, avoiding
  duplicated initialization logic.
- Know `= default` explicitly requests the compiler-generated version of
  a special member function; `= delete` explicitly forbids a function
  from being called/generated at all -- both are clearer than leaving a
  special member implicitly generated or omitted.

Concept: C++17 features in action
- Know structured bindings follow the exact same copy-vs-reference rule
  as plain `auto`: no `&` written means an independent copy of each
  unpacked piece, `&` means a real reference into the original object.
- Know `if` with an initializer statement (`if (init; condition)`) scopes
  the initialized variable tightly to the `if`/`else` -- it does not exist
  in any code after the whole `if` statement ends, even to a shadowing
  outer variable of the same name.
- Know `std::optional<T>` is a type-safe "maybe" value: `has_value()`
  checks presence, `value_or(fallback)` never throws and never reads
  garbage, returning either the real held value or exactly the fallback
  argument.
- Know `std::string_view` is a non-owning view over existing character
  data (no copy, no allocation) -- useful for read-only access, but it
  must not outlive the data it views.

## Study checklist

- [ ] Name the modern feature that replaces a given pre-C++11 snippet and
      explain the specific footgun it removes.
- [ ] Explain the "most vexing parse" and how brace initialization avoids
      it.
- [ ] Predict output for a structured binding declared with vs. without
      &.
- [ ] Explain if-with-initializer's scoping.
- [ ] Explain optional::value_or's contract (never throws, never garbage).
- [ ] State the ownership contract of std::string_view.

## Practiced in

`modernization-bureau`, `seventeen-tracer`
