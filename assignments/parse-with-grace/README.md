# Assignment: Parse With Grace

This assignment is the payoff for a whole course of sentinel-return and
bool/optional-return contracts. Up to now, when a function in this course
could fail, it reported that failure through its return value: a `bool`
success flag, a `std::optional`, a special value like `-1` or `NaN`. That
style works, but it has a real cost -- every caller has to remember to check
it, and nothing in the language forces them to. C++ has a second mechanism
for reporting failure: **exceptions**, written with `throw`, `try`, and
`catch`. This assignment asks you to build a small text-parsing library
using exceptions as the primary way of reporting bad input.

## Exceptions, from first principles

A `throw` statement does two things: it constructs an object (almost always
some subclass of `std::exception`), and it immediately abandons the rest of
the current function -- and every function that called it, and every
function that called *that* one -- until it finds a `catch` block whose
type matches the thrown object. This process of leaving scopes on the way
out is called **stack unwinding**: every local object still alive in each
abandoned scope has its destructor called automatically, in the exact
reverse of the order those objects were constructed.

This is why exceptions pair so well with **RAII** (Resource Acquisition Is
Initialization -- the pattern, which this course has used throughout with
smart pointers and containers, of tying a resource's lifetime to an
object's constructor/destructor). A `std::vector`, a `std::unique_ptr`, a
file handle wrapped in a small guard class -- all of these clean up
correctly during unwinding, with no manual "remember to clean up on every
possible failure path" code anywhere. You will build and test exactly this
guarantee yourself in this assignment, with `ScopedTally`.

`catch` should almost always take its parameter **by const reference**
(`catch (const std::exception& e)`), not by value. Catching by value copies
only the base-class portion of the real, thrown object -- known as
*slicing* -- which can silently discard information a derived exception
type added (including which override of a virtual function like `what()`
should run). A reference binds to the real, full object, whatever its
actual type turns out to be.

### The standard exception hierarchy, briefly

The `<stdexcept>` header (which you will use throughout this assignment)
defines a small hierarchy of exception types, all deriving from
`std::exception`. Two branches matter here:

- `std::logic_error` and its subclasses (`std::invalid_argument`,
  `std::domain_error`, `std::out_of_range`) cover conditions that are, in
  principle, avoidable by checking arguments beforehand -- bad input shapes,
  values outside a valid domain.
- `std::runtime_error` and its subclasses cover conditions that can really
  only be detected while the program runs.

Every exception type in `<stdexcept>` has a `.what()` member function
(inherited from `std::exception`) that returns a `const char*` describing
what went wrong. This assignment's tests check `what()` messages **exactly**
-- see the table below.

### When NOT to use exceptions

This course has used several failure-reporting styles, and none of them is
obsolete now that exceptions exist:

- A **routine, expected** failure that the *immediate* caller is already
  prepared to handle right there (a user mistyped a file path) often fits a
  `bool` or `std::optional` return better than an exception.
- A function on a **performance-critical hot path**, called an enormous
  number of times, may prefer an explicit precondition (documented, checked
  only via `assert()` in debug builds) over paying for exception-handling
  machinery on every call.
- A **destructor should never throw** -- if it does while a different
  exception is already unwinding the stack, the C++ runtime has no defined
  way to handle two exceptions at once, and calls `std::terminate()`,
  aborting the whole program immediately.

This assignment's functions are the other case: parsing untrusted string
input is exactly the kind of condition exceptions are good at reporting,
and a constructor establishing an object's invariants (like `Fraction`'s
denominator never being zero) has no return value to report failure with
at all -- throwing is its only real option.

## What you will implement

Everything lives in `parse_with_grace.hpp`. Do not use `std::stoi`,
`std::stol`, `std::strtol`, or `atoi` anywhere in this file -- you must
implement digit parsing yourself (this is checked automatically).

### `Fraction`

A tiny, complete struct already provided in the starter file:

```cpp
struct Fraction {
    long long numerator;
    long long denominator;
};
```

### `int parse_int(const std::string& s)`

Parses `s` as a base-10 integer. Leading/trailing ASCII spaces and tabs are
allowed and ignored; an optional leading `+` or `-` is allowed.

