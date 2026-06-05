// Hidden Catch2 test suite for LinkedList<T>.
//
// These cases are NOT distributed to students. They run on Gradescope
// and become visible only after the due date.
//
// Compile (done automatically by CMakeBuild via grader/CMakeLists.txt):
//   add_executable(linked_list_hidden_tests
//       "${CMAKE_SOURCE_DIR}/../hidden-tests/test_hidden.cpp")

#include <catch2/catch_test_macros.hpp>
#include <sstream>
#include "linked_list.hpp"

// ---------------------------------------------------------------------------
// Size and empty after mixed operations
// ---------------------------------------------------------------------------

TEST_CASE("size tracks push_back and pop_front correctly", "[hidden][size]") {
    LinkedList<int> lst;
    for (int i = 0; i < 10; ++i) lst.push_back(i);
    REQUIRE(lst.size() == 10);
    for (int i = 0; i < 5; ++i) lst.pop_front();
    REQUIRE(lst.size() == 5);
    for (int i = 0; i < 5; ++i) lst.pop_back();
    REQUIRE(lst.size() == 0);
    REQUIRE(lst.empty());
}

TEST_CASE("size tracks push_front and pop_back correctly", "[hidden][size]") {
    LinkedList<int> lst;
    for (int i = 0; i < 8; ++i) lst.push_front(i);
    REQUIRE(lst.size() == 8);
    for (int i = 0; i < 4; ++i) lst.pop_back();
    REQUIRE(lst.size() == 4);
}

// ---------------------------------------------------------------------------
// Order preservation
// ---------------------------------------------------------------------------

TEST_CASE("push_back then push_front interleaved preserves order", "[hidden][order]") {
    LinkedList<int> lst;
    lst.push_back(3);
    lst.push_back(4);
    lst.push_front(2);
    lst.push_front(1);
    lst.push_back(5);

    std::ostringstream oss;
    lst.print();  // tested via ostringstream redirect below
    REQUIRE(lst.front() == 1);
    REQUIRE(lst.back()  == 5);
    REQUIRE(lst.size()  == 5);
}

TEST_CASE("pop_front restores expected front value", "[hidden][order]") {
    LinkedList<int> lst;
    lst.push_back(10);
    lst.push_back(20);
    lst.push_back(30);
    lst.pop_front();
    REQUIRE(lst.front() == 20);
    lst.pop_front();
    REQUIRE(lst.front() == 30);
    REQUIRE(lst.size()  == 1);
}

TEST_CASE("pop_back restores expected back value", "[hidden][order]") {
    LinkedList<int> lst;
    lst.push_back(10);
    lst.push_back(20);
    lst.push_back(30);
    lst.pop_back();
    REQUIRE(lst.back() == 20);
    lst.pop_back();
    REQUIRE(lst.back() == 10);
    REQUIRE(lst.size() == 1);
}

// ---------------------------------------------------------------------------
// Copy constructor correctness
// ---------------------------------------------------------------------------

TEST_CASE("copy constructor produces same contents", "[hidden][copy]") {
    LinkedList<int> orig;
    orig.push_back(1);
    orig.push_back(2);
    orig.push_back(3);

    LinkedList<int> copy(orig);
    REQUIRE(copy.size()  == orig.size());
    REQUIRE(copy.front() == orig.front());
    REQUIRE(copy.back()  == orig.back());
}

TEST_CASE("mutating copy does not affect original", "[hidden][copy]") {
    LinkedList<int> orig;
    orig.push_back(1);
    orig.push_back(2);
    orig.push_back(3);

    LinkedList<int> copy(orig);
    copy.push_back(99);
    copy.pop_front();

    REQUIRE(orig.size()  == 3);
    REQUIRE(orig.front() == 1);
    REQUIRE(orig.back()  == 3);
}

TEST_CASE("mutating original does not affect copy", "[hidden][copy]") {
    LinkedList<int> orig;
    orig.push_back(7);
    orig.push_back(8);
    orig.push_back(9);

    LinkedList<int> copy(orig);
    orig.pop_back();
    orig.push_front(0);

    REQUIRE(copy.size()  == 3);
    REQUIRE(copy.front() == 7);
    REQUIRE(copy.back()  == 9);
}

// ---------------------------------------------------------------------------
// print output format
// ---------------------------------------------------------------------------

TEST_CASE("print on two-element list is space-separated with newline", "[hidden][print]") {
    std::ostringstream oss;
    std::streambuf* old = std::cout.rdbuf(oss.rdbuf());

    LinkedList<int> lst;
    lst.push_back(42);
    lst.push_back(7);
    lst.print();

    std::cout.rdbuf(old);
    REQUIRE(oss.str() == "42 7\n");
}

TEST_CASE("print on single-element list has no leading/trailing space", "[hidden][print]") {
    std::ostringstream oss;
    std::streambuf* old = std::cout.rdbuf(oss.rdbuf());

    LinkedList<int> lst;
    lst.push_back(99);
    lst.print();

    std::cout.rdbuf(old);
    REQUIRE(oss.str() == "99\n");
}
