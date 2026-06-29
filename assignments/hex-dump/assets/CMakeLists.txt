cmake_minimum_required(VERSION 3.14)
project(hexdump CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(hexdump hexdump.cpp)

target_compile_options(hexdump PRIVATE
    -Wall
    -Wextra
    -Wpedantic
)
