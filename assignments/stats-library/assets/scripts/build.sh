#!/usr/bin/env bash
# Configures and builds the project from the repository root.
set -e
mkdir -p build
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
