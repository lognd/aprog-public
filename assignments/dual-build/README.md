# Dual Build

A small C++ library ships with a header and implementation file. Your job is
to write two build configurations for it -- one using Make, one using CMake --
and understand why the two tools approach the problem differently.

## What you are building

The library provides three number-theory functions declared in `stats.h`.
A test program in `test_stats.cpp` calls each function and prints
`All tests passed.` when everything works. You do not write or modify any of
these files. You write only `Makefile` and `CMakeLists.txt`.

## What to submit

- `Makefile`
- `CMakeLists.txt`

Do not submit `stats.h`, `stats.cpp`, or `test_stats.cpp`. The grader injects
them automatically.

---

## Part 1 -- Makefile

Write a `Makefile` that satisfies all of the following.

### Targets

| Target | Behavior |
|--------|----------|
| `test_stats` | Default target. Compiles and links the test binary. |
| `test` | Runs `./test_stats`. |
| `clean` | Removes all compiled object files and the binary. |

### Rules

Write a separate compile rule for each `.o` file. Each rule must:

- Use the automatic variable `$@` for the target name.
- Use the automatic variable `$<` for the first prerequisite.
- List every file that, if changed, should trigger a rebuild. For a `.cpp`
  that `#include`s `stats.h`, both files are prerequisites.

### Variables

Define a `CXXFLAGS` variable and use it in every compilation command. At
minimum it should enable `-std=c++17`.

### Phony targets

Declare `.PHONY` for any target that is not a real file.

### Why this matters

Make decides whether to rebuild a target by comparing timestamps. If a
prerequisite is newer than the target, the target is rebuilt. If you omit
`stats.h` from the prerequisite list of `stats.o`, editing `stats.h` and
running `make` will silently produce a stale binary -- the kind of bug that
disappears on a clean build and returns the moment someone edits a header.

---

## Part 2 -- CMakeLists.txt

Write a `CMakeLists.txt` at the root of the submission directory that
satisfies the following.

### Requirements

1. Declare `cmake_minimum_required` and `project`.
2. Build `stats.cpp` as a static library named `stats`.
3. Expose the current source directory as a public include path on the
   `stats` target so that consumers can `#include "stats.h"` without
   specifying a path.
4. Build `test_stats.cpp` as an executable named `test_stats`.
5. Link `test_stats` against the `stats` library.
6. Enable CMake testing (`enable_testing`) and register the test binary as
   a test (`add_test`).

### Why this matters

CMake is declarative: you describe what to build and how targets relate to
each other, not how to invoke the compiler. The `target_link_libraries` and
`target_include_directories` calls propagate include paths and flags
automatically. CMake turns the description into build commands appropriate
for the platform and generator -- Makefiles on Linux, Ninja files if
requested, project files on Windows.

---

## Checking your work locally

The `visible-tests/check.sh` script runs both builds and reports pass/fail
for each stage. Run it from the project root (the directory containing your
`Makefile` and `CMakeLists.txt`):

    bash visible-tests/check.sh

The script requires `make`, `cmake`, and `g++` to be available.

---

## Grading

| Component | Points |
|-----------|--------|
| Makefile builds and test passes | 20 |
| Incremental rebuild after `touch stats.h` | 15 |
| Parallel build (`make -j4`) succeeds | 5 |
| Makefile structure (automatic vars, CXXFLAGS, header dep, .PHONY, no spurious rebuilds) | 25 |
| CMake builds and test passes | 35 |
| **Total** | **100** |
