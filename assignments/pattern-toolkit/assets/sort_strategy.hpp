// Pattern Toolkit -- Part 1: the Strategy pattern.
//
// A SortStrategy is a policy object that answers one question: "should a
// come before b?" A single sort function, sort_with, delegates every
// comparison to whichever strategy it is handed, so the same sort produces
// different orders depending on the strategy object -- all decided at
// runtime through virtual dispatch.
//
// Rules:
//   - Do not use `new`, `delete`, or `throw` anywhere in this file.
//   - Do not modify the signatures below.
#pragma once

#include <cstdlib>
#include <vector>

namespace pt {

// Comparison policy for sorting ints. before(a, b) returns true when a
// should be ordered before b. Concrete strategies define the ordering.
class SortStrategy {
public:
    virtual ~SortStrategy() = default;
    virtual bool before(int a, int b) const = 0;
};

// Orders ints in increasing numeric value: before(a, b) == (a < b).
class Ascending : public SortStrategy {
public:
    bool before(int a, int b) const override {
        // TODO
        return false;
    }
};

// Orders ints in decreasing numeric value: before(a, b) == (a > b).
class Descending : public SortStrategy {
public:
    bool before(int a, int b) const override {
        // TODO
        return false;
    }
};

// Orders ints by absolute value, smaller magnitude first. When two values
// have the same absolute value (for example -3 and 3), the tie is broken by
// actual ascending value, so -3 comes before 3.
class ByAbsoluteValue : public SortStrategy {
public:
    bool before(int a, int b) const override {
        // TODO
        return false;
    }
};

// Sorts v in place so that for every adjacent pair the strategy's before()
// holds. Every comparison must be delegated to strategy.before(a, b) --
// sort_with must not hardcode any ordering of its own. The sort is not
// required to be stable.
inline void sort_with(std::vector<int>& v, const SortStrategy& strategy) {
    // TODO
    (void)v;
    (void)strategy;
}

} // namespace pt
