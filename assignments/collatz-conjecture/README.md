# Collatz Conjecture

The Collatz Conjecture is one of the most notorious unsolved problems in mathematics.
You will not have to solve it in this lab. However, the premise is simple.

Take any positive integer **n** and apply the following rules repeatedly:

- If **n** is even: `f(n) = n / 2`
- If **n** is odd: `f(n) = 3n + 1`

Repeat, feeding the output back into the input, until the sequence loops.
The conjecture is that every positive integer eventually falls into the 4 -> 2 -> 1 loop.

## Learning goals

- Implement a mathematical sequence using bitwise operators instead of multiplication and division
- Understand why bitwise shifts are equivalent to multiplying and dividing by powers of two
- Work within operator constraints while still producing correct output
- Think about `unsigned long long` overflow boundaries (overflow happens
  when a value grows past the largest number a type can hold and wraps back
  around, producing an incorrect result) when reasoning about input validity

## Task

You are given the following header file:

**`collatz.hpp`**
```cpp
#pragma once
#include <iostream>

void collatz(unsigned long long n) {
    std::cout << "TODO: implement collatz sequence logic." << std::endl;
}
```

Implement the `collatz` function so that it prints each value in the sequence,
one per line, starting from `n` and ending when it reaches `1`.

Your function will be called from a `main.cpp` provided by the grader, which
reads `n` from the command line and passes it to `collatz`. The visible test
driver below calls it directly with a fixed value so you can check your work
locally without any command-line arguments:

```cpp
#include "collatz.hpp"

int main() {
    collatz(5);
    return 0;
}
```

Expected output:
```
5
16
8
4
2
1
```

Your solution must be correct for any `n` such that no value in the sequence
exceeds the bounds of `unsigned long long`.

## Files

| File | Purpose |
|------|---------|
| `assets/collatz.hpp` | Starter header -- implement `collatz` here |
| `visible-tests/test_collatz.cpp` | Visible test driver; calls `collatz(5)` |
| `expected/collatz_5.txt` | Expected output for the visible test |

## Compilation and Testing

```bash
g++ -std=c++17 -o collatz_test visible-tests/test_collatz.cpp -Iassets
./collatz_test
```

Compare the output against `expected/collatz_5.txt`.

## Constraints

- Do not use `*` or `*=` (multiplication) anywhere in your program.
- Do not use `/` or `/=` (division) anywhere in your program.
- Do not use `-` or `-=` (subtraction) anywhere in your program.
- You may use `+` or `+=` (addition) at most once.
- You may use any operator not listed above, including bitwise operators
  (`<<`, `>>`, `&`, `|`, `^`, `~`).
- Do not add a `main` function to `collatz.hpp`.

**Bonus:** complete the assignment without using `+` or `+=` at all.

## Grading

| Component                     | Points |
|--------------------------------|--------|
| Operator constraints check     | 0*     |
| Compilation                    | 0*     |
| n = 1                           | 5      |
| n = 2                           | 5      |
| n = 5                           | 10     |
| n = 6                           | 10     |
| n = 7                           | 10     |
| n = 27                          | 15     |
| n = 100                         | 15     |
| n = 871                         | 15     |
| n = 9780657631 (large)          | 15     |
| **Total**                       | **100** |

\* The operator constraints check and compilation step must pass cleanly before
any correctness cases are scored, but do not themselves carry points.

## Submission

Submit a single file named `collatz.hpp`. Do not rename it.

## Going further

- Verify that the bonus constraint (no `+` or `+=` at all) is achievable using
  only bitwise operators. Which operator replaces increment?
- Look up the current state of the Collatz conjecture. What is the largest
  starting value that has been verified to reach 1?
- Modify your function to also print the sequence length (number of steps to
  reach 1) after the sequence. What is the length for n = 27?
