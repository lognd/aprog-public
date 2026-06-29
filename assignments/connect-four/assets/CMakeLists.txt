cmake_minimum_required(VERSION 3.16)
project(connect-four CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(connect_four
    main.cpp
    board.cpp
    grid.cpp
)
target_compile_options(connect_four PRIVATE -Wall -Wextra -g)
