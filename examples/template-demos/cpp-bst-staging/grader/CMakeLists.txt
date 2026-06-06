cmake_minimum_required(VERSION 3.16)
project(cpp-bstGrader CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# ---------------------------------------------------------------------------
# Catch2 -- fetched from GitHub during setup, not per-submission.
# ---------------------------------------------------------------------------
include(FetchContent)
FetchContent_Declare(
    Catch2
    GIT_REPOSITORY https://github.com/catchorg/Catch2.git
    GIT_TAG        v3.5.2
)
FetchContent_MakeAvailable(Catch2)

# ---------------------------------------------------------------------------
# After InjectStudentIntoStaff runs, cpp-bst.hpp lives alongside
# this CMakeLists.txt. All targets include the grader directory.
# ---------------------------------------------------------------------------

# Catch2 visible test suite (students use this locally too)
add_executable(cpp-bst_tests
    "${CMAKE_SOURCE_DIR}/visible-tests/test_catch.cpp"
)
target_include_directories(cpp-bst_tests PRIVATE "${CMAKE_SOURCE_DIR}")
target_link_libraries(cpp-bst_tests PRIVATE Catch2::Catch2WithMain)
target_compile_options(cpp-bst_tests PRIVATE -Wall -Wextra -g)

# Catch2 hidden test suite (staff only)
add_executable(cpp-bst_hidden_tests
    "${CMAKE_SOURCE_DIR}/hidden-tests/test_hidden.cpp"
)
target_include_directories(cpp-bst_hidden_tests PRIVATE "${CMAKE_SOURCE_DIR}")
target_link_libraries(cpp-bst_hidden_tests PRIVATE Catch2::Catch2WithMain)
target_compile_options(cpp-bst_hidden_tests PRIVATE -Wall -Wextra -g)

# CLI driver -- student's implementation (included from grader/ after injection)
add_executable(cpp-bst
    "${CMAKE_SOURCE_DIR}/main.cpp"
)
target_include_directories(cpp-bst PRIVATE "${CMAKE_SOURCE_DIR}")
target_compile_options(cpp-bst PRIVATE -Wall -Wextra -g)

# CLI driver -- staff reference (included from hidden-tests/)
add_executable(reference
    "${CMAKE_SOURCE_DIR}/main.cpp"
)
target_include_directories(reference PRIVATE "${CMAKE_SOURCE_DIR}/hidden-tests")
target_compile_options(reference PRIVATE -O2)