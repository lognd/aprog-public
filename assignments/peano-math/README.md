# Peano Math

## Overview

Mathematicians can build all of arithmetic from a single idea: every natural
number is either zero or "the successor of" some other number.  Addition is
just applying the successor repeatedly.  Multiplication is repeated addition.
Exponentiation is repeated multiplication.

In this assignment you will implement exactly that chain using only recursion.
No loops.  No built-in arithmetic operators except in one precisely designated
place.

## Learning goals

- Build complex operations (multiply, exponentiate) from simpler primitives (successor, add)
- Write a chain of recursive functions, where each function is defined in
  terms of the one below it (`exponentiate` calls `multiply`, `multiply`
  calls `add`, `add` calls `successor`) as well as recursively calling
  itself, rather than a single function doing all the work alone
- Understand how recursion replaces loops when iteration is forbidden
- Reason about base cases (the input small enough to answer directly, with
  no further recursive call) and recursive cases (every other input, handled
  by calling the function again on a smaller piece of the problem) for
  arithmetic functions

## Examples at a glance

To make all four functions concrete, here is **one** representative pair of
inputs, `a = 2` and `b = 3`, with what each function returns. Read this
table first -- it is the whole assignment in miniature.

| Call | Returns | Why |
|------|---------|-----|
| `successor(2)` | `3` | the successor of a number is just that number plus one |
| `add(2, 3)` | `5` | adding is applying `successor` to `2`, three times in a row (once per unit of `b`) |
| `multiply(2, 3)` | `6` | multiplying is adding `2` to itself, three times: `2 + 2 + 2 = 6` |
| `exponentiate(2, 3)` | `8` | raising to a power is multiplying `2` by itself, three times: `2 * 2 * 2 = 8` |
| `add(0, 5)` | `5` | adding zero changes nothing -- the edge case `add(0, x) == x` |
| `multiply(0, 5)` | `0` | multiplying by zero is always zero, no matter how large the other number is |
| `exponentiate(5, 0)` | `1` | any number to the power zero is `1` -- this is a base case, not something computed by repeated multiplication |

## Worked example: watch `add(2, 3)` run, step by step

This is the single most important thing to understand in the assignment, so
here is every recursive call spelled out. We are computing `add(2, 3)`,
which the reference implementation defines as: if `b == 0`, return `a`
directly (the base case); otherwise, return `add(successor(a), b - 1)` (the
recursive case) -- trade one unit off of `b` for one application of
`successor` on `a`, and try again with a smaller problem.

| Call | Is `b == 0`? | Action | Reason |
|------|--------------|--------|--------|
| `add(2, 3)` | no (`b = 3`) | calls `add(successor(2), 2)` = `add(3, 2)` | `b` is not yet zero, so trade one unit of `b` for one `successor` on `a` |
| `add(3, 2)` | no (`b = 2`) | calls `add(successor(3), 1)` = `add(4, 1)` | same rule -- `b` is still not zero |
| `add(4, 1)` | no (`b = 1`) | calls `add(successor(4), 0)` = `add(5, 0)` | same rule -- one unit of `b` still remains |
| `add(5, 0)` | **yes** (`b = 0`) | returns `a`, which is `5` | base case reached -- no more `successor` calls needed, `a` already holds the answer |

The recursion bottoms out at `add(5, 0)`, which returns `5` directly. That
`5` is then handed back up through every call that was waiting on it --
`add(4, 1)` returns `5`, `add(3, 2)` returns `5`, and finally the original
call `add(2, 3)` returns **`5`**. Notice that all the real work happened in
`successor`: three calls to it (turning `2` into `3`, `3` into `4`, and `4`
into `5`) is the entire mechanism behind "`2 + 3`". `multiply` and
`exponentiate` work the same way one level up: `multiply(a, b)` peels one
unit off `b` per call and hands off to `add`, and `exponentiate(base, exp)`
peels one unit off `exp` per call and hands off to `multiply` -- the same
"peel off one unit, recurse, then combine" shape all the way up the chain.

## Task

Implement the four functions declared in `peano.hpp` inside `peano.cpp`.

```cpp
// The one and only place a +1 increment may appear.
// Returns n + 1.
int successor(int n);

// Add a to b using only successor() and recursion.  No + operator.
int add(int a, int b);

// Multiply a by b using only add() and recursion.  No * operator.
int multiply(int a, int b);

// Raise base to the power exp using only multiply() and recursion.
// base^0 == 1 for all base.
int exponentiate(int base, int exp);
```

Each function's behavior, spelled out with concrete examples:

- `successor(n)` -- returns `n + 1`. This is the ONLY place the `+` operator
  is allowed to appear anywhere in the file.
  *Example:* `successor(0) == 1`; `successor(1) == 2`; `successor(9) == 10`.
