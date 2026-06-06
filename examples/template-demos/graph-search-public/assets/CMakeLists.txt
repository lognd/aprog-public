cmake_minimum_required(VERSION 3.16)
project(graph-search CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# FILL IN: add your source files.
add_executable(graph-search main.cpp)
target_compile_options(graph-search PRIVATE -Wall -Wextra -g)