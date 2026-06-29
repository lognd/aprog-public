#include <catch2/catch_test_macros.hpp>
#include "html_parser.hpp"

// -----------------------------------------------------------------------
// to_text -- required test categories
//
// You must have at least one test for EACH category below.
// Add more TEST_CASEs or SECTIONs within categories as you see fit.
// -----------------------------------------------------------------------

TEST_CASE("to_text: empty input", "[to_text][empty]") {
    REQUIRE(to_text("") == "");
}

TEST_CASE("to_text: no tags -- plain text passes through unchanged", "[to_text][plain]") {
    // TODO: test that text with no '<' or '>' is returned as-is
}

TEST_CASE("to_text: single tag pair -- tags stripped, text kept", "[to_text][single]") {
    // TODO: e.g. to_text("<b>hello</b>") == "hello"
}

TEST_CASE("to_text: nested tags", "[to_text][nested]") {
    // TODO: e.g. to_text("<b><i>hi</i></b>") == "hi"
}

TEST_CASE("to_text: br tag becomes newline", "[to_text][br]") {
    // TODO: to_text("a<br>b") == "a\nb"
}

TEST_CASE("to_text: p tag becomes double newline", "[to_text][p]") {
    // TODO: to_text("x<p>y") == "x\n\ny"
}

TEST_CASE("to_text: tag names are case-insensitive", "[to_text][case]") {
    // TODO: <B> should behave the same as <b>
}

TEST_CASE("to_text: unknown tags are stripped silently", "[to_text][unknown]") {
    // TODO: e.g. to_text("<span>hi</span>") == "hi"
}

TEST_CASE("to_text: text before the first tag", "[to_text][prefix]") {
    // TODO: e.g. to_text("hello<b> world</b>") == "hello world"
}

TEST_CASE("to_text: text after the last tag", "[to_text][suffix]") {
    // TODO: e.g. to_text("<b>hello</b> world") == "hello world"
}

TEST_CASE("to_text: adjacent tags with no text between", "[to_text][adjacent]") {
    // TODO: e.g. to_text("<b></b>") == ""
}

TEST_CASE("to_text: multiple br tags", "[to_text][multi-br]") {
    // TODO: e.g. to_text("a<br>b<br>c") == "a\nb\nc"
}

TEST_CASE("to_text: malformed tag -- no closing gt", "[to_text][malformed]") {
    // TODO: to_text("hello <b world") should treat '<' as a literal character
}

// -----------------------------------------------------------------------
// count_tag -- required test categories
// -----------------------------------------------------------------------

TEST_CASE("count_tag: basic count of one open tag", "[count_tag][basic]") {
    // TODO: count_tag("<b>hello</b>", "b") == 1
}

TEST_CASE("count_tag: closing tags are not counted", "[count_tag][close]") {
    // TODO: confirm that </b> does not contribute to the count for "b"
}

TEST_CASE("count_tag: case-insensitive tag name", "[count_tag][case]") {
    // TODO: <B> and <b> both count for tag_name "b"
}

TEST_CASE("count_tag: multiple open tags", "[count_tag][multi]") {
    // TODO: count_tag("<b>x</b><b>y</b>", "b") == 2
}

TEST_CASE("count_tag: tag not present returns zero", "[count_tag][absent]") {
    // TODO: count_tag("<i>text</i>", "b") == 0
}
