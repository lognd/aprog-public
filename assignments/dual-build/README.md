# Dual Build

A small C++ library ships with a header and implementation file. Your job is
to write two build configurations for it -- one using Make, one using CMake --
and understand why the two tools approach the problem differently.

## Learning goals

- Write a Makefile from scratch with correct prerequisite lists (a prerequisite is a file a target depends on -- if it changes, the target must be rebuilt), automatic variables, and phony targets (a phony target is a target name in a Makefile that does not correspond to a real output file, like `clean` or `test`)
- Write a CMakeLists.txt that builds a static library (a bundle of compiled `.o` files that gets copied into any executable that links against it) and links an executable against it
- Understand why Make uses timestamps and what happens when a header is missing from prerequisites
- See how the same build intent is expressed declaratively (CMake) vs procedurally (Make)

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

## Examples at a glance

One scenario, traced against the reference solution: a clean directory
containing `Makefile`, `CMakeLists.txt`, `stats.h`, `stats.cpp`, and
`test_stats.cpp`, with no build artifacts yet.

| Command | What it produces | Why |
|---------|-------------------|-----|
| `make` | `stats.o`, `test_stats.o`, `test_stats` (an executable) in the project root | The default target (`test_stats`) compiles each `.cpp` to a `.o`, then links both `.o` files into the binary |
| `make test` | Runs `./test_stats`, prints `All tests passed.` | `test` is phony -- it has no output file of its own, it just runs the binary that `make` (its own prerequisite) builds first |
| `make clean` | Removes `stats.o`, `test_stats.o`, `test_stats`; nothing else in the directory changes | `clean` only deletes generated files, never the source or the Makefile itself |
| `make` (run again, no edits) | Prints `` 'test_stats' is up to date `` and does nothing | Every target's prerequisite is older than the target, so Make has nothing to redo |
| `touch stats.h && make` | Recompiles BOTH `stats.o` and `test_stats.o`, then relinks `test_stats` | Both `.cpp` files `#include "stats.h"`, and both `.o` rules correctly list `stats.h` as a prerequisite, so Make sees it as newer than both objects |
| `make -j4` (from a clean state) | Same three files as plain `make`, but `stats.o` and `test_stats.o` may compile concurrently | Nothing in the prerequisite graph says one `.o` needs the other, so Make is free to run both compile rules in parallel; only the final link step must wait for both |
| `cmake -B build -DCMAKE_BUILD_TYPE=Release` then `cmake --build build` | `build/libstats.a` (the static library) and `build/test_stats` (the executable), plus CMake's own bookkeeping files (`CMakeCache.txt`, `CMakeFiles/`, etc.) | CMake's configure step writes a generated build system into `build/`; the build step actually invokes the compiler and linker, producing the library first (since `test_stats` links against it) and the executable second |
| `ctest --test-dir build` | `1/1 Test #1: test_stats ... Passed` | `add_test(NAME test_stats COMMAND test_stats)` registers the built executable as a test; `ctest` just runs it and checks the exit code |

All of the rows above were run against the reference `Makefile` and
`CMakeLists.txt` to confirm the exact commands and file names -- see the
worked example below for the full step-by-step trace.

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

  *Example (correct):* `stats.o: stats.cpp stats.h` -- running
  `touch stats.h && make` recompiles `stats.o` (and, since `test_stats.o`
  also lists `stats.h`, recompiles that too, then relinks).
  *Example (the bug this catches):* if the rule instead read
  `stats.o: stats.cpp` (missing `stats.h`), the same
  `touch stats.h && make` prints nothing and rebuilds nothing --
  `make -q` exits `0` ("up to date") even though the header changed. This
  is exactly what the grader's incremental-rebuild check looks for.

### Variables

Define a `CXXFLAGS` variable and use it in every compilation command. At
minimum it should enable `-std=c++17`.

### Phony targets

