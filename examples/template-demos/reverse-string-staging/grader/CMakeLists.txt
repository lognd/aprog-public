cmake_minimum_required(VERSION 3.16)
project(reverse-stringGrader CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# After InjectStudentIntoStaff runs, reverse-string.cpp lives alongside
# this CMakeLists.txt. The student binary is built from the injected file.
add_executable(reverse-string
    "${CMAKE_SOURCE_DIR}/reverse-string.cpp"
)
target_compile_options(reverse-string PRIVATE -Wall -Wextra -g)