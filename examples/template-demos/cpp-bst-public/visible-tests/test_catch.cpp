// Visible Catch2 test suite for BST.
//
// Students can compile and run this locally:
//   mkdir build && cd build
//   cmake .. -DSUBMISSION_DIR=<path-to-your-submission>
//   cmake --build .
//   ./cpp-bst_tests

#include <catch2/catch_test_macros.hpp>
#include <sstream>
#include "cpp-bst.hpp"

TEST_CASE("insert and search -- basic", "[bst]") {
    BST t;
    t.insert(5);
    t.insert(3);
    t.insert(7);
    REQUIRE(t.search(5));
    REQUIRE(t.search(3));
    REQUIRE(t.search(7));
    REQUIRE_FALSE(t.search(4));
}

TEST_CASE("inorder -- sorted output", "[bst]") {
    BST t;
    t.insert(5);
    t.insert(2);
    t.insert(8);
    t.insert(1);
    t.insert(4);
    std::ostringstream oss;
    t.inorder(oss);
    REQUIRE(oss.str() == "1 2 4 5 8\n");
}

TEST_CASE("insert -- duplicates ignored", "[bst]") {
    BST t;
    t.insert(10);
    t.insert(10);
    std::ostringstream oss;
    t.inorder(oss);
    REQUIRE(oss.str() == "10\n");
}

TEST_CASE("empty tree -- search returns false", "[bst]") {
    BST t;
    REQUIRE_FALSE(t.search(0));
}
