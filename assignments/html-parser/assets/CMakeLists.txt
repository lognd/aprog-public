cmake_minimum_required(VERSION 3.14)
project(html_parser CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# -----------------------------------------------------------------------
# Fetch Catch2 (the testing framework used in this course's Data Structures track)
# -----------------------------------------------------------------------
include(FetchContent)
FetchContent_Declare(
    Catch2
    GIT_REPOSITORY https://github.com/catchorg/Catch2.git
    GIT_TAG        v3.5.2
)
FetchContent_MakeAvailable(Catch2)

# -----------------------------------------------------------------------
# Your implementation + test suite
# -----------------------------------------------------------------------
add_executable(html_parser_tests
    html_parser.cpp
    tests/test_html_parser.cpp
)

target_include_directories(html_parser_tests PRIVATE ${CMAKE_SOURCE_DIR})
target_link_libraries(html_parser_tests PRIVATE Catch2::Catch2WithMain)
