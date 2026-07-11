# Collatz Conjecture

The Collatz Conjecture is one of the most notorious unsolved problems in mathematics.
You will not have to solve it in this lab. However, the premise is simple.

Take any positive integer **n** and apply the following rules repeatedly:

- If **n** is even: `f(n) = n / 2`
- If **n** is odd: `f(n) = 3n + 1`

Repeat, feeding the output back into the input, until the sequence loops.
The conjecture is that every positive integer eventually falls into the 4 -> 2 -> 1 loop.

## Examples at a glance

The table below shows several starting values `n`, how many lines the
sequence prints (its **length**, i.e. the number of steps including the
starting value and the final `1`), and the largest value the sequence
ever reaches (its **max**). All values are confirmed by actually running
the reference solution.

| `n` | Length (lines printed) | Max value reached | Why |
|-----|-------------------------|--------------------|-----|
| `1` | 1 | 1 | the loop's base case: `1` is odd and even at once as far as this problem cares -- the function checks "is it 1?" first and stops immediately, printing only `1` |
| `2` | 2 | 2 | `2` is even, so `2 / 2 = 1`; only one step is needed to reach `1` |
| `8` | 4 | 8 | `8` is a power of two (`2^3`), so every step just halves it: `8, 4, 2, 1` -- powers of two never grow, they only shrink |
| `16` | 5 | 16 | another power of two (`2^4`); same halving pattern, one step longer than `8` |
| `5` | 6 | 16 | `5` is odd, so it grows first (`5 -> 16`) before it starts shrinking; this is the exact case worked step-by-step below |
| `6` | 9 | 16 | `6` is even but its sequence still passes through the same `5 -> 16 -> ... -> 1` tail once it reaches `3 -> 10 -> 5` |
| `7` | 17 | 52 | a small starting number can still take many steps and climb well above its own value before collapsing to `1` |
| `27` | 112 | 9232 | a famous example: this small-looking input takes over a hundred steps and climbs past 9000 before finally reaching `1` -- a good stress test that your loop does not stop early or overflow |
| `100` | 26 | 100 | its own starting value is also its max -- it never grows past `100`, it only shrinks (with some odd-step detours) |
| `871` | 179 | 190996 | a larger starting value with a long sequence and a very large peak -- useful for checking your `unsigned long long` arithmetic does not overflow or truncate |

---

## Worked example: watch `collatz(5)` run, step by step

This is the exact case used by the visible test, so tracing it by hand
tells you precisely what your loop must do. Each row is one full
iteration of the loop: look at the current value, decide even or odd,
print the current value, then compute the next value.

| Step | Current `n` | Even or odd? | Printed | Next value | Why |
|------|-------------|--------------|---------|------------|-----|
| 1 | 5 | odd | `5` | `3*5 + 1 = 16` | `5` is not `1`, so the loop continues; odd means apply `3n + 1` |
| 2 | 16 | even | `16` | `16 / 2 = 8` | even means apply `n / 2` |
| 3 | 8 | even | `8` | `8 / 2 = 4` | still even, halve again |
| 4 | 4 | even | `4` | `4 / 2 = 2` | still even, halve again |
| 5 | 2 | even | `2` | `2 / 2 = 1` | still even, halve again |
| 6 | 1 | -- | `1` | (stop) | `n` is now `1`, so the loop prints it one last time and stops |

Final printed output (matches `expected/collatz_5.txt` exactly):
```
5
16
8
4
2
1
```
Six lines printed total (the sequence length is 6), and the largest
value seen along the way is `16` (the max). Notice the value goes UP
before it comes back down -- odd numbers under the `3n + 1` rule can
temporarily grow larger than where they started; this is normal and is
exactly what the conjecture is about (every positive integer eventually
falls back down to `1`, no matter how high it climbs first).

---

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

*Examples:* (all confirmed against the reference solution)
- `collatz(1)` prints just `1` -- the base case. `n` starts already equal
  to `1`, so the loop's "have we reached 1 yet?" check is true immediately
  and nothing else ever prints.
- `collatz(8)` prints `8, 4, 2, 1` (four lines). `8` is a power of two
  (`2^3`), so every step only ever halves -- it never takes the `3n + 1`
  branch at all.
- `collatz(6)` prints `6, 3, 10, 5, 16, 8, 4, 2, 1` (nine lines) -- note
  it mixes even and odd steps (`6 -> 3` halves, `3 -> 10` applies
  `3n + 1`) before settling into the same shrinking tail as `collatz(5)`.
- `collatz(27)` prints 112 lines and climbs as high as `9232` before
  falling back to `1` -- a small starting value with a surprisingly long,
  large-valued sequence; a good check that your loop does not stop early
  and that your arithmetic does not overflow partway through.
- `collatz(871)` prints 179 lines and peaks at `190996`, the largest
  value in this assignment's grading cases -- confirms your
  `unsigned long long` arithmetic holds up for bigger, longer-climbing
  inputs.

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
