cmake_minimum_required(VERSION 3.16)
project(linked-list-iteratorsVisibleTests CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# SUBMISSION_DIR can be passed on the command line:
#   cmake .. -DSUBMISSION_DIR=/path/to/your/submission
if(NOT DEFINED SUBMISSION_DIR)
    set(SUBMISSION_DIR "${CMAKE_SOURCE_DIR}/..")
endif()

include(FetchContent)
FetchContent_Declare(
    Catch2
    GIT_REPOSITORY https://github.com/catchorg/Catch2.git
    GIT_TAG        v3.5.2
)
FetchContent_MakeAvailable(Catch2)

add_executable(linked-list-iterators_tests test_catch.cpp)
target_include_directories(linked-list-iterators_tests PRIVATE "${SUBMISSION_DIR}")
target_link_libraries(linked-list-iterators_tests PRIVATE Catch2::Catch2WithMain)
target_compile_options(linked-list-iterators_tests PRIVATE -Wall -Wextra -g)
