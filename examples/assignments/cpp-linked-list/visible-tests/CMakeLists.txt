cmake_minimum_required(VERSION 3.16)
project(LinkedListTests CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# ---------------------------------------------------------------------------
# Catch2  --  fetched automatically; no system install required.
# ---------------------------------------------------------------------------
include(FetchContent)
FetchContent_Declare(
    Catch2
    GIT_REPOSITORY https://github.com/catchorg/Catch2.git
    GIT_TAG        v3.5.2
)
FetchContent_MakeAvailable(Catch2)

# ---------------------------------------------------------------------------
# The student submission directory is injected by the grader as
# -DSUBMISSION_DIR=<path>.  Fall back to the repo root for local use.
# ---------------------------------------------------------------------------
if(NOT DEFINED SUBMISSION_DIR)
    set(SUBMISSION_DIR "${CMAKE_SOURCE_DIR}/..")
endif()

add_executable(linked_list_tests test_catch.cpp)
target_include_directories(linked_list_tests PRIVATE "${SUBMISSION_DIR}")
target_link_libraries(linked_list_tests PRIVATE Catch2::Catch2WithMain)
target_compile_options(linked_list_tests PRIVATE -Wall -Wextra -g)
