// Visible Catch2 test suite for Binary Bounds.
//
// Compile and run locally:
//   cd visible-tests
//   mkdir build && cd build
//   cmake .. -DSUBMISSION_DIR=<path-to-your-binary_bounds.hpp-directory>
//   cmake --build .
//   ./binary-bounds_tests

#include <catch2/catch_test_macros.hpp>
#include "binary_bounds.hpp"

using namespace bbounds;

TEST_CASE("linear_search basic", "[linear_search]") {
    std::vector<int> v = {2, 4, 6, 8, 10};
    REQUIRE(linear_search(v, 6) == 2);
    REQUIRE(linear_search(v, 5) == -1);
}

TEST_CASE("binary_search_idx basic", "[binary_search_idx]") {
    std::vector<int> v = {2, 4, 6, 8, 10};
    long idx = binary_search_idx(v, 8);
    REQUIRE(idx >= 0);
    REQUIRE(v[static_cast<std::size_t>(idx)] == 8);
    REQUIRE(binary_search_idx(v, 5) == -1);
}

TEST_CASE("first_occurrence basic", "[first_occurrence]") {
    std::vector<int> v = {1, 3, 3, 3, 5, 7, 7, 9, 11};
    REQUIRE(first_occurrence(v, 3) == 1);
    REQUIRE(first_occurrence(v, 4) == -1);
}

TEST_CASE("last_occurrence basic", "[last_occurrence]") {
    std::vector<int> v = {1, 3, 3, 3, 5, 7, 7, 9, 11};
    REQUIRE(last_occurrence(v, 3) == 3);
    REQUIRE(last_occurrence(v, 7) == 6);
}

TEST_CASE("count_of basic", "[count_of]") {
    std::vector<int> v = {1, 3, 3, 3, 5, 7, 7, 9, 11};
    REQUIRE(count_of(v, 3) == 3);
    REQUIRE(count_of(v, 7) == 2);
    REQUIRE(count_of(v, 4) == 0);
}

TEST_CASE("insert_position basic", "[insert_position]") {
    std::vector<int> v = {1, 3, 3, 3, 5, 7, 7, 9, 11};
    REQUIRE(insert_position(v, 4) == 4);
    REQUIRE(insert_position(v, 0) == 0);
    REQUIRE(insert_position(v, 100) == 9);
}
