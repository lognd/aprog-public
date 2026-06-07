#include "stats.h"
#include <cassert>
#include <cstdio>

int main() {
    // sum_of_primes
    assert(sum_of_primes(10) == 17);   // 2+3+5+7
    assert(sum_of_primes(2)  == 2);
    assert(sum_of_primes(1)  == 0);
    assert(sum_of_primes(0)  == 0);

    // count_primes_in
    assert(count_primes_in(1,  10) == 4);   // 2,3,5,7
    assert(count_primes_in(10, 20) == 4);   // 11,13,17,19
    assert(count_primes_in(14, 16) == 0);
    assert(count_primes_in(2,  2)  == 1);

    // is_abundant
    assert(is_abundant(12) == true);    // 1+2+3+4+6 = 16 > 12
    assert(is_abundant(20) == true);    // 1+2+4+5+10 = 22 > 20
    assert(is_abundant(6)  == false);   // 1+2+3 = 6  (perfect)
    assert(is_abundant(7)  == false);   // 1 < 7
    assert(is_abundant(1)  == false);

    std::printf("All tests passed.\n");
    return 0;
}
