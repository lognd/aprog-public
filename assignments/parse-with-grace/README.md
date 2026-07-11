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

## Examples at a glance

To make the whole assignment concrete, here is **one** scenario: a user typed
the raw text `"3,-7,x,999999999999"`, meaning to give a comma-separated list
of integers, plus a companion fraction string `"3/-7"` built from its first
two numbers. The table below shows what every function in this assignment
does with pieces of that same scenario. Read this table first -- it is the
whole assignment in miniature.

```
list input  = "3,-7,x,999999999999"
             (piece 0: "3", piece 1: "-7", piece 2: "x", piece 3: "999999999999")
frac input  = "3/-7"
```

| Call | Result | Why |
|------|--------|-----|
| `parse_int("3")` | `3` | an ordinary positive integer, no sign, no whitespace |
| `parse_int(" -7 ")` | `-7` | leading/trailing spaces are trimmed before parsing; the sign is kept |
| `parse_int("999999999999")` | throws `std::out_of_range`, `what() == "parse_int: value out of int range in '999999999999'"` | the digits fit in a `long long` just fine, but the resulting value is far bigger than `INT_MAX` |
| `parse_int("x")` | throws `std::invalid_argument`, `what() == "parse_int: invalid character 'x' in 'x'"` | `'x'` is neither a digit nor a leading sign |
| `parse_fraction("3/-7")` | `Fraction{3, -7}` | exactly one `/` splits the string into two valid integers |
| `parse_fraction("3/0")` | throws `std::domain_error`, `what() == "parse_fraction: denominator cannot be zero in '3/0'"` | a fraction can never have a zero denominator |
| `parse_int_list("3,-7,x,999999999999", ',')` | throws `std::invalid_argument`, `what() == "parse_int: invalid character 'x' in 'x'"` | piece 2 (`"x"`) fails inside `parse_int`, and that exact exception (same type, same message) propagates straight out -- `parse_int_list` never wraps or rewrites it |
| `parse_int_list("", ',')` | `{}` | an empty string is a valid, empty list -- there is nothing to split |
| `parse_int_or("3,-7,x,999999999999", -1)` | `-1` | the whole string is not a bare integer (the first comma is an invalid character), so `parse_int` throws and `parse_int_or` catches it and returns the fallback |
| `parse_int_or("3", -1)` | `3` | parsing succeeds, so the fallback is never used |
| `ScopedTally` around a normal scope | tally goes `0 -> 1 -> 0` | constructor increments on entry, destructor decrements on the normal way out |
| `ScopedTally` around a scope that throws | tally still goes `0 -> 1 -> 0` | the destructor runs during stack unwinding too -- this is the whole point of RAII |

## Worked example: watch `parse_int_list` hit a deliberate error, step by step

This is the single most important thing to understand in the assignment, so
here is every step spelled out. We call
`parse_int_list("3,-7,x,999999999999", ',')`, splitting on `,` and parsing
each piece with `parse_int` in order, left to right.

| Step | Piece | `parse_int(piece)` | Outcome | Why |
|------|-------|---------------------|---------|-----|
| 1 | `"3"` | `3` | pushed onto the result vector -> `{3}` | ordinary positive integer |
| 2 | `"-7"` | `-7` | pushed onto the result vector -> `{3, -7}` | leading `-` is a valid sign, `7` is a valid digit run |
| 3 | `"x"` | throws `std::invalid_argument("parse_int: invalid character 'x' in 'x'")` | `parse_int_list` does **not** catch this -- it propagates immediately | `'x'` is not a digit and not a leading sign, so `parse_int` cannot parse it at all |
| -- | `"999999999999"` | never reached | -- | the exception from piece 2 (index 2) already unwound out of the function; the loop never gets to the fourth piece |

The final observable result of `parse_int_list("3,-7,x,999999999999", ',')` is:
no vector is ever returned. The caller sees a `std::invalid_argument` exception
whose `what()` is exactly `"parse_int: invalid character 'x' in 'x'"` -- the
identical message `parse_int("x")` would have produced on its own, byte for
byte. This is the "propagates unchanged" contract: `parse_int_list` is not
allowed to catch this error, add context to it, wrap it in a different
exception type, or swallow it -- it must let it pass through exactly as
`parse_int` raised it. Notice also that the partial work already done (the
`3` and `-7` already parsed) is simply discarded along with the abandoned
`std::vector<int>` local -- nothing about that is a bug: the function has no
well-defined partial answer to return once one piece has failed.

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
  against `INT_MAX`/`INT_MIN`, from `<climits>`): `"parse_int: value out of
  int range in '<s>'"`, with `<s>` here as the **original, untrimmed**
  argument (unlike the `invalid_argument` messages above, this one does not
  strip leading/trailing spaces and tabs before reporting `s`).

- **Example (basic parse):** `parse_int("42") == 42`.
- **Example (trimming):** `parse_int(" -17 ") == -17` -- **spaces and tabs
  are trimmed before parsing**.
