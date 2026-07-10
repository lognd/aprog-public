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
- Write mutually recursive functions that call each other through a defined interface
- Understand how recursion replaces loops when iteration is forbidden
- Reason about base cases and recursive cases for arithmetic functions

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

### Contracts

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

Using the provided CMake setup (recommended -- this is what the grader uses):

```bash
cd visible-tests
mkdir build && cd build
cmake .. -DSUBMISSION_DIR=../../assets
cmake --build .
./peano-math_tests
```

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
- **No standard library arithmetic functions** (`std::pow`, `__builtin_popcount`, etc.).
- All four functions must be implemented recursively.

The grader enforces these constraints automatically.  Submissions that violate
them will receive zero on the affected function.

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
