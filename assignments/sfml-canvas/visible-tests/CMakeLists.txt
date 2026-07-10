cmake_minimum_required(VERSION 3.16)
project(sfml-canvasVisibleTests CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# SUBMISSION_DIR can be passed on the command line:
#   cmake .. -DSUBMISSION_DIR=/path/to/your/submission
# It must contain both canvas.hpp and canvas.cpp.
if(NOT DEFINED SUBMISSION_DIR)
    set(SUBMISSION_DIR "${CMAKE_SOURCE_DIR}/..")
endif()

find_package(SFML 2.5 COMPONENTS graphics system REQUIRED)

include(FetchContent)
FetchContent_Declare(
    Catch2
    GIT_REPOSITORY https://github.com/catchorg/Catch2.git
    GIT_TAG        v3.5.2
)
FetchContent_MakeAvailable(Catch2)

add_executable(sfml-canvas_tests
    test_catch.cpp
    "${SUBMISSION_DIR}/canvas.cpp"
)
target_include_directories(sfml-canvas_tests PRIVATE "${SUBMISSION_DIR}")
target_link_libraries(sfml-canvas_tests PRIVATE Catch2::Catch2WithMain sfml-graphics sfml-system)
target_compile_options(sfml-canvas_tests PRIVATE -Wall -Wextra -g)
