#pragma once
#include <cstdlib>

// Returns true if n is prime (n >= 2 and has no divisors other than 1 and itself).
// Must run in O(sqrt(n)) time.
bool is_prime(long long n) {
    // TODO
    return false;
}

// Returns the greatest common divisor of two positive integers a and b.
long long gcd(long long a, long long b) {
    // TODO
    return 0;
}

// Returns the sum of the decimal digits of n. Treats negative input as its
// absolute value. Returns 0 for n == 0.
long long digit_sum(long long n) {
    // TODO
    return 0;
}

// Returns the number of positive divisors of n.
long long count_divisors(long long n) {
    // TODO
    return 0;
}

// Returns the nth Fibonacci number (1-indexed, iterative).
// nth_fibonacci(1) == 1, nth_fibonacci(2) == 1, nth_fibonacci(3) == 2, ...
long long nth_fibonacci(long long n) {
    // TODO
    return 0;
}

// Returns true if n is a power of two (n > 0 and exactly one bit is set).
// Must use bitwise operations; no loops or division.
bool is_power_of_two(long long n) {
    // TODO
    return false;
}

// Returns the number of 1-bits in the binary representation of n.
// Example: popcount(13) == 3  because 13 == 0b1101
// Must use bit manipulation (shifts and masks); no library functions.
int popcount(unsigned long long n) {
    // TODO
    return 0;
}

// Returns true if n is abundant: the sum of its proper divisors exceeds n.
// A proper divisor of n is a positive divisor strictly less than n.
// Example: is_abundant(12) == true  because 1+2+3+4+6 = 16 > 12
// is_abundant(1) == false, is_abundant(6) == false (6 is perfect, not abundant)
bool is_abundant(long long n) {
    // TODO
    return false;
}
