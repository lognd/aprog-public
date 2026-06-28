cmake_minimum_required(VERSION 3.14)
project(pointer-matrix-visible-tests)

set(CMAKE_CXX_STANDARD 17)

if(NOT DEFINED SUBMISSION_DIR)
    set(SUBMISSION_DIR "${CMAKE_SOURCE_DIR}/../assets")
endif()

find_package(Catch2 REQUIRED)

add_executable(pointer-matrix_tests
    test_visible.cpp
    ${SUBMISSION_DIR}/matrix.cpp
)
target_include_directories(pointer-matrix_tests PRIVATE ${SUBMISSION_DIR})
target_link_libraries(pointer-matrix_tests PRIVATE Catch2::Catch2)
