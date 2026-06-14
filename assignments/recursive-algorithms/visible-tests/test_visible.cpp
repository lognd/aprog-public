// Visible tests for recursive-algorithms.
// Compile: g++ -std=c++17 -I.. -o tests test_visible.cpp ../recursive_algorithms.cpp
// Run:     ./tests
#include "../recursive_algorithms.hpp"
#include <cassert>
#include <iostream>
#include <string>
#include <vector>

static int passed = 0;
static int failed = 0;

#define CHECK(expr) do { \
    if (expr) { ++passed; } \
    else { ++failed; std::cerr << "FAIL: " #expr " (line " << __LINE__ << ")\n"; } \
} while(0)

int main() {
    // binary_search
    {
        std::vector<int> v = {1, 3, 5, 7, 9};
        CHECK(recur::binary_search(v, 5, 0, 4) == 2);
        CHECK(recur::binary_search(v, 4, 0, 4) == -1);
        CHECK(recur::binary_search(v, 1, 0, 4) == 0);
        CHECK(recur::binary_search(v, 9, 0, 4) == 4);
    }

    // merge_sort
    {
        std::vector<int> v = {5, 3, 1, 4, 2};
        recur::merge_sort(v, 0, 4);
        CHECK((v == std::vector<int>{1, 2, 3, 4, 5}));

        std::vector<int> w = {7};
        recur::merge_sort(w, 0, 0);
        CHECK(w[0] == 7);
    }

    // fibonacci
    {
        std::vector<long long> cache(35, -1);
        CHECK(recur::fibonacci(0, cache) == 0);
        CHECK(recur::fibonacci(1, cache) == 1);
        CHECK(recur::fibonacci(10, cache) == 55);
    }

    // digit_sum
    {
        CHECK(recur::digit_sum(0) == 0);
        CHECK(recur::digit_sum(5) == 5);
        CHECK(recur::digit_sum(493) == 16);
    }

    // is_palindrome
    {
        std::string s1 = "racecar";
        CHECK(recur::is_palindrome(s1, 0, 6));
        std::string s2 = "hello";
        CHECK(!recur::is_palindrome(s2, 0, 4));
        std::string s3 = "a";
        CHECK(recur::is_palindrome(s3, 0, 0));
    }

    std::cout << passed << " check(s) passed";
    if (failed) std::cerr << "\n" << failed << " check(s) FAILED\n";
    else std::cout << "\n";
    return failed ? 1 : 0;
}