- **Error case (empty string):** `parse_int("")` throws
  `std::invalid_argument` with **`what() == "parse_int: empty string"`**.
- **Edge case (whitespace-only):** `parse_int("   ")` throws the same --
  **whitespace-only counts as empty**.
- **Error case (lone sign):** `parse_int("+")` throws
  `std::invalid_argument` with
  **`what() == "parse_int: no digits found in '+'"`**.
- **Error case (invalid character):** `parse_int("12a")` throws
  `std::invalid_argument` with
  **`what() == "parse_int: invalid character 'a' in '12a'"`**.
- **Error case (out of range):** `parse_int("  -2147483649  ")` throws
  `std::out_of_range` with
  **`what() == "parse_int: value out of int range in '  -2147483649  '"`**
  (note the **untrimmed original string** appears in this particular
  message, unlike the `invalid_argument` cases above).

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

- **Example (basic parse):** `parse_fraction("3/4") == Fraction{3, 4}`.
- **Example (both signs negative):** `parse_fraction("-3/-4") ==
  Fraction{-3, -4}` -- **no reduction to lowest terms** is required or
  performed.
- **Error case (no slash):** `parse_fraction("34")` throws
  `std::invalid_argument` with
  **`what() == "parse_fraction: expected exactly one '/' in '34'"`**.
- **Error case (too many slashes):** `parse_fraction("1/2/3")` throws the
  same kind, with
  **`what() == "parse_fraction: expected exactly one '/' in '1/2/3'"`**.
- **Error case (malformed numerator):** `parse_fraction("a/4")` throws
  `std::invalid_argument` with
  **`what() == "parse_fraction: invalid character 'a' in 'a'"`** (same shape
  as `parse_int`'s message, but naming `parse_fraction`).
- **Error case (zero denominator):** `parse_fraction("3/0")` throws
  `std::domain_error` with
  **`what() == "parse_fraction: denominator cannot be zero in '3/0'"`**.

### `std::vector<int> parse_int_list(const std::string& s, char sep)`

Splits `s` on `sep`, parsing each piece with `parse_int`. Empty `s` returns
an empty vector. **Any exception `parse_int` throws for one element must
propagate out of `parse_int_list` completely unchanged** -- the exact same
exception type, and the exact same `what()` message `parse_int` itself
would have produced for that piece. Do not catch, wrap, or rewrap it.

- **Example (basic split):** `parse_int_list("1,2,3", ',') ==
  std::vector<int>{1, 2, 3}`.
- **Empty-input case:** `parse_int_list("", ',') == std::vector<int>{}` --
  **empty string, empty list, not an error**.
- **Edge case (no separator found):** `parse_int_list("5", ',') ==
  std::vector<int>{5}` -- no separator found means **one single piece**.
- **Error case (propagated unchanged):** `parse_int_list("1,x,3", ',')`
  throws `std::invalid_argument` with
  **`what() == "parse_int: invalid character 'x' in 'x'"`** (note the
  message says `parse_int`, not `parse_int_list` -- it is the **unmodified
  exception** `parse_int("x")` itself would have thrown).
- **Error case (empty middle piece):** `parse_int_list("1,,3", ',')` throws
  `std::invalid_argument` with **`what() == "parse_int: empty string"`** --
  the middle piece, between two commas, is empty.

### `int parse_int_or(const std::string& s, int fallback)`

Parses `s` with `parse_int`; if `parse_int` throws (either exception type),
catches it and returns `fallback` instead. **This is the one function in
this assignment required to use `try`/`catch` itself** -- every other
function in this file either throws directly or (in `parse_int_list`'s
case) deliberately lets an exception pass through untouched.

- **Example (success, fallback unused):** `parse_int_or("5", -1) == 5`.
- **Example (malformed input):** `parse_int_or("bad", -1) == -1` --
  `std::invalid_argument` is **caught and swallowed**.
- **Edge case (out of range):** `parse_int_or("99999999999999", -1) == -1`
  -- valid digits but out of `int` range; **`std::out_of_range` is also
  caught**, since `parse_int_or` catches both exception types.
- **Empty-input case:** `parse_int_or("", 0) == 0` -- **empty string is
  malformed too**.

### `class ScopedTally`

An RAII counter. `ScopedTally(int& tally)` increments `tally` in its
constructor; its destructor decrements the same `tally`. This must work
correctly even when the destructor runs because an exception is unwinding
the stack through a `ScopedTally` -- that is precisely the guarantee this
class exists to demonstrate.

- **Example (normal scope exit):** constructing `ScopedTally t(tally)` when
  `tally == 0` leaves **`tally == 1`**; letting `t` go out of scope normally
  afterward brings it back to **`tally == 0`**.
- **Tricky case (unwinding through a throw):** constructing
  `ScopedTally t(tally)` and then `throw`-ing past it (so its destructor
  runs during unwinding, not because the enclosing block ended normally)
  still brings `tally` back down by exactly one: `tally == 0` before,
  `tally == 1` while `t` is alive and the exception is in flight, then
  **`tally == 0` again** once the exception has been caught further up the
  stack.

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
