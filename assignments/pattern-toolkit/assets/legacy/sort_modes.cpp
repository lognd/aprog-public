// Pattern Toolkit -- legacy reference material, NOT graded, do not submit.
//
// This file shows how sort_numbers actually grew over two years of "just
// add one more mode" requests. Read it, then compare it to the Strategy
// pattern you are asked to implement in sort_strategy.hpp.
//
// History, as it really happened:
//   2022: original version only ever sorted ascending. One loop, one job.
//   2023: added DESCENDING for the finance team, who wanted top-down
//         leaderboards. Easiest fix: copy the loop, flip the comparison.
//   2024: added ABS for the physics module -- copy of the ascending loop
//         with std::abs sprinkled in. Nobody noticed the tie-break for
//         equal magnitudes was inconsistent with the sort_strategy.hpp spec
//         until a student found it during grading.
//
// Every mode below is a full copy of a simple insertion sort with one
// comparison changed. That is the whole bug: the algorithm is duplicated
// three times, so every future mode means writing (and maintaining) a
// fourth copy.

#include <cstdlib>
#include <vector>

enum SortMode {
    ASCENDING,
    DESCENDING,
    ABS,
};

// Sorts v in place according to mode. Compiles and works correctly for all
// three modes -- that is the problem: it works, and it is still bad code.
void sort_numbers(std::vector<int>& v, SortMode mode) {
    switch (mode) {
        case ASCENDING: {
            // 2022: the original. Plain insertion sort, ascending order.
            for (std::size_t i = 1; i < v.size(); ++i) {
                int key = v[i];
                std::size_t j = i;
                while (j > 0 && v[j - 1] > key) {
                    v[j] = v[j - 1];
                    --j;
                }
                v[j] = key;
            }
            break;
        }
        case DESCENDING: {
            // 2023: added DESCENDING for the finance team.
            // Same loop as ASCENDING, comparison flipped. Copy-pasted from
            // the block above because "it was faster than refactoring."
            for (std::size_t i = 1; i < v.size(); ++i) {
                int key = v[i];
                std::size_t j = i;
                while (j > 0 && v[j - 1] < key) {
                    v[j] = v[j - 1];
                    --j;
                }
                v[j] = key;
            }
            break;
        }
        case ABS: {
            // 2024: added ABS for the physics module -- copy of the
            // ascending loop with std::abs sprinkled in.
            // TODO: marketing wants a "reverse ABS" mode too, but that means
            // copying this block again. There has to be a better way.
            for (std::size_t i = 1; i < v.size(); ++i) {
                int key = v[i];
                std::size_t j = i;
                while (j > 0 && std::abs(v[j - 1]) > std::abs(key)) {
                    v[j] = v[j - 1];
                    --j;
                }
                v[j] = key;
            }
            break;
        }
    }
}
