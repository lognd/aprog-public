// Visible Catch2 test suite for LinkedList<T>.
//
// Students can compile and run this locally:
//   mkdir build && cd build
//   cmake .. -DSUBMISSION_DIR=<path-to-your-submission>
//   cmake --build .
//   ./linked_list_tests
//
// The grader runs all of these cases and shows results immediately.

#include <catch2/catch_test_macros.hpp>
#include <sstream>
#include "linked_list.hpp"

// ---------------------------------------------------------------------------
// push_back / size / empty
// ---------------------------------------------------------------------------

TEST_CASE("empty list has size 0", "[basic]") {
    LinkedList<int> lst;
    REQUIRE(lst.size() == 0);
    REQUIRE(lst.empty());
}

TEST_CASE("push_back increases size", "[basic]") {
    LinkedList<int> lst;
    lst.push_back(1);
    REQUIRE(lst.size() == 1);
    REQUIRE_FALSE(lst.empty());
    lst.push_back(2);
    REQUIRE(lst.size() == 2);
}

TEST_CASE("front and back after push_back", "[basic]") {
    LinkedList<int> lst;
    lst.push_back(10);
    lst.push_back(20);
    lst.push_back(30);
    REQUIRE(lst.front() == 10);
    REQUIRE(lst.back() == 30);
}

// ---------------------------------------------------------------------------
// push_front
// ---------------------------------------------------------------------------

TEST_CASE("push_front prepends correctly", "[basic]") {
    LinkedList<int> lst;
    lst.push_back(2);
    lst.push_front(1);
    REQUIRE(lst.front() == 1);
    REQUIRE(lst.back() == 2);
    REQUIRE(lst.size() == 2);
}

// ---------------------------------------------------------------------------
// pop_front
// ---------------------------------------------------------------------------

TEST_CASE("pop_front on single element leaves empty list", "[pop]") {
    LinkedList<int> lst;
    lst.push_back(42);
    lst.pop_front();
    REQUIRE(lst.empty());
}

TEST_CASE("pop_front on multiple elements", "[pop]") {
    LinkedList<int> lst;
    lst.push_back(1);
    lst.push_back(2);
    lst.push_back(3);
    lst.pop_front();
    REQUIRE(lst.front() == 2);
    REQUIRE(lst.size() == 2);
}

TEST_CASE("pop_front on empty list is a no-op", "[pop]") {
    LinkedList<int> lst;
    REQUIRE_NOTHROW(lst.pop_front());
    REQUIRE(lst.empty());
}

// ---------------------------------------------------------------------------
// pop_back
// ---------------------------------------------------------------------------

TEST_CASE("pop_back on single element leaves empty list", "[pop]") {
    LinkedList<int> lst;
    lst.push_back(7);
    lst.pop_back();
    REQUIRE(lst.empty());
}

TEST_CASE("pop_back removes the tail", "[pop]") {
    LinkedList<int> lst;
    lst.push_back(1);
    lst.push_back(2);
    lst.push_back(3);
    lst.pop_back();
    REQUIRE(lst.back() == 2);
    REQUIRE(lst.size() == 2);
}

TEST_CASE("pop_back on empty list is a no-op", "[pop]") {
    LinkedList<int> lst;
    REQUIRE_NOTHROW(lst.pop_back());
}

// ---------------------------------------------------------------------------
// print
// ---------------------------------------------------------------------------

TEST_CASE("print produces space-separated output with trailing newline", "[print]") {
    LinkedList<int> lst;
    lst.push_back(1);
    lst.push_back(2);
    lst.push_back(3);

    // Redirect cout to a string buffer to capture print() output.
    std::ostringstream oss;
    std::streambuf* old = std::cout.rdbuf(oss.rdbuf());
    lst.print();
    std::cout.rdbuf(old);

    REQUIRE(oss.str() == "1 2 3\n");
}

// ---------------------------------------------------------------------------
// Copy constructor
// ---------------------------------------------------------------------------

TEST_CASE("copy constructor creates an independent deep copy", "[copy]") {
    LinkedList<int> original;
    original.push_back(1);
    original.push_back(2);
    original.push_back(3);

    LinkedList<int> copy = original;
    REQUIRE(copy.size() == 3);
    REQUIRE(copy.front() == 1);
    REQUIRE(copy.back() == 3);

    // Mutating the copy must not affect the original.
    copy.push_back(99);
    REQUIRE(original.size() == 3);
    REQUIRE(copy.size() == 4);
}
