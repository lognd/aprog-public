cmake_minimum_required(VERSION 3.16)
project(statslib)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Library target -- implements the stats functions
add_library(statslib src/statslib/stats.cpp)
target_include_directories(statslib PUBLIC include/)

# Test target -- your test suite; links against statslib
add_executable(stats_tests tests/test_stats.cpp)
target_include_directories(stats_tests PRIVATE src/)
target_link_libraries(stats_tests PRIVATE statslib)
