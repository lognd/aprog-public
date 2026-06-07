# Number Toolkit

Implement five number-theory utility functions in `number_toolkit.hpp`.

## Functions

| Function | Signature | Notes |
|----------|-----------|-------|
| `is_prime` | `bool is_prime(long long n)` | Must be O(sqrt(n)); a naive O(n) loop fails the performance test on a large prime. |
| `gcd` | `long long gcd(long long a, long long b)` | Loop down from `min(a, b)` for full points. Euclidean algorithm earns bonus credit. |
| `digit_sum` | `long long digit_sum(long long n)` | Sum of decimal digits. Handles negatives and zero. |
| `count_divisors` | `long long count_divisors(long long n)` | Count all positive divisors of `n`. |
| `nth_fibonacci` | `long long nth_fibonacci(long long n)` | 1-indexed iterative Fibonacci. `nth_fibonacci(1) == 1`. |

## Examples

```cpp
is_prime(17)          // true
is_prime(9)           // false
gcd(12, 8)            // 4
gcd(7, 3)             // 1  (coprime)
digit_sum(123)        // 6
digit_sum(-456)       // 15
digit_sum(0)          // 0
count_divisors(12)    // 6  (1,2,3,4,6,12)
count_divisors(7)     // 2  (1,7)
nth_fibonacci(1)      // 1
nth_fibonacci(7)      // 13
```

## Constraints

- `is_prime`: return `false` for any `n < 2`.
- `gcd`: both `a` and `b` are positive integers.
- `digit_sum`: treat negative input as its absolute value.
- `count_divisors`: `n` is a positive integer.
- `nth_fibonacci`: `n` is a positive integer; use an iterative loop (do-while or while).
- Do not add a `main` function to your header.
- Do not use `std::gcd` or `__gcd`.

## Grading

| Component             | Points |
|-----------------------|--------|
| Visible correctness   | 50     |
| Hidden correctness    | 40     |
| is_prime performance  | 10     |
| **Total**             | **100** |
| Euclidean GCD bonus   | +5     |

The performance test calls `is_prime(999999937)` with a 0.1-second time limit.
An O(sqrt(n)) implementation finishes in microseconds; O(n) does not pass.

## Submission

Submit a single file named `number_toolkit.hpp`. Do not rename the file.

## Local Testing

```bash
g++ -std=c++17 -o toolkit_test visible-tests/test_visible.cpp -I assets
./toolkit_test
```
