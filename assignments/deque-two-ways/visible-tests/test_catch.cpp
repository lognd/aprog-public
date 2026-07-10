// Visible Catch2 test suite for deque-two-ways.
//
// Compile and run locally:
//   mkdir build && cd build
//   cmake .. -DSUBMISSION_DIR=<path-to-your-submission>
//   cmake --build .
//   ./deque-two-ways_tests

#include <catch2/catch_test_macros.hpp>
#include <string>
#include <utility>

#include "array_deque.hpp"
#include "list_deque.hpp"
#include "stack_queue.hpp"

// ---------------------------------------------------------------------------
// ArrayDeque
// ---------------------------------------------------------------------------

TEST_CASE("ArrayDeque default-constructed is empty", "[ArrayDeque]") {
    ArrayDeque<int> d;
    REQUIRE(d.empty());
    REQUIRE(d.size() == 0);
}

TEST_CASE("ArrayDeque push_back appends in order", "[ArrayDeque]") {
    ArrayDeque<int> d;
    d.push_back(10);
    d.push_back(20);
    d.push_back(30);
    REQUIRE(d.size() == 3);
    REQUIRE(d.front() == 10);
    REQUIRE(d.back() == 30);
}

TEST_CASE("ArrayDeque push_front inserts at the head", "[ArrayDeque]") {
    ArrayDeque<int> d;
    d.push_back(20);
    d.push_front(10);
    REQUIRE(d.size() == 2);
    REQUIRE(d.front() == 10);
    REQUIRE(d.back() == 20);
}

TEST_CASE("ArrayDeque pop_front and pop_back remove correctly", "[ArrayDeque]") {
    ArrayDeque<int> d;
    d.push_back(1);
    d.push_back(2);
    d.push_back(3);
    REQUIRE(d.pop_front());
    REQUIRE(d.front() == 2);
    REQUIRE(d.pop_back());
    REQUIRE(d.back() == 2);
    REQUIRE(d.size() == 1);
}

TEST_CASE("ArrayDeque pop on empty returns false", "[ArrayDeque]") {
    ArrayDeque<int> d;
    REQUIRE_FALSE(d.pop_front());
    REQUIRE_FALSE(d.pop_back());
}

TEST_CASE("ArrayDeque grows capacity when full", "[ArrayDeque]") {
    ArrayDeque<int> d;
    std::size_t first_cap = d.capacity();
    for (int i = 0; i < 100; ++i) {
        d.push_back(i);
    }
    REQUIRE(d.size() == 100);
    REQUIRE(d.capacity() >= 100);
    REQUIRE(d.capacity() != first_cap);
    REQUIRE(d.front() == 0);
    REQUIRE(d.back() == 99);
}

TEST_CASE("ArrayDeque copy constructor deep copies", "[ArrayDeque]") {
    ArrayDeque<int> a;
    a.push_back(1);
    a.push_back(2);
    ArrayDeque<int> b(a);
    b.push_back(3);
    REQUIRE(a.size() == 2);
    REQUIRE(b.size() == 3);
}

TEST_CASE("ArrayDeque move constructor empties the source", "[ArrayDeque]") {
    ArrayDeque<int> a;
    a.push_back(1);
    a.push_back(2);
    ArrayDeque<int> b(std::move(a));
    REQUIRE(b.size() == 2);
    REQUIRE(a.size() == 0);
    REQUIRE(a.empty());
}

// ---------------------------------------------------------------------------
// ListDeque
// ---------------------------------------------------------------------------

TEST_CASE("ListDeque default-constructed is empty", "[ListDeque]") {
    ListDeque<int> d;
    REQUIRE(d.empty());
    REQUIRE(d.size() == 0);
}

TEST_CASE("ListDeque push_back/push_front/pop_back/pop_front", "[ListDeque]") {
    ListDeque<int> d;
    d.push_back(10);
    d.push_front(5);
    d.push_back(20);
    REQUIRE(d.front() == 5);
    REQUIRE(d.back() == 20);
    REQUIRE(d.pop_front());
    REQUIRE(d.front() == 10);
    REQUIRE(d.pop_back());
    REQUIRE(d.back() == 10);
    REQUIRE(d.size() == 1);
}

TEST_CASE("ListDeque copy constructor deep copies", "[ListDeque]") {
    ListDeque<std::string> a;
    a.push_back("x");
    a.push_back("y");
    ListDeque<std::string> b(a);
    b.push_back("z");
    REQUIRE(a.size() == 2);
    REQUIRE(b.size() == 3);
}

// ---------------------------------------------------------------------------
// Stack / Queue adapters
// ---------------------------------------------------------------------------

TEST_CASE("Stack is LIFO over ArrayDeque", "[Stack]") {
    Stack<int> s;
    s.push(1);
    s.push(2);
    s.push(3);
    REQUIRE(s.top() == 3);
    REQUIRE(s.pop());
    REQUIRE(s.top() == 2);
    REQUIRE(s.size() == 2);
}

TEST_CASE("Queue is FIFO over ArrayDeque", "[Queue]") {
    Queue<int> q;
    q.push(1);
    q.push(2);
    q.push(3);
    REQUIRE(q.front() == 1);
    REQUIRE(q.pop());
    REQUIRE(q.front() == 2);
    REQUIRE(q.back() == 3);
    REQUIRE(q.size() == 2);
}
