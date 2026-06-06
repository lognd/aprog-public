// Visible tests for parse_csv.
// Build: g++ -std=c++17 -o test visible-tests/test_csv_parser.cpp && ./test
// Do not modify this file.

#include "../assets/csv_parser.hpp"
#include <cassert>
#include <iostream>

static int passed = 0;
static int failed = 0;

#define CHECK(cond) do { \
    if (cond) { ++passed; } \
    else { ++failed; std::cerr << "FAIL: " #cond " (line " << __LINE__ << ")\n"; } \
} while (0)

// ── basic parsing ─────────────────────────────────────────────────────────────

void test_simple_row() {
    auto rows = parse_csv("a,b,c");
    CHECK(rows.size() == 1);
    CHECK(rows[0].size() == 3);
    CHECK(rows[0][0] == "a");
    CHECK(rows[0][1] == "b");
    CHECK(rows[0][2] == "c");
}

void test_two_rows() {
    auto rows = parse_csv("x,y\n1,2");
    CHECK(rows.size() == 2);
    CHECK(rows[1][0] == "1");
    CHECK(rows[1][1] == "2");
}

void test_crlf_line_endings() {
    auto rows = parse_csv("a,b\r\nc,d");
    CHECK(rows.size() == 2);
    CHECK(rows[1][0] == "c");
    CHECK(rows[1][1] == "d");
}

// ── quoted fields ─────────────────────────────────────────────────────────────

void test_quoted_field_with_comma() {
    auto rows = parse_csv("a,\"b,c\",d");
    CHECK(rows[0].size() == 3);
    CHECK(rows[0][1] == "b,c");
}

void test_escaped_quote_in_quoted_field() {
    // RFC 4180: "" inside a quoted field is a literal "
    auto rows = parse_csv("a,\"say \"\"hi\"\"\",b");
    CHECK(rows[0][1] == "say \"hi\"");
}

void test_quoted_field_with_newline() {
    // A quoted field may contain a literal newline
    auto rows = parse_csv("a,\"line1\nline2\",b");
    CHECK(rows[0].size() == 3);
    CHECK(rows[0][1] == "line1\nline2");
}

// ── missing and empty fields ──────────────────────────────────────────────────

void test_empty_field_in_middle() {
    auto rows = parse_csv("a,,b");
    CHECK(rows[0].size() == 3);
    CHECK(rows[0][1] == "");
}

void test_trailing_comma() {
    auto rows = parse_csv("a,b,");
    CHECK(rows[0].size() == 3);
    CHECK(rows[0][2] == "");
}

void test_empty_line_produces_empty_row() {
    auto rows = parse_csv("a,b\n\nc,d");
    CHECK(rows.size() == 3);
    CHECK(rows[1].size() == 0);
}

// ── multi-row example ─────────────────────────────────────────────────────────

void test_readme_example() {
    const std::string csv =
        "Name,City,Score\n"
        "Alice,\"Portland, OR\",92\n"
        "Bob,\"Said \"\"hi\"\"\",88\n"
        "Carol,,75";

    auto rows = parse_csv(csv);
    CHECK(rows.size() == 4);
    CHECK(rows[0][0] == "Name");
    CHECK(rows[1][1] == "Portland, OR");
    CHECK(rows[2][1] == "Said \"hi\"");
    CHECK(rows[3][1] == "");
    CHECK(rows[3][2] == "75");
}

int main() {
    test_simple_row();
    test_two_rows();
    test_crlf_line_endings();
    test_quoted_field_with_comma();
    test_escaped_quote_in_quoted_field();
    test_quoted_field_with_newline();
    test_empty_field_in_middle();
    test_trailing_comma();
    test_empty_line_produces_empty_row();
    test_readme_example();

    std::cout << passed << " passed, " << failed << " failed.\n";
    return (failed == 0) ? 0 : 1;
}
