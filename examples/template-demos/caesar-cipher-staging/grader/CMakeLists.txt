cmake_minimum_required(VERSION 3.16)
project(caesar-cipherGrader C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

# After InjectStudentIntoStaff runs, caesar-cipher.c lives here.
add_executable(caesar-cipher
    "${CMAKE_SOURCE_DIR}/caesar-cipher.c"
)
target_compile_options(caesar-cipher PRIVATE -Wall -Wextra -g)