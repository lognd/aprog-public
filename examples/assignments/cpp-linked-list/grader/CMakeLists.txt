cmake_minimum_required(VERSION 3.16)
project(LinkedListGrader CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# ---------------------------------------------------------------------------
# Catch2  --  fetched from GitHub during setup (not per-submission).
# cmake is installed via setup.sh before any student code runs.
# ---------------------------------------------------------------------------
include(FetchContent)
FetchContent_Declare(
    Catch2
    GIT_REPOSITORY https://github.com/catchorg/Catch2.git
    GIT_TAG        v3.5.2
)
FetchContent_MakeAvailable(Catch2)

# ---------------------------------------------------------------------------
# After InjectStudentIntoStaff runs, linked_list.hpp lives alongside this
# CMakeLists.txt. All targets include the grader directory.
# ---------------------------------------------------------------------------

# Catch2 visible test suite (distributed to students for local use)
add_executable(linked_list_tests
    "${CMAKE_SOURCE_DIR}/../visible-tests/test_catch.cpp"
)
target_include_directories(linked_list_tests PRIVATE "${CMAKE_SOURCE_DIR}")
target_link_libraries(linked_list_tests PRIVATE Catch2::Catch2WithMain)
target_compile_options(linked_list_tests PRIVATE -Wall -Wextra -g)

# Catch2 hidden test suite (staff-only, not visible to students)
add_executable(linked_list_hidden_tests
    "${CMAKE_SOURCE_DIR}/../hidden-tests/test_hidden.cpp"
)
target_include_directories(linked_list_hidden_tests PRIVATE "${CMAKE_SOURCE_DIR}")
target_link_libraries(linked_list_hidden_tests PRIVATE Catch2::Catch2WithMain)
target_compile_options(linked_list_hidden_tests PRIVATE -Wall -Wextra -g)

# Student driver binary (includes linked_list.hpp from grader/ after injection)
add_executable(linked_list
    "${CMAKE_SOURCE_DIR}/main.cpp"
)
target_include_directories(linked_list PRIVATE "${CMAKE_SOURCE_DIR}")
target_compile_options(linked_list PRIVATE -Wall -Wextra -g)

# Staff reference binary (includes the staff solution from hidden-tests/)
# Compiled at grading time so no pre-built binary needs to be committed.
add_executable(reference
    "${CMAKE_SOURCE_DIR}/main.cpp"
)
target_include_directories(reference PRIVATE "${CMAKE_SOURCE_DIR}/../hidden-tests")
target_compile_options(reference PRIVATE -O2)
