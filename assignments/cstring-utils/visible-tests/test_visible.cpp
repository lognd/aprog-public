// Visible tests for cstring-utils.
// Compile: g++ -std=c++17 -I.. -o tests test_visible.cpp ../cstring_utils.cpp
// Run:     ./tests
#include "../cstring_utils.hpp"
#include <cassert>
#include <cstring>
#include <iostream>

static int passed = 0, failed = 0;
#define CHECK(expr) do { \
    if (expr) { ++passed; } \
    else { ++failed; std::cerr << "FAIL: " #expr " (line " << __LINE__ << ")\n"; } \
} while(0)

int main() {
    CHECK(csu::length("hello") == 5);
    CHECK(csu::length("") == 0);

    char buf[30];
    csu::copy(buf, "world");
    CHECK(std::strcmp(buf, "world") == 0);

    csu::copy(buf, "foo");
    csu::append(buf, "bar");
    CHECK(std::strcmp(buf, "foobar") == 0);

    CHECK(csu::compare("abc", "abc") == 0);
    CHECK(csu::compare("abc", "abd") < 0);
    CHECK(csu::compare("abd", "abc") > 0);

    CHECK(csu::find_char("hello", 'l') != nullptr);
    CHECK(*csu::find_char("hello", 'l') == 'l');
    CHECK(csu::find_char("hello", 'z') == nullptr);

    CHECK(csu::find_str("hello world", "world") != nullptr);
    CHECK(csu::find_str("hello", "xyz") == nullptr);

    char s[] = "hello";
    csu::reverse(s);
    CHECK(std::strcmp(s, "olleh") == 0);

    CHECK(csu::is_digits("12345") == true);
    CHECK(csu::is_digits("12a45") == false);
    CHECK(csu::is_digits("") == true);

    char ibuf[12];
    csu::int_to_str(42, ibuf);
    CHECK(std::strcmp(ibuf, "42") == 0);
    csu::int_to_str(0, ibuf);
    CHECK(std::strcmp(ibuf, "0") == 0);

    std::cout << passed << " check(s) passed";
    if (failed) std::cerr << "\n" << failed << " check(s) FAILED\n";
    else std::cout << "\n";
    return failed ? 1 : 0;
}
