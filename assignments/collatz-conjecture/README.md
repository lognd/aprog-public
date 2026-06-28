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
- Think about `unsigned long long` overflow boundaries when reasoning about input validity

## Your task

You are given the following header file:

**`collatz.hpp`**
```cpp
#include <iostream>

void collatz(unsigned long long n) {
    std::cout << "TODO: implement collatz sequence logic." << std::endl;
}
```

Implement the `collatz` function so that it prints each value in the sequence,
one per line, starting from `n` and ending when it reaches `1`.

Your function will be called from a `main.cpp` provided by the grader. For example:

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

## Constraints

**You may not use the following operators anywhere in your program:**

- `*` or `*=` (multiplication)
- `/` or `/=` (division)
- `-` or `-=` (subtraction)

**You may use the addition or addition-assignment operator (`+` or `+=`) at most once.**

You may use any operator not listed above, including bitwise operators (`<<`, `>>`, `&`, `|`, `^`, `~`).

**Bonus:** Complete the assignment without using `+` or `+=` at all.

## Notes

- Your solution must be correct for any `n` such that no value in the sequence
  exceeds the bounds of `unsigned long long`.
- Do not add a `main` function to `collatz.hpp`.
- Submit only `collatz.hpp`.

## Going further

- Verify that the bonus constraint (no `+` or `+=` at all) is achievable using
  only bitwise operators. Which operator replaces increment?
- Look up the current state of the Collatz conjecture. What is the largest
  starting value that has been verified to reach 1?
- Modify your function to also print the sequence length (number of steps to
  reach 1) after the sequence. What is the length for n = 27?
