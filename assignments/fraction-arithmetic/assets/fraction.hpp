// Fraction Arithmetic -- starter header.
//
// Fraction encapsulates a rational number and maintains three invariants at
// all times, regardless of which constructor or arithmetic method was used
// to produce a given instance:
//
//   1. The fraction is always stored in lowest terms (numerator and
//      denominator share no common factor greater than 1).
//   2. The denominator is always strictly positive. Sign lives entirely in
//      the numerator (e.g. -3/4 is stored as numerator=-3, denominator=4 --
//      never numerator=3, denominator=-4).
//   3. The value zero is always normalized to 0/1.
//
// Contract: passing denominator == 0 to the two-argument constructor, or
// calling dividedBy() with a Fraction whose value is zero, is a precondition
// violation. Behavior is unspecified in that case (this mirrors the
// documented-precondition convention used elsewhere in this course, e.g.
// peano-math's successor/add/multiply/exponentiate contracts). Well-behaved
// callers -- and every hidden test -- never do this.
//
// Do not modify this file. Implement every declared method in fraction.cpp.
#pragma once

#include <string>

class Fraction {
public:
    // Constructs 0/1.
    Fraction();

    // Constructs n/1.
    Fraction(int n);

    // Constructs numerator/denominator, reduced to lowest terms with the
    // sign normalized onto the numerator.
    // Precondition: denominator != 0.
    Fraction(int numerator, int denominator);

    // Returns the (possibly negative) numerator of the reduced fraction.
    int num() const;

    // Returns the (always positive) denominator of the reduced fraction.
    int den() const;

    // Returns a new Fraction equal to *this + other.
    Fraction plus(const Fraction& other) const;

    // Returns a new Fraction equal to *this - other.
    Fraction minus(const Fraction& other) const;

    // Returns a new Fraction equal to *this * other.
    Fraction times(const Fraction& other) const;

    // Returns a new Fraction equal to *this / other.
    // Precondition: other.num() != 0.
    Fraction dividedBy(const Fraction& other) const;

    // Returns true if *this and other represent the same rational value.
    bool equals(const Fraction& other) const;

    // Returns true if *this < other.
    bool lessThan(const Fraction& other) const;

    // Renders the fraction as "3/4", or "-3/4" when negative, or "5"
    // (no "/1") when the reduced denominator is 1, including "0" for zero.
    std::string to_string() const;

private:
    int numerator_;
    int denominator_;
};
