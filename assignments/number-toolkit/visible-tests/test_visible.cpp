// Visible test driver -- compile with:
//   g++ -std=c++17 -o toolkit_test test_visible.cpp -I../assets
// Then run: ./toolkit_test

#include "../assets/number_toolkit.hpp"
#include <cassert>
#include <iostream>

int main() {
    // is_prime
    assert(is_prime(17)  == true);
    assert(is_prime(9)   == false);

    // gcd
    assert(gcd(12, 8) == 4);
    assert(gcd(7,  3) == 1);

    // digit_sum
    assert(digit_sum(123) == 6);
    assert(digit_sum(0)   == 0);

    // count_divisors
    assert(count_divisors(12) == 6);
    assert(count_divisors(7)  == 2);

    // nth_fibonacci
    assert(nth_fibonacci(1) == 1);
    assert(nth_fibonacci(7) == 13);

    // is_power_of_two
    assert(is_power_of_two(1)  == true);
    assert(is_power_of_two(8)  == true);
    assert(is_power_of_two(6)  == false);
    assert(is_power_of_two(0)  == false);

    // popcount
    assert(popcount(0)  == 0);
    assert(popcount(1)  == 1);
    assert(popcount(13) == 3);   // 0b1101

    // is_abundant
    assert(is_abundant(12) == true);   // 1+2+3+4+6 = 16 > 12
    assert(is_abundant(6)  == false);  // 1+2+3 = 6 (perfect, not abundant)
    assert(is_abundant(1)  == false);

    std::cout << "All visible tests passed.\n";
    return 0;
}