- `add(a, b)` -- returns `a + b`, computed by calling `successor` on `a`
  exactly `b` times (see the worked example above for the full trace).
  *Example:* `add(2, 3) == 5`; `add(0, 5) == 5` (adding zero changes
  nothing); `add(5, 0) == 5` (the base case -- `b` is already zero, so `a`
  is returned immediately with no `successor` calls at all).
- `multiply(a, b)` -- returns `a * b`, computed by adding `a` to itself
  `b` times.
  *Example:* `multiply(2, 3) == 6`; `multiply(0, 5) == 0` (multiplying by
  zero is always zero, regardless of the other number); `multiply(1, 7)
  == 7` (multiplying by one is `add`ing `a` to zero exactly once).
- `exponentiate(base, exp)` -- returns `base` raised to the power `exp`,
  computed by multiplying `base` by itself `exp` times.
  *Example:* `exponentiate(2, 3) == 8`; `exponentiate(5, 0) == 1` (the
  base case -- ANY base raised to the power zero is `1`, including
  `exponentiate(0, 0) == 1`); `exponentiate(3, 1) == 3` (raising to the
  power one just multiplies `base` by the identity result of the
  zero-power base case).

### Contracts

A function's contract is the set of rules about what inputs it accepts and
what it promises to return. A precondition is the part of the contract that
lists what must be true about the inputs *before* the function is called --
here, that means the caller must not pass negative numbers. An edge case is
an input at the boundary of what a function normally handles (like zero, or
the smallest allowed value) -- exactly the kind of input where bugs like to hide.

| Function | Precondition | Edge case |
|---|---|---|
| `successor` | `n >= 0` | -- |
| `add` | `a >= 0`, `b >= 0` | `add(0, x) == x` |
| `multiply` | `a >= 0`, `b >= 0` | `multiply(0, x) == 0`, `multiply(1, x) == x` |
| `exponentiate` | `base >= 0`, `exp >= 0` | `exponentiate(x, 0) == 1` |

You do not need to handle negative inputs.

## Files

| File | Purpose |
|------|---------|
| `assets/peano.cpp` | Starter source -- submit this file with all four functions implemented |
| `assets/peano.hpp` | Provided; do not modify. Contains the function declarations |
| `visible-tests/test_catch.cpp` | Visible Catch2 test suite |
| `visible-tests/CMakeLists.txt` | Builds the visible test suite against your submission |

## Compilation and Testing

The visible tests use Catch2, a C++ testing framework that runs a set of
checks and reports which ones pass or fail; you do not need to understand
its internals for this assignment, only build and run it as shown below.
You will cover testing frameworks properly in a later topic.

Using the provided CMake setup (recommended -- this is what the grader uses):

```bash
cd visible-tests
mkdir build && cd build
cmake .. -DSUBMISSION_DIR=../assets
cmake --build .
./peano-math_tests
```

Note: `SUBMISSION_DIR` is resolved relative to `visible-tests/` (where
`CMakeLists.txt` lives), not relative to the `build/` directory you are
standing in when you run `cmake`. That is why the path above is `../assets`
(one level up from `visible-tests/`) rather than `../../assets`.

Or compile directly with g++, linking Catch2 yourself:

```bash
g++ -std=c++17 -Wall -Wextra -o peano_tests assets/peano.cpp visible-tests/test_catch.cpp -lCatch2Main -lCatch2
./peano_tests
```

## Constraints

- **No loops.** `for`, `while`, and `do` are forbidden in `peano.cpp`.
- **No `+` operator in `add`, `multiply`, or `exponentiate`.**
  The `+` operator (and `++`, `+=`) may only appear inside `successor`.
- **No `*`, `/`, `%` operators anywhere.**
- **No standard library arithmetic functions** (`std::pow`, `__builtin_popcount`, etc.) --
  this defeats the point of building arithmetic from `successor` yourself,
  even though it is not the kind of thing an automated scan can reliably catch.
- All four functions must be implemented recursively.

The no-loops rule and the operator rules above are enforced automatically by
the grader as two separate checks (10 points each; see Grading below).
Violating either check costs you those points regardless of whether your
tests otherwise pass -- it does not zero out any individual function's test
score.

## Grading

| Component                 | Points |
|----------------------------|--------|
| No loops check             | 10     |
| Operator constraints check | 10     |
| Compilation                | 0*     |
| Visible tests               | 35     |
| Hidden tests                 | 45     |
| **Total**                   | **100** |

\* Compilation must succeed before any test cases can be scored, but does not
itself carry points.

## Submission

Submit a single file named `peano.cpp`. Do not rename it.

## Going further

- Implement `subtract(a, b)` using only `successor` and recursion. What is the
  base case, and how do you handle the case where `b > a`?
- Read about Church numerals -- a representation of natural numbers as functions.
  How does it relate to what you implemented here?
- Add a `modulo(a, b)` function built from `subtract` and comparison. Can you
  then implement `is_prime` using only your Peano primitives?
