#include <catch2/catch_test_macros.hpp>
#include "html_parser.hpp"

TEST_CASE("to_text: strips a simple bold tag", "[visible]") {
    REQUIRE(to_text("<b>hello</b>") == "hello");
}

TEST_CASE("to_text: passes plain text unchanged", "[visible]") {
    REQUIRE(to_text("hello world") == "hello world");
}

TEST_CASE("to_text: br becomes newline", "[visible]") {
    REQUIRE(to_text("a<br>b") == "a\nb");
}

TEST_CASE("to_text: empty string", "[visible]") {
    REQUIRE(to_text("") == "");
}

TEST_CASE("count_tag: basic count", "[visible]") {
    REQUIRE(count_tag("<b>hello</b>", "b") == 1);
}

TEST_CASE("count_tag: absent tag returns zero", "[visible]") {
    REQUIRE(count_tag("<i>hello</i>", "b") == 0);
}
