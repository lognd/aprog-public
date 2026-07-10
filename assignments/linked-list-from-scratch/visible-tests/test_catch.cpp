// Visible Catch2 test suite for linked-list-from-scratch.
//
// Compile and run locally:
//   mkdir build && cd build
//   cmake .. -DSUBMISSION_DIR=<path-to-your-submission>
//   cmake --build .
//   ./linked-list-from-scratch_tests

#include <catch2/catch_test_macros.hpp>
#include <string>
#include <utility>

#include "linked_list.hpp"

TEST_CASE("default-constructed list is empty", "[LinkedList]") {
    LinkedList<int> list;
    REQUIRE(list.empty());
    REQUIRE(list.size() == 0);
}

TEST_CASE("push_back appends in order", "[LinkedList]") {
    LinkedList<int> list;
    list.push_back(10);
    list.push_back(20);
    list.push_back(30);
    REQUIRE(list.size() == 3);
    REQUIRE(list.front() == 10);
    REQUIRE(list.back() == 30);
}

TEST_CASE("push_front inserts at the head", "[LinkedList]") {
    LinkedList<int> list;
    list.push_back(20);
    list.push_front(10);
    REQUIRE(list.size() == 2);
    REQUIRE(list.front() == 10);
    REQUIRE(list.back() == 20);
}

TEST_CASE("insert_at inserts in the middle", "[LinkedList]") {
    LinkedList<int> list;
    list.push_back(10);
    list.push_back(20);
    list.push_back(40);
    REQUIRE(list.insert_at(2, 30));
    REQUIRE(list.size() == 4);
    REQUIRE(list.find(30) == 2);
}

TEST_CASE("insert_at at index == size appends", "[LinkedList]") {
    LinkedList<int> list;
    list.push_back(1);
    REQUIRE(list.insert_at(1, 2));
    REQUIRE(list.back() == 2);
}

TEST_CASE("insert_at out of range returns false", "[LinkedList]") {
    LinkedList<int> list;
    list.push_back(1);
    REQUIRE_FALSE(list.insert_at(5, 99));
    REQUIRE(list.size() == 1);
}

TEST_CASE("remove_at removes and relinks", "[LinkedList]") {
    LinkedList<int> list;
    list.push_back(10);
    list.push_back(20);
    list.push_back(30);
    REQUIRE(list.remove_at(1));
    REQUIRE(list.size() == 2);
    REQUIRE(list.front() == 10);
    REQUIRE(list.back() == 30);
}

TEST_CASE("remove_at on empty list returns false", "[LinkedList]") {
    LinkedList<int> list;
    REQUIRE_FALSE(list.remove_at(0));
}

TEST_CASE("find returns -1 when absent", "[LinkedList]") {
    LinkedList<int> list;
    list.push_back(1);
    list.push_back(2);
    REQUIRE(list.find(99) == -1);
    REQUIRE(list.find(2) == 1);
}

TEST_CASE("copy constructor deep copies", "[LinkedList]") {
    LinkedList<int> a;
    a.push_back(1);
    a.push_back(2);
    LinkedList<int> b(a);
    b.push_back(3);
    REQUIRE(a.size() == 2);
    REQUIRE(b.size() == 3);
}

TEST_CASE("move constructor empties the source", "[LinkedList]") {
    LinkedList<int> a;
    a.push_back(1);
    a.push_back(2);
    LinkedList<int> b(std::move(a));
    REQUIRE(b.size() == 2);
    REQUIRE(a.size() == 0);
    REQUIRE(a.empty());
}

TEST_CASE("clear empties the list and it stays usable", "[LinkedList]") {
    LinkedList<std::string> list;
    list.push_back("a");
    list.push_back("b");
    list.clear();
    REQUIRE(list.empty());
    list.push_back("c");
    REQUIRE(list.size() == 1);
    REQUIRE(list.front() == "c");
}

TEST_CASE("LinkedList works with a non-trivial element type", "[LinkedList]") {
    LinkedList<std::string> list;
    list.push_back("hello");
    list.push_front("world");
    REQUIRE(list.front() == "world");
    REQUIRE(list.back() == "hello");
}
