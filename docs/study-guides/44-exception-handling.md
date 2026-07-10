# Study Guide 44: Exception Handling

This module introduces `throw`/`try`/`catch` mechanics and stack unwinding
by tracing instrumented construction/destruction output, builds the
judgment for when an exception is the right tool versus a return-value
style, and has students build a parsing library reporting failure
primarily through exceptions with exact `what()` message contracts.

## Know before you start

- Constructors/destructors and construction/destruction order [assumed:
  row 21 -- OOP Implementation in C++]
- RAII tying a resource's lifetime to an object's constructor/destructor
  [assumed: row 21 -- OOP Implementation in C++]
- Virtual dispatch and slicing (catch by reference vs. by value) [assumed:
  row 22 -- Inheritance]
- Class hierarchies and derived-to-base matching [assumed: row 22 --
  Inheritance]
- `std::optional`/sentinel-value return styles used before exceptions were
  introduced [assumed: row 43 -- Modern C++]

## Taught here

Concept: throw/try/catch mechanics and stack unwinding
- Know `throw` constructs an exception object (almost always a subclass
  of `std::exception`) and immediately abandons the rest of the current
  `try` block and every calling function's frame until a matching `catch`
  is found.
- Know stack unwinding is the process of leaving those scopes on the way
  out: every local object still alive in each abandoned scope has its
  destructor called automatically, in the EXACT REVERSE of construction
  order, even across multiple function frames.
- Know catch-clause type matching is tried in source order, first match
  wins, and a clause never intercepts a thrown type unless that type IS
  the clause's type or is derived from it -- a near-miss clause (e.g.
  catching `std::logic_error` when a `std::runtime_error` was thrown)
  provides no protection.
- Know `catch (const Type& e)` (by const reference) preserves the real,
  un-sliced object and its virtual overrides; `catch (Type e)` (by value)
  slices a derived exception down to exactly its base-class portion,
  including which override of `what()` runs.
- Know a bare `throw;` inside a catch block rethrows the current exception
  unchanged, preserving its original type.
- Know why RAII cleanup during unwinding is reliable: `std::vector`,
  `std::unique_ptr`, and any resource-owning guard class clean up
  automatically with no manual "remember to clean up on every failure
  path" code, because their destructors run as part of unwinding.

Concept: judgment -- when to throw and when not to
- Know a routine, EXPECTED failure that the immediate caller is already
  prepared to handle right there often fits a `bool`/`std::optional`
  return better than an exception.
- Know a constructor that cannot establish its class's invariants has no
  return value to report failure with at all -- throwing is its only real
  option.
- Know a destructor must never throw: if it does while a different
  exception is already unwinding the stack, the C++ runtime has no
  defined way to handle two exceptions at once and calls
  `std::terminate()`, aborting the whole program immediately.
- Know a performance-critical hot path called an enormous number of times
  may prefer an explicit documented precondition, checked only via
  `assert()` in debug builds, over paying for exception-handling machinery
  on every call.
- Know `catch (...) { }` (an empty catch-all) is an anti-pattern -- it
  silently discards the failure with no diagnostic and no recovery.
- Know `noexcept` is a promise to the compiler that a function will not
  throw, which the compiler is allowed to optimize around; violating it
  calls `std::terminate()`.
- Know the basic exception-safety guarantee: an object's invariants
  survive an exception, but the exact resulting value is not promised
  (stronger guarantees exist but are not required by default).

Concept: `<stdexcept>` and building an exceptions-first library
- Know `std::logic_error` and its subclasses (`std::invalid_argument`,
  `std::domain_error`, `std::out_of_range`) cover conditions that are, in
  principle, avoidable by checking arguments beforehand; `std::runtime_error`
  and its subclasses cover conditions only detectable while running.
- Know every `<stdexcept>` type has `.what()` (inherited from
  `std::exception`) returning a `const char*` description, and that exact
  `what()` message strings are part of a function's contract, not an
  implementation detail.
- Be able to let an exception propagate out of a wrapper function
  completely unchanged (same type, same `what()`) by simply not catching
  it, versus deliberately catching and converting one to a fallback
  return value (`parse_int_or`'s one required `try`/`catch`).
- Be able to build an RAII counter (`ScopedTally`) whose destructor
  decrements a counter correctly even when invoked by stack unwinding
  during an in-flight exception.

## Study checklist

- [ ] Predict the exact construct/destruct/print order of an instrumented
      throw/catch program.
- [ ] Explain why catch (const Type&) is preferred over catch (Type).
- [ ] Explain why a destructor must never throw and what happens if it
      does.
- [ ] For a scenario, decide exception vs. return-value vs. assert() and
      justify it.
- [ ] Explain std::logic_error vs. std::runtime_error's branches.
- [ ] Write a function that lets an exception propagate unmodified versus
      one that catches and converts it to a fallback value.

## Practiced in

`unwind-tracer`, `throw-or-not-court`, `parse-with-grace`
