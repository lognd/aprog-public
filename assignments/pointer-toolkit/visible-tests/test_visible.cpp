// Visible tests for pointer-toolkit.
// Compile: g++ -std=c++17 -I.. -o tests test_visible.cpp ../pointer_toolkit.cpp
// Run:     ./tests
#include "../pointer_toolkit.hpp"
#include <cassert>
#include <cstring>
#include <iostream>

static int passed = 0;
static int failed = 0;

#define CHECK(expr) do { \
    if (expr) { ++passed; } \
    else { ++failed; std::cerr << "FAIL: " #expr " (line " << __LINE__ << ")\n"; } \
} while(0)

int main() {
    // reverse
    {
        int arr[] = {1, 2, 3, 4, 5};
        ptk::reverse(arr, 5);
        CHECK(arr[0] == 5 && arr[4] == 1 && arr[2] == 3);
    }

    // find
    {
        int arr[] = {10, 20, 30};
        const int* p = ptk::find(arr, 3, 20);
        CHECK(p != nullptr && *p == 20);
        CHECK(ptk::find(arr, 3, 99) == nullptr);
    }

    // copy_ints
    {
        int src[] = {7, 8, 9};
        int dst[3] = {};
        ptk::copy_ints(dst, src, 3);
        CHECK(dst[0] == 7 && dst[1] == 8 && dst[2] == 9);
    }

    // str_len
    {
        CHECK(ptk::str_len("hello") == 5);
        CHECK(ptk::str_len("") == 0);
    }

    // str_copy
    {
        char buf[20];
        ptk::str_copy(buf, "world");
        CHECK(std::strcmp(buf, "world") == 0);
    }

    // str_compare
    {
        CHECK(ptk::str_compare("abc", "abc") == 0);
        CHECK(ptk::str_compare("abc", "abd") < 0);
        CHECK(ptk::str_compare("abd", "abc") > 0);
    }

    // str_reverse
    {
        char s[] = "hello";
        ptk::str_reverse(s);
        CHECK(std::strcmp(s, "olleh") == 0);
    }

    // str_find_char
    {
        CHECK(ptk::str_find_char("hello", 'l') != nullptr);
        CHECK(ptk::str_find_char("hello", 'z') == nullptr);
    }

    std::cout << passed << " check(s) passed";
    if (failed) std::cerr << "\n" << failed << " check(s) FAILED\n";
    else std::cout << "\n";
    return failed ? 1 : 0;
}
