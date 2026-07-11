cmake_minimum_required(VERSION 3.14)
project(pointer-matrix-visible-tests)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(NOT DEFINED SUBMISSION_DIR)
    set(SUBMISSION_DIR "${CMAKE_SOURCE_DIR}/../assets")
endif()

include(FetchContent)
FetchContent_Declare(
    Catch2
    GIT_REPOSITORY https://github.com/catchorg/Catch2.git
    GIT_TAG        v3.5.2
)
FetchContent_MakeAvailable(Catch2)

add_executable(pointer-matrix_tests
    test_visible.cpp
    ${SUBMISSION_DIR}/matrix.cpp
)
target_include_directories(pointer-matrix_tests PRIVATE ${SUBMISSION_DIR})
target_link_libraries(pointer-matrix_tests PRIVATE Catch2::Catch2WithMain)
