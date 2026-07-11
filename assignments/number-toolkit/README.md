# Number Toolkit

Number theory shows up everywhere in real programs -- checking a key size is a
power of two, deciding whether two rates share a common factor, hashing, or
just summing digits for a checksum -- and most of these problems have both a
slow, obvious solution and a fast one that is barely any more code. This
assignment is a tour of eight such problems: for each one, the "obvious"
approach works but does not scale, and a small change in HOW you loop (not
how much code you write) is the difference between an answer that comes back
instantly and one that never finishes.

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

## Examples at a glance

To make all eight functions concrete, here is **one** number, `n = 28`, and
what every function in this assignment produces for it. Read this table
first -- it is the whole assignment in miniature. (`28` is a nice pick
because it is even, not prime, and turns out to be a "perfect number" --
which matters for the last row below.)

| Call | Returns | Why |
|------|---------|-----|
| `is_prime(28)`        | `false`  | `28` is even and greater than `2`, so `2` divides it -- not prime |
| `gcd(28, 12)`         | `4`      | `28 = 4 * 7` and `12 = 4 * 3`; the largest factor they share is `4` |
| `digit_sum(28)`       | `10`     | its digits are `2` and `8`, and `2 + 8 = 10` |
| `count_divisors(28)`  | `6`      | `1, 2, 4, 7, 14, 28` all divide `28` evenly -- six divisors total |
| `nth_fibonacci(28)`   | `317811` | the 28th Fibonacci number, built up one step at a time from `nth_fibonacci(1) == 1` |
| `is_power_of_two(28)` | `false`  | `28` in binary is `11100` -- more than one bit is set |
| `popcount(28)`        | `3`      | `28 == 0b11100`, which has three `1`-bits |
| `is_abundant(28)`     | `false`  | `28`'s proper divisors are `1 + 2 + 4 + 7 + 14 = 28`, exactly equal to `28` (a "perfect number"), not more than it |

## Worked example: watch `gcd(28, 12)` run step by step

This is the trickiest function to get right efficiently, so here is every
step of the Euclidean algorithm spelled out. We start with `a = 28`,
`b = 12`, and repeat while `b != 0`: replace `a` with the old `b`, and
replace `b` with the remainder of `a` divided by `b` (written `a % b`).

| Step | `a` | `b` | Is `b == 0`? | Action |
|------|-----|-----|--------------|--------|
| start | 28 | 12 | no  | compute `28 % 12 = 4`; new `a` = old `b` = `12`, new `b` = the remainder = `4` |
| 2     | 12 | 4  | no  | compute `12 % 4 = 0`; new `a` = old `b` = `4`, new `b` = the remainder = `0` |
| end   | 4  | 0  | yes | loop stops; `gcd` returns `a`, which is `4` |

The loop ends with `a == 4`, so `gcd(28, 12)` returns **`4`**. Notice the
algorithm never counted down from `min(a, b)` one number at a time -- each
step replaces the pair `(a, b)` with the smaller pair `(b, a % b)`, which
shrinks far faster than counting down does. That speed is exactly why the
Euclidean variant earns bonus credit over the loop-down version.

## Task

Implement the following eight functions in `number_toolkit.hpp`:

**1. `is_prime` -- `bool is_prime(long long n)`.** Must not test every
number up to `n` -- testing divisors up to the square root of `n` is
enough and required; a loop that checks every number up to `n` fails the
performance test on a large prime.

- **Example (prime):** `is_prime(17) == true`.
- **Example (composite):** `is_prime(9) == false`.
- **Edge case (below range):** `is_prime(1) == false` -- **anything less
  than `2` is never prime**.

**2. `gcd` -- `long long gcd(long long a, long long b)`.** Loop down from
`min(a, b)` for full points. Euclidean algorithm earns bonus credit.

- **Example (common factor):** `gcd(12, 8) == 4`.
- **Example (coprime):** `gcd(7, 3) == 1` -- **the two numbers share no
  common factor besides `1`**.
- **Edge case (equal inputs):** `gcd(5, 5) == 5` -- **a number is its own
  gcd with itself**.

**3. `digit_sum` -- `long long digit_sum(long long n)`.** Sum of decimal
digits. Handles negatives and zero.

- **Example (positive):** `digit_sum(123) == 6`.
- **Example (negative):** `digit_sum(-456) == 15` -- **negative input is
  treated as its absolute value**.
- **Edge case (zero):** `digit_sum(0) == 0`.

**4. `count_divisors` -- `long long count_divisors(long long n)`.** Count
all positive divisors of `n`.

- **Example (composite):** `count_divisors(12) == 6`.
- **Example (prime):** `count_divisors(7) == 2` -- **every prime has
  exactly two divisors: `1` and itself**.
- **Edge case (one):** `count_divisors(1) == 1` -- only `1` divides `1`.

**5. `nth_fibonacci` -- `long long nth_fibonacci(long long n)`.**
1-indexed iterative Fibonacci. `nth_fibonacci(1) == 1`.

- **Example (first term):** `nth_fibonacci(1) == 1`.
- **Example (second term):** `nth_fibonacci(2) == 1` -- **the first two
  terms are both `1`**.
- **Example (seventh term):** `nth_fibonacci(7) == 13`.

**6. `is_power_of_two` -- `bool is_power_of_two(long long n)`.** `n > 0`
and exactly one bit set. Must use bitwise operations only -- no loops, no
division.

- **Example (power of two):** `is_power_of_two(8) == true`.
- **Example (not a power of two):** `is_power_of_two(6) == false`.
- **Edge case (zero):** `is_power_of_two(0) == false` -- **zero has no
  bits set at all, so it fails the "exactly one bit" test**.

**7. `popcount` -- `int popcount(unsigned long long n)`.** Number of
1-bits in `n`. Must use bit manipulation (shifts and masks) -- no library
functions.

- **Example (multiple bits):** `popcount(13) == 3` (`13 == 0b1101`).
- **Edge case (zero):** `popcount(0) == 0`.
- **Edge case (one bit):** `popcount(1) == 1`.

**8. `is_abundant` -- `bool is_abundant(long long n)`.** `true` if the
sum of `n`'s proper divisors (positive divisors strictly less than `n`)
exceeds `n`.

- **Example (abundant):** `is_abundant(12) == true` (`1+2+3+4+6 = 16 >
  12`).
- **Example (perfect, not abundant):** `is_abundant(6) == false`
  (`1+2+3 = 6`, a "perfect number", **not abundant**).
- **Edge case (one):** `is_abundant(1) == false` -- **`1` has no proper
  divisors to sum**.

All eight signatures at a glance:

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
