// Visible Catch2 tests for Matrix Class.
#include <catch2/catch_test_macros.hpp>
#include <sstream>
#include "matrix-class.hpp"

TEST_CASE("constructor -- zero initialized", "[matrix]") {
    Matrix m(2, 3);
    REQUIRE(m.rows() == 2);
    REQUIRE(m.cols() == 3);
    REQUIRE(m.at(0, 0) == 0.0);
    REQUIRE(m.at(1, 2) == 0.0);
}

TEST_CASE("at -- read and write", "[matrix]") {
    Matrix m(2, 2);
    m.at(0, 0) = 1.0;
    m.at(0, 1) = 2.0;
    m.at(1, 0) = 3.0;
    m.at(1, 1) = 4.0;
    REQUIRE(m.at(0, 1) == 2.0);
    REQUIRE(m.at(1, 0) == 3.0);
}

TEST_CASE("operator+ -- element-wise add", "[matrix]") {
    Matrix a(2, 2), b(2, 2);
    a.at(0, 0) = 1.0; a.at(0, 1) = 2.0;
    a.at(1, 0) = 3.0; a.at(1, 1) = 4.0;
    b.at(0, 0) = 10.0; b.at(0, 1) = 20.0;
    b.at(1, 0) = 30.0; b.at(1, 1) = 40.0;
    Matrix c = a + b;
    REQUIRE(c.at(0, 0) == 11.0);
    REQUIRE(c.at(1, 1) == 44.0);
}

TEST_CASE("transpose -- 2x3 becomes 3x2", "[matrix]") {
    Matrix m(2, 3);
    m.at(0, 0) = 1; m.at(0, 1) = 2; m.at(0, 2) = 3;
    m.at(1, 0) = 4; m.at(1, 1) = 5; m.at(1, 2) = 6;
    Matrix t = m.transpose();
    REQUIRE(t.rows() == 3);
    REQUIRE(t.cols() == 2);
    REQUIRE(t.at(0, 0) == 1);
    REQUIRE(t.at(2, 1) == 6);
}

TEST_CASE("operator* -- 2x2 identity", "[matrix]") {
    Matrix a(2, 2), I(2, 2);
    a.at(0, 0) = 1; a.at(0, 1) = 2;
    a.at(1, 0) = 3; a.at(1, 1) = 4;
    I.at(0, 0) = 1; I.at(1, 1) = 1;
    Matrix r = a * I;
    REQUIRE(r.at(0, 0) == 1);
    REQUIRE(r.at(1, 1) == 4);
}
