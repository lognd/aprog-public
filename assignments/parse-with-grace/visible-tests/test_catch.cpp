// Visible Catch2 test suite for Parse With Grace.
//
// Compile and run locally:
//   mkdir build && cd build
//   cmake .. -DSUBMISSION_DIR=<path-to-your-submission>
//   cmake --build .
//   ./parse-with-grace_tests

#include <catch2/catch_test_macros.hpp>
#include "parse_with_grace.hpp"

using namespace pwg;

TEST_CASE("parse_int basic positive", "[parse_int]") {
    REQUIRE(parse_int("42") == 42);
}

TEST_CASE("parse_int basic negative", "[parse_int]") {
    REQUIRE(parse_int("-17") == -17);
}

TEST_CASE("parse_int throws invalid_argument on non-digit", "[parse_int]") {
    REQUIRE_THROWS_AS(parse_int("abc"), std::invalid_argument);
}

TEST_CASE("parse_int throws invalid_argument on empty string", "[parse_int]") {
    REQUIRE_THROWS_AS(parse_int(""), std::invalid_argument);
}

TEST_CASE("parse_int throws out_of_range on overflow", "[parse_int]") {
    REQUIRE_THROWS_AS(parse_int("99999999999999"), std::out_of_range);
}

TEST_CASE("parse_fraction basic", "[parse_fraction]") {
    Fraction f = parse_fraction("3/4");
    REQUIRE(f.numerator == 3);
    REQUIRE(f.denominator == 4);
}

TEST_CASE("parse_fraction throws domain_error on zero denominator", "[parse_fraction]") {
    REQUIRE_THROWS_AS(parse_fraction("3/0"), std::domain_error);
}

TEST_CASE("parse_fraction throws invalid_argument on missing slash", "[parse_fraction]") {
    REQUIRE_THROWS_AS(parse_fraction("34"), std::invalid_argument);
}

TEST_CASE("parse_int_list basic", "[parse_int_list]") {
    std::vector<int> v = parse_int_list("1,2,3", ',');
    REQUIRE(v == std::vector<int>{1, 2, 3});
}

TEST_CASE("parse_int_list propagates element error unchanged", "[parse_int_list]") {
    try {
        parse_int_list("1,x,3", ',');
        FAIL("expected an exception");
    } catch (const std::invalid_argument& e) {
        REQUIRE(std::string(e.what()).find("x") != std::string::npos);
    }
}

TEST_CASE("parse_int_or returns parsed value on success", "[parse_int_or]") {
    REQUIRE(parse_int_or("5", -1) == 5);
}

TEST_CASE("parse_int_or returns fallback on failure", "[parse_int_or]") {
    REQUIRE(parse_int_or("bad", -1) == -1);
}

TEST_CASE("ScopedTally increments and decrements on normal exit", "[ScopedTally]") {
    int tally = 0;
    {
        ScopedTally t(tally);
        REQUIRE(tally == 1);
    }
    REQUIRE(tally == 0);
}

TEST_CASE("ScopedTally decrements during unwinding through a thrown exception", "[ScopedTally]") {
    int tally = 0;
    try {
        ScopedTally t(tally);
        REQUIRE(tally == 1);
        throw std::runtime_error("boom");
    } catch (const std::runtime_error&) {
        // expected
    }
    REQUIRE(tally == 0);
}
