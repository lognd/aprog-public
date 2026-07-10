// Binary Bounds -- implement every function in this file.
// Rules:
//   - Mark every function inline.
//   - Do not use exceptions (throw/try/catch) anywhere in this file.
//   - Do not use std::lower_bound, std::upper_bound, std::binary_search,
//     or std::equal_range anywhere in this file -- implement the bound
//     logic yourself. (See the README for why.)
//   - `v` is always already sorted in ascending order for every function
//     below. None of these functions sort anything themselves.
#pragma once

#include <vector>

namespace bbounds {

// Scans `v` front to back and returns the index of the FIRST element that
// equals `x`, or -1 if no element equals `x`. This is the O(n) baseline --
// it does not assume `v` is sorted, even though every caller in this
// assignment happens to pass a sorted vector. Empty input -> -1.
inline long linear_search(const std::vector<int>& v, int x) {
    // TODO
    return -1;
}

// Returns the index of SOME element equal to `x` in the sorted vector `v`,
// or -1 if `x` is not present. If `x` appears more than once, any one of
// the matching indices is an acceptable return value. Must run in
// O(log n) time. Empty input -> -1.
inline long binary_search_idx(const std::vector<int>& v, int x) {
    // TODO
    return -1;
}

// Returns the index of the FIRST (lowest-index) element equal to `x` in
// the sorted vector `v`, or -1 if `x` is not present. Must run in
// O(log n) time. Empty input -> -1.
inline long first_occurrence(const std::vector<int>& v, int x) {
    // TODO
    return -1;
}

// Returns the index of the LAST (highest-index) element equal to `x` in
// the sorted vector `v`, or -1 if `x` is not present. Must run in
// O(log n) time. Empty input -> -1.
inline long last_occurrence(const std::vector<int>& v, int x) {
    // TODO
    return -1;
}

// Returns how many elements of the sorted vector `v` equal `x`. Must run
// in O(log n) time (build this from first_occurrence/last_occurrence --
// do not scan). Empty input, or `x` not present -> 0.
inline long count_of(const std::vector<int>& v, int x) {
    // TODO
    return 0;
}

// Returns the index `x` would need to be inserted at to keep the sorted
// vector `v` still sorted (the position of the first element that is NOT
// less than `x`; if `x` is already present, this is the same index
// first_occurrence would return). Must run in O(log n) time. Works for
// values not present in `v` too, including values smaller than every
// element (returns 0) or larger than every element (returns v.size()).
// Empty input -> 0.
inline long insert_position(const std::vector<int>& v, int x) {
    // TODO
    return 0;
}

} // namespace bbounds
