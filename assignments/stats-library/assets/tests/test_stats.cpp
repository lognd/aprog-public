#include "../src/testing_harness/harness.hpp"
#include "../include/stats.hpp"
#include <vector>

TEST_CASE("mean -- basic") {
    // TODO: add your own test cases
    CHECK_CLOSE(stats::mean({1.0, 2.0, 3.0}), 2.0, 1e-9);
}

// TODO: add TEST_CASE blocks for median, mode, variance, stddev, minimum, maximum, range

int main() { return RUN_ALL_TESTS(); }
