// Sort Suite -- implement every function in this file.
// Rules:
//   - Mark every function inline.
//   - Do not use exceptions (throw/try/catch) anywhere in this file.
//   - Do not use std::sort, std::stable_sort, std::partial_sort, or qsort
//     anywhere in this file -- implement every algorithm yourself. (See
//     the README for why.)
//   - Every function mutates the vector it is given in place (sorts it
//     directly) except is_sorted_asc, which only reads.
#pragma once

#include <string>
#include <utility>
#include <vector>

namespace sortsuite {

// Sorts `v` ascending using selection sort: repeatedly find the minimum of
// the remaining unsorted region and swap it into place. In-place (no extra
// array needed). Empty or single-element input -> no-op.
inline void selection_sort(std::vector<int>& v) {
    // TODO
    (void)v;
}

// Sorts `v` ascending using insertion sort: build up a sorted prefix one
// element at a time, shifting larger elements right to make room. In-place.
// Empty or single-element input -> no-op.
inline void insertion_sort(std::vector<int>& v) {
    // TODO
    (void)v;
}

// Sorts `v` ascending using merge sort: split in half recursively, sort
// each half, then merge the two sorted halves back together. May use an
// O(n) scratch array (e.g. a std::vector<int> the same size as `v`) for the
// merge step -- this does not need to be in-place. Must run in O(n log n)
// time. Empty or single-element input -> no-op.
inline void merge_sort(std::vector<int>& v) {
    // TODO
    (void)v;
}

// Sorts `v` ascending by .first ONLY, built from the same merge sort logic
// as merge_sort above (may use O(n) scratch space). Must be STABLE: two
// elements with equal .first must keep their original relative order.
// Empty or single-element input -> no-op.
inline void stable_sort_pairs(std::vector<std::pair<int, std::string>>& v) {
    // TODO
    (void)v;
}

// Returns true if `v` is sorted in ascending order (v[i] <= v[i+1] for
// every adjacent pair), false otherwise. An empty vector or a
// single-element vector is always considered sorted -> true.
inline bool is_sorted_asc(const std::vector<int>& v) {
    // TODO
    (void)v;
    return false;
}

} // namespace sortsuite
