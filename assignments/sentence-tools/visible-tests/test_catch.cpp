// Visible Catch2 test suite for Sentence Tools.
//
// Compile and run locally:
//   mkdir build && cd build
//   cmake .. -DSUBMISSION_DIR=<path-to-your-submission>
//   cmake --build .
//   ./sentence-tools_tests

#include <catch2/catch_test_macros.hpp>
#include "sentence_tools.hpp"

using namespace stools;

TEST_CASE("word_count basic", "[word_count]") {
    REQUIRE(word_count("hello world") == 2);
    REQUIRE(word_count("one") == 1);
    REQUIRE(word_count("") == 0);
}

TEST_CASE("word_at basic", "[word_at]") {
    char buf[32];
    REQUIRE(word_at("hello world", 1, buf, sizeof(buf)) == true);
    REQUIRE(strcmp(buf, "world") == 0);

    REQUIRE(word_at("hello world", 0, buf, sizeof(buf)) == true);
    REQUIRE(strcmp(buf, "hello") == 0);
}

TEST_CASE("contains_word basic", "[contains_word]") {
    REQUIRE(contains_word("the cat sat", "cat") == true);
    REQUIRE(contains_word("the cat sat", "dog") == false);
}

TEST_CASE("trim basic", "[trim]") {
    char s1[] = "  hello  ";
    trim(s1);
    REQUIRE(strcmp(s1, "hello") == 0);

    char s2[] = "  hello   world  ";
    trim(s2);
    REQUIRE(strcmp(s2, "hello   world") == 0);
}

TEST_CASE("capitalize_words basic", "[capitalize_words]") {
    char s[] = "hello world";
    capitalize_words(s);
    REQUIRE(strcmp(s, "Hello World") == 0);
}

TEST_CASE("to_lower basic", "[to_lower]") {
    char s[] = "HELLO World";
    to_lower(s);
    REQUIRE(strcmp(s, "hello world") == 0);
}
