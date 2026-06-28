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

### Constraints

- **No loops.** `for`, `while`, and `do` are forbidden in `peano.cpp`.
- **No `+` operator in `add`, `multiply`, or `exponentiate`.**
  The `+` operator (and `++`, `+=`) may only appear inside `successor`.
- **No `*`, `/`, `%` operators anywhere.**
- **No standard library arithmetic functions** (`std::pow`, `__builtin_popcount`, etc.).
- All four functions must be implemented recursively.

The grader enforces these constraints automatically.  Submissions that violate
them will receive zero on the affected function.

## Files

- `peano.cpp` -- **submit this file.**  Implement all four functions here.
- `peano.hpp` -- provided; do not modify.  Contains the function declarations.

## Compilation and Testing

```bash
g++ -std=c++17 -Wall -Wextra -o peano_tests peano.cpp visible-tests/test_visible.cpp
./peano_tests
```

Or compile your own driver:

```bash
g++ -std=c++17 -Wall -Wextra -o run peano.cpp main.cpp
./run
```

## Grading

- 20 pts -- `successor`: correctness
- 20 pts -- `add`: correctness
- 20 pts -- `multiply`: correctness
- 20 pts -- `exponentiate`: correctness
- 20 pts -- constraints satisfied (no loops, operator rules)
- 10 pts extra credit -- all four functions correct and constraints satisfied on
  large inputs (stress tests)

## Going further

- Implement `subtract(a, b)` using only `successor` and recursion. What is the
  base case, and how do you handle the case where `b > a`?
- Read about Church numerals -- a representation of natural numbers as functions.
  How does it relate to what you implemented here?
- Add a `modulo(a, b)` function built from `subtract` and comparison. Can you
  then implement `is_prime` using only your Peano primitives?
