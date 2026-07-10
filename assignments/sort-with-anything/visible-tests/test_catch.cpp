// Visible Catch2 test suite for Sort With Anything.
//
// Compile and run locally:
//   cd visible-tests
//   mkdir build && cd build
//   cmake .. -DSUBMISSION_DIR=<path-to-your-sort_with_anything.hpp-directory>
//   cmake --build .
//   ./sort-with-anything_tests

#include <catch2/catch_test_macros.hpp>
#include <string>
#include <vector>
#include "sort_with_anything.hpp"

using namespace swa;

TEST_CASE("sort_by with lambda comparator sorts ascending", "[sort_by]") {
    std::vector<int> v = {5, 3, 8, 1, 4};
    sort_by(v, [](int a, int b) { return a < b; });
    REQUIRE(v == std::vector<int>{1, 3, 4, 5, 8});
}

TEST_CASE("sort_by with free function comparator (by_length_asc)", "[sort_by]") {
    std::vector<std::string> v = {"ccc", "a", "bb", "dddd"};
    sort_by(v, by_length_asc);
    REQUIRE(v == std::vector<std::string>{"a", "bb", "ccc", "dddd"});
}

TEST_CASE("sort_by with functor comparator (ByAbsoluteValue)", "[sort_by]") {
    std::vector<int> v = {3, -1, -5, 2, -2};
    sort_by(v, ByAbsoluteValue{});
    // abs(-1)=1, abs(2)=2, abs(-2)=2 (tie: -2 before 2, smaller actual
    // value first), abs(3)=3, abs(-5)=5
    REQUIRE(v == std::vector<int>{-1, -2, 2, 3, -5});
}

TEST_CASE("filter basic", "[filter]") {
    std::vector<int> v = {1, 2, 3, 4, 5, 6};
    auto evens = filter(v, [](int x) { return x % 2 == 0; });
    REQUIRE(evens == std::vector<int>{2, 4, 6});
}

TEST_CASE("for_each_apply basic mutates in place", "[for_each_apply]") {
    std::vector<int> v = {1, 2, 3};
    for_each_apply(v, [](int& x) { x *= 10; });
    REQUIRE(v == std::vector<int>{10, 20, 30});
}

TEST_CASE("count_matching basic", "[count_matching]") {
    std::vector<int> v = {1, 2, 3, 4, 5, 6};
    std::size_t n = count_matching(v, [](int x) { return x > 3; });
    REQUIRE(n == 3);
}
