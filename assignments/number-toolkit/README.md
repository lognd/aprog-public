# Number Toolkit

Implement eight number-theory and bit-manipulation utility functions in
`number_toolkit.hpp`.

## Learning goals

- Implement number-theory algorithms that stay fast as their input grows
- Test primality by trial division only up to the square root of `n`,
  instead of checking every number up to `n` -- for a large `n` this is
  the difference between finishing instantly and not finishing at all
- Apply the Euclidean algorithm (a fast, ancient method for computing the
  greatest common divisor by repeated division instead of counting down) and
  understand why it is faster than looping from min(a, b)
- Write iterative Fibonacci -- using a loop instead of a function that calls
  itself (a technique called recursion, covered in a later topic) -- so the
  work grows one step at a time instead of ballooning: a naive recursive
  version redoes so much repeated work that it quickly becomes far too slow
  to run

(The formal tool for talking about "how many steps as input grows"
precisely -- Big-O notation -- arrives later in the course, in the
Complexity Theory topic. For now, the goal is just to feel the difference
between an approach that stays fast and one that does not.)

## Task

Implement the following eight functions in `number_toolkit.hpp`:

| Function | Signature | Notes |
|----------|-----------|-------|
| `is_prime` | `bool is_prime(long long n)` | Must not test every number up to `n` -- testing divisors up to the square root of `n` is enough and required; a loop that checks every number up to `n` fails the performance test on a large prime. |
| `gcd` | `long long gcd(long long a, long long b)` | Loop down from `min(a, b)` for full points. Euclidean algorithm earns bonus credit. |
| `digit_sum` | `long long digit_sum(long long n)` | Sum of decimal digits. Handles negatives and zero. |
| `count_divisors` | `long long count_divisors(long long n)` | Count all positive divisors of `n`. |
| `nth_fibonacci` | `long long nth_fibonacci(long long n)` | 1-indexed iterative Fibonacci. `nth_fibonacci(1) == 1`. |
| `is_power_of_two` | `bool is_power_of_two(long long n)` | `n > 0` and exactly one bit set. Must use bitwise operations only -- no loops, no division. |
| `popcount` | `int popcount(unsigned long long n)` | Number of 1-bits in `n`. Must use bit manipulation (shifts and masks) -- no library functions. |
| `is_abundant` | `bool is_abundant(long long n)` | `true` if the sum of `n`'s proper divisors (positive divisors strictly less than `n`) exceeds `n`. |

Examples:

```cpp
is_prime(17)          // true
is_prime(9)           // false
gcd(12, 8)            // 4
gcd(7, 3)             // 1  (coprime -- the two numbers share no common factor besides 1)
digit_sum(123)        // 6
digit_sum(-456)       // 15
digit_sum(0)          // 0
count_divisors(12)    // 6  (1,2,3,4,6,12)
count_divisors(7)     // 2  (1,7)
nth_fibonacci(1)      // 1
nth_fibonacci(7)      // 13
is_power_of_two(8)    // true
is_power_of_two(6)    // false
popcount(13)          // 3  (13 == 0b1101)
is_abundant(12)       // true   (1+2+3+4+6 = 16 > 12)
is_abundant(6)        // false  (1+2+3 = 6, perfect, not abundant)
```

## Files

| File | Purpose |
|------|---------|
| `assets/number_toolkit.hpp` | Starter header -- implement all eight functions here |
| `visible-tests/test_visible.cpp` | Visible test driver; exercises all eight functions |

## Compilation and Testing

```bash
g++ -std=c++17 -o toolkit_test visible-tests/test_visible.cpp -Iassets
./toolkit_test
```

## Constraints

- `is_prime`: return `false` for any `n < 2`.
- `gcd`: both `a` and `b` are positive integers.
- `digit_sum`: treat negative input as its absolute value.
- `count_divisors`: `n` is a positive integer.
- `nth_fibonacci`: `n` is a positive integer; use an iterative loop (do-while or while).
- `is_power_of_two`: no loops, no division -- bitwise operations only.
- `popcount`: no library functions (e.g. no `std::popcount` or `__builtin_popcount`) -- shifts and masks only.
- Do not add a `main` function to your header.
- Do not use `std::gcd` or `__gcd`.

## Grading

| Component                          | Points |
|-------------------------------------|--------|
| `is_prime` -- visible correctness   | 10     |
| `is_prime` -- hidden correctness    | 12     |
| `is_prime` -- performance           | 10     |
| `gcd` -- visible correctness        | 10     |
| `gcd` -- hidden correctness         | 8      |
| `digit_sum` -- visible correctness  | 10     |
| `digit_sum` -- hidden correctness   | 4      |
| `count_divisors` -- visible correctness | 10 |
| `count_divisors` -- hidden correctness  | 8  |
| `nth_fibonacci` -- visible correctness  | 10 |
| `nth_fibonacci` -- hidden correctness   | 8  |
| **Total**                            | **100** |
| Euclidean GCD bonus (`gcd`)          | +5     |

The performance test calls `is_prime(999999937)` with a 0.1-second time limit.
Trial division up to the square root of `n` finishes in microseconds; a loop
that checks every number up to `n` does not pass.

`is_power_of_two`, `popcount`, and `is_abundant` are required -- the visible
test driver will not compile without correct signatures, and a wrong
implementation fails its `assert`s -- but they are not yet separately
weighted in the autograder's point map above. Get them right anyway: a
failing `assert` in `visible-tests/test_visible.cpp` stops that program
before it reaches later checks.

## Submission

Submit a single file named `number_toolkit.hpp`. Do not rename the file.

## Going further

- Implement the Sieve of Eratosthenes and benchmark it against your trial-division
  `is_prime` for finding all primes up to 1,000,000. At what threshold does the
  sieve become faster?
- Look up Miller-Rabin primality testing. How does it differ from trial division,
  and at what input size does it become relevant?
- Add a `prime_factors` function that returns the prime factorization of n as a
  sorted vector. Use your `is_prime` to guide it.
