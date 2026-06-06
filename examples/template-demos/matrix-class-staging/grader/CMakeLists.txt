cmake_minimum_required(VERSION 3.16)
project(matrix-classGrader CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)
FetchContent_Declare(
    Catch2
    GIT_REPOSITORY https://github.com/catchorg/Catch2.git
    GIT_TAG        v3.5.2
)
FetchContent_MakeAvailable(Catch2)

# After InjectStudentIntoStaff, matrix-class.hpp and .cpp are in the grader dir.

add_executable(matrix-class_tests
    "${CMAKE_SOURCE_DIR}/visible-tests/test_catch.cpp"
    "${CMAKE_SOURCE_DIR}/matrix-class.cpp"
)
target_include_directories(matrix-class_tests PRIVATE "${CMAKE_SOURCE_DIR}")
target_link_libraries(matrix-class_tests PRIVATE Catch2::Catch2WithMain)
target_compile_options(matrix-class_tests PRIVATE -Wall -Wextra -g)

add_executable(matrix-class_hidden_tests
    "${CMAKE_SOURCE_DIR}/hidden-tests/test_hidden.cpp"
    "${CMAKE_SOURCE_DIR}/matrix-class.cpp"
)
target_include_directories(matrix-class_hidden_tests PRIVATE "${CMAKE_SOURCE_DIR}")
target_link_libraries(matrix-class_hidden_tests PRIVATE Catch2::Catch2WithMain)
target_compile_options(matrix-class_hidden_tests PRIVATE -Wall -Wextra -g)