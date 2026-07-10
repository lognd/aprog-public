cmake_minimum_required(VERSION 3.16)
project(media-libraryVisibleTests CXX)

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

add_executable(media-library_tests
    test_catch.cpp
    "${SUBMISSION_DIR}/media-library.cpp"
)
target_include_directories(media-library_tests PRIVATE "${SUBMISSION_DIR}")
target_link_libraries(media-library_tests PRIVATE Catch2::Catch2WithMain)
target_compile_options(media-library_tests PRIVATE -Wall -Wextra -g)
