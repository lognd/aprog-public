// Visible Catch2 test suite for Text Filters.
//
// Compile and run locally:
//   mkdir build && cd build
//   cmake .. -DSUBMISSION_DIR=<path-to-your-submission>
//   cmake --build .
//   ./text-filters_tests

#include <catch2/catch_test_macros.hpp>
#include <string>
#include <vector>
#include "text_filters.hpp"

using namespace tf;

TEST_CASE("UppercaseFilter converts to uppercase", "[UppercaseFilter]") {
    UppercaseFilter f;
    REQUIRE(f.apply("hello world") == "HELLO WORLD");
    REQUIRE(f.apply("Already UP") == "ALREADY UP");
}

TEST_CASE("TrimFilter removes leading and trailing whitespace", "[TrimFilter]") {
    TrimFilter f;
    REQUIRE(f.apply("  hello world  ") == "hello world");
    REQUIRE(f.apply("no whitespace") == "no whitespace");
}

TEST_CASE("CensorFilter replaces word with asterisks", "[CensorFilter]") {
    CensorFilter f("cat");
    REQUIRE(f.apply("the cat sat") == "the *** sat");
    REQUIRE(f.apply("no match here") == "no match here");
}

TEST_CASE("SqueezeSpacesFilter collapses runs of spaces", "[SqueezeSpacesFilter]") {
    SqueezeSpacesFilter f;
    REQUIRE(f.apply("a   b") == "a b");
    REQUIRE(f.apply("a b") == "a b");
}

TEST_CASE("apply_filters applies filters in order via TextFilter pointers", "[apply_filters]") {
    UppercaseFilter up;
    TrimFilter trim;
    std::vector<const TextFilter*> filters{&trim, &up};
    REQUIRE(apply_filters("  hello  ", filters) == "HELLO");
}

TEST_CASE("apply_twice applies a filter twice via template", "[apply_twice]") {
    SqueezeSpacesFilter f;
    REQUIRE(apply_twice("a     b", f) == "a b");
}
