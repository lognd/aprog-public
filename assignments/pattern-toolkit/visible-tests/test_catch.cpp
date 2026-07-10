// Visible Catch2 test suite for Pattern Toolkit.
//
// Compile and run locally:
//   mkdir build && cd build
//   cmake .. -DSUBMISSION_DIR=<path-to-your-submission>
//   cmake --build .
//   ./pattern-toolkit_tests

#include <catch2/catch_test_macros.hpp>
#include <vector>

#include "report_generator.hpp"
#include "sort_strategy.hpp"
#include "thermometer.hpp"

using namespace pt;

TEST_CASE("Ascending sorts in increasing order", "[strategy]") {
    std::vector<int> v{3, 1, 2, -5, 4};
    Ascending strat;
    sort_with(v, strat);
    REQUIRE(v == std::vector<int>{-5, 1, 2, 3, 4});
}

TEST_CASE("Descending sorts in decreasing order", "[strategy]") {
    std::vector<int> v{3, 1, 2, -5, 4};
    Descending strat;
    sort_with(v, strat);
    REQUIRE(v == std::vector<int>{4, 3, 2, 1, -5});
}

TEST_CASE("ByAbsoluteValue sorts by magnitude with ascending tie-break", "[strategy]") {
    std::vector<int> v{3, -3, 1, -2};
    ByAbsoluteValue strat;
    sort_with(v, strat);
    REQUIRE(v == std::vector<int>{1, -2, -3, 3});
}

TEST_CASE("HighAlarm counts temperatures above its threshold", "[observer]") {
    Thermometer t;
    HighAlarm alarm(100.0);
    t.attach(&alarm);
    t.set_temperature(50.0);
    t.set_temperature(150.0);
    t.set_temperature(200.0);
    REQUIRE(alarm.count() == 2);
}

TEST_CASE("TemperatureLog records every temperature in order", "[observer]") {
    Thermometer t;
    TemperatureLog log;
    t.attach(&log);
    t.set_temperature(1.0);
    t.set_temperature(2.0);
    t.set_temperature(3.0);
    REQUIRE(log.values() == std::vector<double>{1.0, 2.0, 3.0});
}

TEST_CASE("SalesReport::generate assembles header, body, footer", "[template-method]") {
    SalesReport report;
    REQUIRE(report.generate() ==
            "=== Sales Report ===\n"
            "Total Sales: $1000\n"
            "--- End of Report ---\n");
}
