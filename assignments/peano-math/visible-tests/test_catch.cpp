// Visible Catch2 test suite for Peano Math.
//
// Compile and run locally:
//   g++ -std=c++17 -Wall -Wextra -o peano_tests peano.cpp test_catch.cpp -lCatch2Main -lCatch2
//   ./peano_tests
//
// Or using the CMake setup in this directory:
//   mkdir build && cd build
//   cmake .. -DSUBMISSION_DIR=<path-to-your-submission>
//   cmake --build .
//   ./peano-math_tests

#include <catch2/catch_test_macros.hpp>
#include "peano.hpp"

TEST_CASE("successor basic", "[successor]") {
    REQUIRE(successor(0) == 1);
    REQUIRE(successor(1) == 2);
    REQUIRE(successor(9) == 10);
}

TEST_CASE("add identity", "[add]") {
    REQUIRE(add(0, 0) == 0);
    REQUIRE(add(0, 5) == 5);
    REQUIRE(add(5, 0) == 5);
}

TEST_CASE("add small", "[add]") {
    REQUIRE(add(2, 3) == 5);
    REQUIRE(add(3, 2) == 5);
    REQUIRE(add(4, 4) == 8);
}

TEST_CASE("multiply identity", "[multiply]") {
    REQUIRE(multiply(0, 5) == 0);
    REQUIRE(multiply(5, 0) == 0);
    REQUIRE(multiply(1, 7) == 7);
    REQUIRE(multiply(7, 1) == 7);
}

TEST_CASE("multiply small", "[multiply]") {
    REQUIRE(multiply(2, 3) == 6);
    REQUIRE(multiply(3, 4) == 12);
}

TEST_CASE("exponentiate base cases", "[exponentiate]") {
    REQUIRE(exponentiate(0, 0) == 1);
    REQUIRE(exponentiate(5, 0) == 1);
    REQUIRE(exponentiate(3, 1) == 3);
}

TEST_CASE("exponentiate small", "[exponentiate]") {
    REQUIRE(exponentiate(2, 3) == 8);
    REQUIRE(exponentiate(3, 2) == 9);
    REQUIRE(exponentiate(2, 4) == 16);
}
