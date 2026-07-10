// Parse With Grace -- implement every function in this file.
//
// This assignment is the payoff for a whole course of sentinel-return and
// bool/optional-return contracts: here, you use REAL exceptions
// (throw/try/catch) to report parsing failures, with types and messages
// specified exactly in README.md.
//
// Rules:
//   - Mark every function inline.
//   - Do NOT use std::stoi, std::stol, std::strtol, or atoi anywhere in
//     this file -- implement digit parsing yourself.
//   - what() messages must match README.md EXACTLY (tests check them).
#pragma once

#include <stdexcept>
#include <string>
#include <vector>

namespace pwg {

// A minimal fraction type: just the two fields, no reduction required.
struct Fraction {
    long long numerator;
    long long denominator;
};

// Parses `s` as a base-10 integer (optional leading '+'/'-', optional
// surrounding whitespace) and range-checks it against int's range.
// Throws std::invalid_argument on a malformed string, std::out_of_range if
// the value does not fit in an int. See README.md for exact message text.
inline int parse_int(const std::string& s) {
    (void)s;
    // TODO
    return 0;
}

// Parses "a/b" into a Fraction. Throws std::invalid_argument if the string
// is not exactly two integers separated by a single '/', and
// std::domain_error if the denominator parses to exactly zero.
inline Fraction parse_fraction(const std::string& s) {
    (void)s;
    // TODO
    return Fraction{0, 1};
}

// Splits `s` on `sep`, parsing each piece with parse_int. Any exception
// thrown by parse_int for a single element must PROPAGATE UNCHANGED (same
// type, same what() message) -- do not catch, wrap, or rewrap it.
inline std::vector<int> parse_int_list(const std::string& s, char sep) {
    (void)s;
    (void)sep;
    // TODO
    return {};
}

// Parses `s` with parse_int; if parse_int throws, catches it and returns
// `fallback` instead. This function MUST use try/catch itself.
inline int parse_int_or(const std::string& s, int fallback) {
    (void)s;
    (void)fallback;
    // TODO
    return fallback;
}

// RAII counter: increments `tally` on construction, decrements it on
// destruction -- including when destruction happens because an exception
// is unwinding the stack through a ScopedTally.
class ScopedTally {
public:
    explicit ScopedTally(int& tally) : tally_(tally) {
        // TODO
        (void)tally_;
    }

    ~ScopedTally() {
        // TODO
    }

    ScopedTally(const ScopedTally&) = delete;
    ScopedTally& operator=(const ScopedTally&) = delete;

private:
    int& tally_;
};

}  // namespace pwg