- Throws `std::invalid_argument` on a malformed string -- empty (or
  whitespace-only) input, a lone sign with no digits, or any non-digit
  character. Exact `what()` messages, with `s` as the input **after**
  trimming leading/trailing spaces and tabs (so `"  -  "` reports as `'-'`,
  not `'  -  '`):
  - Empty or whitespace-only input: `"parse_int: empty string"`
  - A lone `+`/`-` with no digits after it: `"parse_int: no digits found in '<s>'"`
  - Any other invalid character `c`: `"parse_int: invalid character '<c>' in '<s>'"`
- Throws `std::out_of_range` if the value does not fit in `int` (checked
  against `INT_MAX`/`INT_MIN`, from `<climits>`): `"parse_int: value out of int range in '<s>'"`

### `Fraction parse_fraction(const std::string& s)`

Parses `"a/b"` into a `Fraction`. `a` and `b` follow the same digit rules as
`parse_int` (each parsed as its own `long long`, not range-checked against
`int` -- only the final denominator-is-zero check applies).

- Throws `std::invalid_argument` if `s` is not exactly two integers
  separated by exactly one `/` (zero slashes, or more than one, both
  count): `"parse_fraction: expected exactly one '/' in '<s>'"`. A malformed
  numerator or denominator half also throws `std::invalid_argument`, with a
  message following the same shape as `parse_int`'s, but with `parse_fraction`
  in place of `parse_int`.
- Throws `std::domain_error` if the denominator parses to exactly zero:
  `"parse_fraction: denominator cannot be zero in '<s>'"`.

### `std::vector<int> parse_int_list(const std::string& s, char sep)`

Splits `s` on `sep`, parsing each piece with `parse_int`. Empty `s` returns
an empty vector. **Any exception `parse_int` throws for one element must
propagate out of `parse_int_list` completely unchanged** -- the exact same
exception type, and the exact same `what()` message `parse_int` itself
would have produced for that piece. Do not catch, wrap, or rewrap it.

### `int parse_int_or(const std::string& s, int fallback)`

Parses `s` with `parse_int`; if `parse_int` throws (either exception type),
catches it and returns `fallback` instead. **This is the one function in
this assignment required to use `try`/`catch` itself** -- every other
function in this file either throws directly or (in `parse_int_list`'s
case) deliberately lets an exception pass through untouched.

### `class ScopedTally`

An RAII counter. `ScopedTally(int& tally)` increments `tally` in its
constructor; its destructor decrements the same `tally`. This must work
correctly even when the destructor runs because an exception is unwinding
the stack through a `ScopedTally` -- that is precisely the guarantee this
class exists to demonstrate.

## Getting started

```bash
mkdir build && cd build
cmake .. -DSUBMISSION_DIR=<path-to-your-submission>
cmake --build .
./parse-with-grace_tests
```

## You will know you are done when...

All visible Catch2 tests pass locally, and your implementation matches
every `what()` message specified above exactly.

## Hints

- Write one shared helper that scans a run of digits and returns a
  `long long`, and call it from both `parse_int` and `parse_fraction` --
  you should not need to write the digit-scanning loop twice.
- Check for overflow *before* the multiply-and-add on each digit, not
  after -- once a `long long` has actually overflowed, the resulting value
  cannot be trusted to tell you it overflowed.
- `parse_int` range-checks against `int`'s range; the shared digit-parsing
  helper underneath it should use a wider range internally (`long long`) so
  it can represent "too big to fit in an `int`" as an ordinary value
  instead of overflowing itself first.

## Going further

- Extend `parse_fraction` to reduce the result to lowest terms (using a
  greatest-common-divisor helper), and decide: should a fraction like
  `"-3/-4"` (both signs negative) normalize to `"3/4"`? Write your own
  tests for the choice you make.
- Rewrite `parse_int_or` to accept a *predicate* -- a small callable that
  decides whether a caught exception is one it should recover from -- so a
  caller could choose to swallow `std::invalid_argument` but let
  `std::out_of_range` keep propagating.
