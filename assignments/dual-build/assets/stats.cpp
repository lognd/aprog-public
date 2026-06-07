#include "stats.h"

static bool is_prime(int n) {
    if (n < 2) return false;
    for (int d = 2; d * d <= n; ++d)
        if (n % d == 0) return false;
    return true;
}

long long sum_of_primes(int limit) {
    long long total = 0;
    for (int n = 2; n <= limit; ++n)
        if (is_prime(n)) total += n;
    return total;
}

int count_primes_in(int lo, int hi) {
    int count = 0;
    for (int n = lo; n <= hi; ++n)
        if (is_prime(n)) ++count;
    return count;
}

bool is_abundant(int n) {
    if (n < 2) return false;
    int sum = 1;
    for (int d = 2; d * d <= n; ++d) {
        if (n % d == 0) {
            sum += d;
            if (d != n / d) sum += n / d;
        }
    }
    return sum > n;
}
