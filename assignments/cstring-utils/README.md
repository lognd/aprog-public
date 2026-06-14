# Cstring Utils

TODO: describe this assignment.

## Problem Statement

TODO: Describe the data structure or algorithm the student must implement.

## Interface

The starter file `cstring-utils.hpp` declares the interface you must implement:

```cpp
// FILL IN: show the key interface here.
```

## Requirements

- TODO: list behavioral requirements (e.g., no STL containers, manage memory manually).

## Grading

| Component              | Points |
|------------------------|--------|
| Compilation            | 0 (required) |
| Visible tests (Catch2) | 60     |
| Hidden tests (Catch2)  | 45     |
| Memory safety          | 20     |
| Manual I/O cases       | 25     |
| Extra credit           | +15    |

## Submission

Submit a single file named `cstring-utils.hpp` that implements the
declared interface. Do not rename the file.

## Local Testing

Students can compile and run the visible Catch2 test suite directly:

```bash
mkdir build && cd build
cmake .. -DSUBMISSION_DIR=<path-to-your-submission>
cmake --build .
./cstring-utils_tests
```