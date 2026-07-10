#include <catch2/catch_test_macros.hpp>
#include "fraction.hpp"

TEST_CASE("default constructor is 0/1", "[visible]") {
    Fraction f;
    REQUIRE(f.num() == 0);
    REQUIRE(f.den() == 1);
}

TEST_CASE("single-int constructor", "[visible]") {
    Fraction f(5);
    REQUIRE(f.num() == 5);
    REQUIRE(f.den() == 1);
}

TEST_CASE("two-arg constructor reduces to lowest terms", "[visible]") {
    Fraction f(4, 8);
    REQUIRE(f.num() == 1);
    REQUIRE(f.den() == 2);
}

TEST_CASE("two-arg constructor normalizes sign onto numerator", "[visible]") {
    Fraction f(3, -4);
    REQUIRE(f.num() == -3);
    REQUIRE(f.den() == 4);
}

TEST_CASE("plus adds two fractions", "[visible]") {
    Fraction a(1, 2);
    Fraction b(1, 3);
    Fraction c = a.plus(b);
    REQUIRE(c.num() == 5);
    REQUIRE(c.den() == 6);
}

TEST_CASE("times multiplies two fractions", "[visible]") {
    Fraction a(2, 3);
    Fraction b(3, 4);
    Fraction c = a.times(b);
    REQUIRE(c.num() == 1);
    REQUIRE(c.den() == 2);
}

TEST_CASE("equals compares reduced values", "[visible]") {
    Fraction a(2, 4);
    Fraction b(1, 2);
    REQUIRE(a.equals(b));
}

TEST_CASE("lessThan orders fractions correctly", "[visible]") {
    Fraction a(1, 3);
    Fraction b(1, 2);
    REQUIRE(a.lessThan(b));
    REQUIRE_FALSE(b.lessThan(a));
}

TEST_CASE("to_string renders whole numbers without a denominator", "[visible]") {
    Fraction f(6, 2);
    REQUIRE(f.to_string() == "3");
}

TEST_CASE("to_string renders reduced fractions", "[visible]") {
    Fraction f(3, 4);
    REQUIRE(f.to_string() == "3/4");
}
