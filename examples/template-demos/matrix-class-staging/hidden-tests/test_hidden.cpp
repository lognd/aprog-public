// Hidden Catch2 tests for Matrix Class.
#include <catch2/catch_test_macros.hpp>
#include <sstream>
#include "matrix-class.hpp"

TEST_CASE("hidden -- copy constructor deep copy", "[matrix][hidden]") {
    Matrix a(2, 2);
    a.at(0, 0) = 5.0;
    Matrix b = a;
    b.at(0, 0) = 99.0;
    REQUIRE(a.at(0, 0) == 5.0);
}

TEST_CASE("hidden -- copy assignment deep copy", "[matrix][hidden]") {
    Matrix a(2, 2), b(2, 2);
    a.at(0, 0) = 7.0;
    b = a;
    b.at(0, 0) = 0.0;
    REQUIRE(a.at(0, 0) == 7.0);
}

TEST_CASE("hidden -- matrix multiply 2x3 * 3x2", "[matrix][hidden]") {
    Matrix a(2, 3), b(3, 2);
    a.at(0,0)=1; a.at(0,1)=2; a.at(0,2)=3;
    a.at(1,0)=4; a.at(1,1)=5; a.at(1,2)=6;
    b.at(0,0)=7;  b.at(0,1)=8;
    b.at(1,0)=9;  b.at(1,1)=10;
    b.at(2,0)=11; b.at(2,1)=12;
    Matrix c = a * b;
    REQUIRE(c.rows() == 2);
    REQUIRE(c.cols() == 2);
    REQUIRE(c.at(0,0) == 58.0);
    REQUIRE(c.at(1,1) == 154.0);
}

TEST_CASE("hidden -- print output", "[matrix][hidden]") {
    Matrix m(2, 2);
    m.at(0,0)=1; m.at(0,1)=2;
    m.at(1,0)=3; m.at(1,1)=4;
    std::ostringstream oss;
    m.print(oss);
    REQUIRE(oss.str() == "1 2\n3 4\n");
}
