#pragma once

// Returns the sum of all primes in [2, limit].
// Returns 0 if limit < 2.
long long sum_of_primes(int limit);

// Returns the count of primes in [lo, hi] inclusive.
int count_primes_in(int lo, int hi);

// Returns true if n is abundant: the sum of n's proper divisors
// (all positive divisors strictly less than n) is greater than n.
// is_abundant(1) == false, is_abundant(6) == false (perfect), is_abundant(12) == true.
bool is_abundant(int n);
