// visible-tests/test_visible.cpp
// These tests use the same harness as your test_stats.cpp.
// Build (from your project root): g++ -std=c++17 -I include -I src \
//     visible-tests/test_visible.cpp src/statslib/stats.cpp -o test_visible
// Run:   ./test_visible

#include "../src/testing_harness/harness.hpp"
#include "../include/stats.hpp"
#include <vector>

TEST_CASE("mean -- integers") {
    CHECK_CLOSE(stats::mean({1.0, 2.0, 3.0, 4.0, 5.0}), 3.0, 1e-9);
}

TEST_CASE("median -- odd count sorted") {
    CHECK_CLOSE(stats::median({1.0, 2.0, 3.0}), 2.0, 1e-9);
}

TEST_CASE("median -- even count") {
    CHECK_CLOSE(stats::median({1.0, 2.0, 3.0, 4.0}), 2.5, 1e-9);
}

TEST_CASE("mode -- single mode") {
    std::vector<double> m = stats::mode({1.0, 2.0, 2.0, 3.0});
    CHECK(m.size() == 1);
    CHECK_CLOSE(m[0], 2.0, 1e-9);
}

TEST_CASE("minimum and maximum") {
    CHECK_CLOSE(stats::minimum({3.0, 1.0, 4.0}), 1.0, 1e-9);
    CHECK_CLOSE(stats::maximum({3.0, 1.0, 4.0}), 4.0, 1e-9);
}

int main() { return RUN_ALL_TESTS(); }
