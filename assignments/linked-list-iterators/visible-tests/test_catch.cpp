// Visible Catch2 test suite for linked-list-iterators.
//
// Compile and run locally:
//   mkdir build && cd build
//   cmake .. -DSUBMISSION_DIR=<path-to-your-submission>
//   cmake --build .
//   ./linked-list-iterators_tests

#include <catch2/catch_test_macros.hpp>
#include <string>

#include "linked_list.hpp"

TEST_CASE("empty list: begin() == end()", "[Iterator]") {
    LinkedList<int> list;
    REQUIRE(list.begin() == list.end());
}

TEST_CASE("range-for sums every element in order", "[Iterator]") {
    LinkedList<int> list;
    list.push_back(1);
    list.push_back(2);
    list.push_back(3);
    int sum = 0;
    for (int x : list) {
        sum += x;
    }
    REQUIRE(sum == 6);
}

TEST_CASE("manual begin()/end() loop visits every element", "[Iterator]") {
    LinkedList<int> list;
    list.push_back(10);
    list.push_back(20);
    list.push_back(30);
    int count = 0;
    int sum = 0;
    for (auto it = list.begin(); it != list.end(); ++it) {
        sum += *it;
        ++count;
    }
    REQUIRE(count == 3);
    REQUIRE(sum == 60);
}

TEST_CASE("prefix ++ advances and returns the new position", "[Iterator]") {
    LinkedList<int> list;
    list.push_back(1);
    list.push_back(2);
    auto it = list.begin();
    auto& ref = ++it;
    REQUIRE(*it == 2);
    REQUIRE(*ref == 2);
    REQUIRE(&ref == &it);
}

TEST_CASE("postfix ++ returns the OLD position, then advances", "[Iterator]") {
    LinkedList<int> list;
    list.push_back(1);
    list.push_back(2);
    list.push_back(3);
    auto it = list.begin();
    auto old = it++;
    REQUIRE(*old == 1);
    REQUIRE(*it == 2);
}

TEST_CASE("operator-> accesses members through the iterator", "[Iterator]") {
    LinkedList<std::string> list;
    list.push_back("cat");
    list.push_back("elephant");
    auto it = list.begin();
    REQUIRE(it->size() == 3);
    ++it;
    REQUIRE(it->size() == 8);
}

TEST_CASE("iterator equality and inequality", "[Iterator]") {
    LinkedList<int> list;
    list.push_back(1);
    auto a = list.begin();
    auto b = list.begin();
    REQUIRE(a == b);
    ++b;
    REQUIRE(a != b);
    REQUIRE(b == list.end());
}

TEST_CASE("find_it returns an iterator to the first match", "[Iterator]") {
    LinkedList<int> list;
    list.push_back(5);
    list.push_back(10);
    list.push_back(15);
    auto it = list.find_it(10);
    REQUIRE(it != list.end());
    REQUIRE(*it == 10);
}

TEST_CASE("find_it returns end() when the value is absent", "[Iterator]") {
    LinkedList<int> list;
    list.push_back(1);
    list.push_back(2);
    REQUIRE(list.find_it(99) == list.end());
}

TEST_CASE("insert_after inserts a value right after the given position", "[Iterator]") {
    LinkedList<int> list;
    list.push_back(1);
    list.push_back(3);
    auto it = list.find_it(1);
    bool ok = list.insert_after(it, 2);
    REQUIRE(ok);
    REQUIRE(list.size() == 3);
    int values[3];
    int i = 0;
    for (int x : list) {
        values[i++] = x;
    }
    REQUIRE(values[0] == 1);
    REQUIRE(values[1] == 2);
    REQUIRE(values[2] == 3);
}

TEST_CASE("erase_after removes the node right after the given position", "[Iterator]") {
    LinkedList<int> list;
    list.push_back(1);
    list.push_back(2);
    list.push_back(3);
    auto it = list.find_it(1);
    bool ok = list.erase_after(it);
    REQUIRE(ok);
    REQUIRE(list.size() == 2);
    REQUIRE(list.front() == 1);
    REQUIRE(list.back() == 3);
}

TEST_CASE("erase_after with nothing after the position is a documented no-op", "[Iterator]") {
    LinkedList<int> list;
    list.push_back(1);
    list.push_back(2);
    auto it = list.find_it(2);   // last element -- nothing after it
    bool ok = list.erase_after(it);
    REQUIRE_FALSE(ok);
    REQUIRE(list.size() == 2);
}

TEST_CASE("const iteration compiles and sums correctly", "[Iterator]") {
    LinkedList<int> list;
    list.push_back(4);
    list.push_back(5);
    list.push_back(6);
    const LinkedList<int>& clist = list;
    int sum = 0;
    for (int x : clist) {
        sum += x;
    }
    REQUIRE(sum == 15);
    int csum = 0;
    for (auto it = list.cbegin(); it != list.cend(); ++it) {
        csum += *it;
    }
    REQUIRE(csum == 15);
}
