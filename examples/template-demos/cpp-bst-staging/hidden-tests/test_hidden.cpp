// Hidden Catch2 test suite for BST.
// Not shown to students until after the due date.

#include <catch2/catch_test_macros.hpp>
#include <sstream>
#include "cpp-bst.hpp"

TEST_CASE("hidden -- single element inorder", "[bst][hidden]") {
    BST t;
    t.insert(42);
    std::ostringstream oss;
    t.inorder(oss);
    REQUIRE(oss.str() == "42\n");
}

TEST_CASE("hidden -- insert descending", "[bst][hidden]") {
    BST t;
    for (int i = 10; i >= 1; --i) t.insert(i);
    std::ostringstream oss;
    t.inorder(oss);
    REQUIRE(oss.str() == "1 2 3 4 5 6 7 8 9 10\n");
}

TEST_CASE("hidden -- search after many inserts", "[bst][hidden]") {
    BST t;
    int vals[] = {50, 25, 75, 10, 40, 60, 90};
    for (int v : vals) t.insert(v);
    for (int v : vals) REQUIRE(t.search(v));
    REQUIRE_FALSE(t.search(1));
    REQUIRE_FALSE(t.search(100));
}

TEST_CASE("hidden -- inorder large", "[bst][hidden]") {
    BST t;
    int vals[] = {8, 3, 10, 1, 6, 14, 4, 7, 13};
    for (int v : vals) t.insert(v);
    std::ostringstream oss;
    t.inorder(oss);
    REQUIRE(oss.str() == "1 3 4 6 7 8 10 13 14\n");
}
