// Visible Catch2 test suite for unique-ptr-from-scratch.
//
// Compile and run locally:
//   mkdir build && cd build
//   cmake .. -DSUBMISSION_DIR=<path-to-your-submission>
//   cmake --build .
//   ./unique-ptr-from-scratch_tests

#include <catch2/catch_test_macros.hpp>
#include <utility>
#include <vector>

#include "my_unique_ptr.hpp"
#include "std_smart_pointers.hpp"

TEST_CASE("MyUniquePtr basic ownership: get and bool", "[MyUniquePtr]") {
    MyUniquePtr<int> empty;
    REQUIRE(empty.get() == nullptr);
    REQUIRE(static_cast<bool>(empty) == false);

    MyUniquePtr<int> owning(new int(42));
    REQUIRE(owning.get() != nullptr);
    REQUIRE(*owning.get() == 42);
    REQUIRE(static_cast<bool>(owning) == true);
}

TEST_CASE("MyUniquePtr operator* and operator->", "[MyUniquePtr]") {
    struct Point { int x; int y; };

    MyUniquePtr<Point> p(new Point{3, 4});
    REQUIRE((*p).x == 3);
    REQUIRE(p->y == 4);

    p->x = 10;
    REQUIRE((*p).x == 10);
}

TEST_CASE("MyUniquePtr move constructor transfers ownership", "[MyUniquePtr]") {
    MyUniquePtr<int> a(new int(7));
    int* raw = a.get();

    MyUniquePtr<int> b(std::move(a));
    REQUIRE(b.get() == raw);
    REQUIRE(*b == 7);
    REQUIRE(a.get() == nullptr);
}

TEST_CASE("MyUniquePtr move assignment releases old and steals new", "[MyUniquePtr]") {
    MyUniquePtr<int> a(new int(1));
    MyUniquePtr<int> b(new int(2));
    int* raw_a = a.get();

    b = std::move(a);
    REQUIRE(b.get() == raw_a);
    REQUIRE(*b == 1);
    REQUIRE(a.get() == nullptr);
}

TEST_CASE("MyUniquePtr release relinquishes ownership", "[MyUniquePtr]") {
    MyUniquePtr<int> p(new int(99));
    int* raw = p.release();

    REQUIRE(p.get() == nullptr);
    REQUIRE(static_cast<bool>(p) == false);
    REQUIRE(*raw == 99);
    delete raw; // caller now owns it -- must clean up manually
}

TEST_CASE("MyUniquePtr reset replaces owned pointer", "[MyUniquePtr]") {
    MyUniquePtr<int> p(new int(1));
    p.reset(new int(2));
    REQUIRE(*p == 2);

    p.reset();
    REQUIRE(p.get() == nullptr);
    REQUIRE(static_cast<bool>(p) == false);
}

TEST_CASE("std smart pointer functions: make_shape and total_area", "[std_smart_pointers]") {
    std::vector<std::unique_ptr<Shape>> shapes;
    shapes.push_back(make_shape("circle", 1.0));
    shapes.push_back(make_shape("square", 2.0));

    REQUIRE(shapes[0] != nullptr);
    REQUIRE(shapes[1] != nullptr);

    double total = total_area(shapes);
    REQUIRE(total > 0.0);

    REQUIRE(make_shape("triangle", 1.0) == nullptr);
}
