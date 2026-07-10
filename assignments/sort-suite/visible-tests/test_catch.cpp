// Visible Catch2 test suite for Sort Suite.
//
// Compile and run locally:
//   cd visible-tests
//   mkdir build && cd build
//   cmake .. -DSUBMISSION_DIR=<path-to-your-sort_suite.hpp-directory>
//   cmake --build .
//   ./sort-suite_tests

#include <catch2/catch_test_macros.hpp>
#include <string>
#include <utility>
#include <vector>
#include "sort_suite.hpp"

using namespace sortsuite;

TEST_CASE("selection_sort basic", "[selection_sort]") {
    std::vector<int> v = {5, 3, 8, 1, 4};
    selection_sort(v);
    REQUIRE(v == std::vector<int>{1, 3, 4, 5, 8});
}

TEST_CASE("insertion_sort basic", "[insertion_sort]") {
    std::vector<int> v = {5, 3, 8, 1, 4};
    insertion_sort(v);
    REQUIRE(v == std::vector<int>{1, 3, 4, 5, 8});
}

TEST_CASE("merge_sort basic", "[merge_sort]") {
    std::vector<int> v = {5, 3, 8, 1, 4};
    merge_sort(v);
    REQUIRE(v == std::vector<int>{1, 3, 4, 5, 8});
}

TEST_CASE("stable_sort_pairs basic keeps equal-key order", "[stable_sort_pairs]") {
    std::vector<std::pair<int, std::string>> v = {
        {2, "b"}, {1, "x"}, {2, "a"}, {1, "y"},
    };
    stable_sort_pairs(v);
    std::vector<std::pair<int, std::string>> expected = {
        {1, "x"}, {1, "y"}, {2, "b"}, {2, "a"},
    };
    REQUIRE(v == expected);
}

TEST_CASE("is_sorted_asc basic", "[is_sorted_asc]") {
    std::vector<int> sorted = {1, 2, 2, 5, 9};
    std::vector<int> unsorted = {1, 5, 2};
    REQUIRE(is_sorted_asc(sorted));
    REQUIRE_FALSE(is_sorted_asc(unsorted));
}
