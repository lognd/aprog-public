// Sort With Anything -- implement every function/template declared here.
//
// sort_by is your merge sort, generalized: instead of hardcoding a
// comparison (like < ), it takes a Compare argument -- any CALLABLE with
// the signature `bool operator()(const T&, const T&)` (or something the
// compiler can treat that way). The same one template works whether the
// caller passes a free function, a functor (a struct with operator()), or
// a lambda -- sort_by itself never needs to know or care which. That is
// the entire lesson of this assignment: write the algorithm once, and let
// callers plug in any comparison rule they want.
//
// Rules:
//   - Do not use std::sort, std::stable_sort, std::partial_sort, or qsort
//     anywhere in this file -- implement sort_by's merge sort yourself.
//   - Do not use exceptions (throw/try/catch) anywhere in this file.
//   - Do not modify the public signatures below.
#pragma once

#include <cstddef>
#include <string>
#include <vector>

namespace swa {

// Sorts v in place using merge sort, ordering elements according to cmp.
//
// cmp(a, b) must return true if a belongs STRICTLY before b, and follow the
// "strict weak ordering" contract (see the README): consistent (cmp(a, b)
// and cmp(b, a) are never both true), irreflexive (cmp(a, a) is always
// false), and NEVER returns true for two elements you consider equal.
//
// Must be STABLE: two elements that cmp treats as equal (neither cmp(a, b)
// nor cmp(b, a) is true) keep their original relative order.
//
// Compare may be a free function, a functor, or a lambda -- sort_by works
// identically with all three. O(n log n); may allocate an O(n) scratch
// std::vector<T> for the merge step. Empty or single-element v is a
// documented no-op.
template <typename T, typename Compare>
void sort_by(std::vector<T>& v, Compare cmp) {
    // TODO
    (void)v;
    (void)cmp;
}

// FREE FUNCTION comparator: orders strings by ascending length. Ties
// (equal-length strings) are left entirely to sort_by's stability -- this
// function only needs to compare lengths.
inline bool by_length_asc(const std::string& a, const std::string& b) {
    // TODO
    (void)a;
    (void)b;
    return false;
}

// FUNCTOR comparator: orders ints by ascending ABSOLUTE value. On a tie in
// absolute value, the smaller ACTUAL value comes first -- e.g. -3 belongs
// before 3, even though both have absolute value 3, because -3 < 3.
struct ByAbsoluteValue {
    bool operator()(int a, int b) const {
        // TODO
        (void)a;
        (void)b;
        return false;
    }
};

// Returns a NEW vector containing every element of v for which
// keep(element) is true, in original relative order. Does not modify v.
// Pred may be a free function, a functor, or a lambda.
template <typename T, typename Pred>
std::vector<T> filter(const std::vector<T>& v, Pred keep) {
    // TODO
    (void)v;
    (void)keep;
    return {};
}

// Applies f to every element of v IN PLACE: f takes a T& and mutates it
// directly (f does not return a replacement value). F may be a free
// function, a functor, or a lambda.
template <typename T, typename F>
void for_each_apply(std::vector<T>& v, F f) {
    // TODO
    (void)v;
    (void)f;
}

// Returns how many elements of v satisfy pred(element). Does not modify v.
// Empty v -> 0.
template <typename T, typename Pred>
std::size_t count_matching(const std::vector<T>& v, Pred pred) {
    // TODO
    (void)v;
    (void)pred;
    return 0;
}

} // namespace swa
