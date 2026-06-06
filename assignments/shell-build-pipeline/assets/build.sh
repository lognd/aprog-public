#!/bin/bash
# Shell Build Pipeline
#
# TODO: implement a staged, incremental build.
#
# The project contains three translation units:
#   main.cpp    greet.cpp    math_utils.cpp
#
# Each must pass through four stages in order:
#
#   Stage 1 -- Preprocess:  g++ -E  <source.cpp>  -o <source.i>
#   Stage 2 -- Compile:     g++ -S  <source.i>    -o <source.s>
#   Stage 3 -- Assemble:    g++ -c  <source.s>    -o <source.o>
#   Stage 4 -- Link:        g++     main.o greet.o math_utils.o  -o program
#
# Requirements:
#   1. Only run a stage if the input is NEWER than the output (or the output
#      does not yet exist).  Use:  [ input -nt output ]
#   2. Redirect all compiler error output to build.log.
#      Use 2>build.log (first stage) or 2>>build.log (subsequent stages).
#   3. Use at least one pipe -- for example, count or inspect preprocessed
#      lines before committing them to disk.
#
# When done, running ./program should print:
#   Hello, world!
#   answer: 42
#   passphrase: STAGES_COMPLETE