Declare `.PHONY` for any target that is not a real file. `test` and `clean`
belong there. `test_stats`, `stats.o`, and `test_stats.o` do **not** --
they are real files on disk, and declaring them phony forces Make to
rebuild them on every invocation even when nothing changed. Running `make`
twice in a row with no edits in between should do nothing the second time
(Make prints `` `test_stats' is up to date`` or similar); if it rebuilds
anyway, check your `.PHONY` line first.

*Example:* `.PHONY: test clean` -- with this line, `make` twice in a row
prints `` 'test_stats' is up to date `` on the second run. *Edge case:*
if you instead wrote `.PHONY: test clean test_stats`, every `make`
invocation would relink `test_stats` from scratch even with no source
changes, because Make never trusts a phony target's timestamp.

### Parallel builds

A Makefile with a correct, complete prerequisite list for every rule
already supports `make -j4` with no extra work -- Make uses the
prerequisite graph you wrote to figure out which rules are independent and
can run concurrently. Grading runs `make -j4` as a check (see the table
below); you do not need to add anything beyond what Parts 1's Rules and
Variables sections already ask for.

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
2. Build `stats.cpp` as a static library named `stats` (a static library is a
   bundle of compiled `.o` files that gets copied into any executable that
   links against it, as opposed to a shared/dynamic library that is loaded
   separately at runtime).
3. Expose the current source directory as a public include path on the
   `stats` target so that consumers can `#include "stats.h"` without
   specifying a path.
4. Build `test_stats.cpp` as an executable named `test_stats`.
5. Link `test_stats` against the `stats` library.
6. Enable CMake testing (`enable_testing`) and register the test binary as
   a test (`add_test`).

*Examples, confirmed by actually configuring and building the reference
solution:*

- `cmake -B build && cmake --build build` produces `build/libstats.a`
  (the static library from requirement 2) and `build/test_stats` (the
  executable from requirement 4), with `test_stats` already linked
  against `stats` -- no missing-symbol errors at link time, because
  requirement 5's `target_link_libraries` wired it up.
- *Edge case -- forgetting requirement 3:* if
  `target_include_directories(stats PUBLIC ...)` is omitted,
  `test_stats.cpp`'s `#include "stats.h"` still happens to work in this
  particular layout (everything lives in one flat directory, so the
  compiler's default `.` search path finds it anyway) -- but drop
  `stats.h` into a subdirectory and the build breaks with
  `fatal error: stats.h: No such file or directory` for every consumer
  of the `stats` target, which is exactly the bug requirement 3 exists
  to prevent.
- `cmake -B build -DCMAKE_BUILD_TYPE=Bogus` (an unrecognized build type)
  does not stop the configure step -- CMake accepts any string for
  `CMAKE_BUILD_TYPE` and simply skips adding optimization/debug flags it
  does not recognize a preset for. The build still succeeds and still
  produces `build/libstats.a` and `build/test_stats`; only the compiler
  flags differ from a real `Release` or `Debug` build.
- `ctest --test-dir build` after a successful build prints
  `1/1 Test #1: test_stats ... Passed`, confirming requirement 6's
  `add_test` registration actually runs the binary.

### Why this matters

CMake is declarative: you describe what to build and how targets relate to
each other, not how to invoke the compiler. The `target_link_libraries` and
`target_include_directories` calls propagate include paths and flags
automatically. CMake turns the description into build commands appropriate
for the platform and generator (a generator is the specific tool CMake emits
build instructions for) -- Makefiles on Linux, Ninja files if
requested, project files on Windows.

---

## Worked example: what the build produces, step by step

This traces one exact invocation against the reference solution, starting
from a clean directory containing only `Makefile`, `CMakeLists.txt`,
`stats.h`, `stats.cpp`, and `test_stats.cpp` -- no `.o` files, no `build/`
directory, nothing generated yet.

### `make` (Part 1), from scratch

| Step | Command Make runs | What lands on disk | Why |
|------|--------------------|---------------------|-----|
| 1 | `g++ -std=c++17 -Wall -Wextra -c -o stats.o stats.cpp` | `stats.o` | `test_stats` depends on `stats.o`, which does not exist yet, so Make builds it first, using the `stats.o: stats.cpp stats.h` rule |
| 2 | `g++ -std=c++17 -Wall -Wextra -c -o test_stats.o test_stats.cpp` | `test_stats.o` | Same reasoning, using the `test_stats.o: test_stats.cpp stats.h` rule |
| 3 | `g++ -std=c++17 -Wall -Wextra -o test_stats stats.o test_stats.o` | `test_stats` (an executable) | Both prerequisites of the `test_stats` rule now exist, so Make links them into the final binary |
| 4 (run `make` again) | *(nothing)* | *(unchanged)* | Every target's timestamp is now newer than every prerequisite; Make prints `` 'test_stats' is up to date `` and exits |
| 5 (run `make test`) | `./test_stats` | prints `All tests passed.` to stdout | `test` is phony and lists `test_stats` as a prerequisite, so Make first confirms `test_stats` is current (step 4's check), then runs the program |

### `cmake -B build -DCMAKE_BUILD_TYPE=Release` then `cmake --build build` (Part 2), from the same clean state

| Step | What happens | Why |
|------|---------------|-----|
| 1. Configure (`cmake -B build ...`) | CMake reads `CMakeLists.txt`, detects the C and C++ compilers, and writes a generated build system (a `Makefile`, `CMakeCache.txt`, and the `CMakeFiles/` directory) into `build/` -- nothing is compiled yet | The configure step's only job is turning the declarative `CMakeLists.txt` into concrete build instructions for this platform; on Linux with no `-G` flag, that means a Makefile-based generator |
| 2. Build, target `stats` | Runs `g++` with `-c` on `stats.cpp`, producing `build/CMakeFiles/stats.dir/stats.cpp.o`, then archives it into `build/libstats.a` with `ar` | `add_library(stats STATIC stats.cpp)` declares `stats` as a static library target; CMake builds its dependencies (here, none) before the target itself |
| 3. Build, target `test_stats` | Runs `g++` with `-c` on `test_stats.cpp`, then links the resulting object file against `build/libstats.a` to produce `build/test_stats` | `add_executable(test_stats test_stats.cpp)` plus `target_link_libraries(test_stats PRIVATE stats)` mean `test_stats` cannot link until `stats` exists, so CMake orders the two targets accordingly |
| 4. Run `ctest --test-dir build` | Executes `build/test_stats` and reports `1/1 Test #1: test_stats ... Passed` | `add_test(NAME test_stats COMMAND test_stats)` registered the binary as ctest's one and only test |

End state: `build/libstats.a` (a static library archive) and
`build/test_stats` (an executable already linked against it) both exist,
and `ctest` confirms the executable runs and exits successfully -- the
exact same `All tests passed.` behavior as the Makefile build, produced
by a completely different set of tool invocations.

---

## Checking your work locally

The `visible-tests/check.sh` script exercises every row of the grading
table below -- both builds, the incremental rebuild, the parallel build,
the Makefile structure checks, and the CMake/ctest run -- and reports
pass/fail for each stage. Run it from the project root (the directory
containing your `Makefile` and `CMakeLists.txt`):

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

## Going further

- Add a `compile_commands.json` target to your CMakeLists.txt (set
  `CMAKE_EXPORT_COMPILE_COMMANDS=ON`) and open the project in an IDE that
  uses it. What does the IDE gain from this file?
- Deliberately remove `stats.h` from a prerequisite list, run `make -j4`,
  and watch it still "succeed" with a stale object file -- parallelism
  makes a missing dependency more dangerous, not less, because two rules
  that should have run in a fixed order may now race.
- Look up `cmake --preset` (CMake 3.19+). Write a `CMakePresets.json` that
  defines a debug and a release preset.
