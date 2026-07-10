# Study Guide 8: Makefile & CMake

This module goes deep on the two build systems used throughout the course.
Students learn how Make decides what to rebuild (and how to break that by
omitting a header dependency), how to write a multi-target CMake project
from an outline, and finally write both a Makefile and a CMakeLists.txt for
the same library to compare the declarative and procedural approaches
directly.

## Know before you start

- Basic Make and CMake concepts (target, Makefile, CMakeLists.txt)
  [assumed: row 2 -- Environment Setup]
- The four compilation stages and manual `g++` invocation [assumed: row 4
  -- Command-Line & Compilation]

## Taught here

Concept: how Make decides what to rebuild
- Know that `make` compares file timestamps: a target is rebuilt if any of
  its listed prerequisites are newer than the target itself.
- Know that a prerequisite is a file a target depends on; if a file that
  affects the compiled output (like an included header) is not listed as a
  prerequisite, `make` never knows it changed and silently produces a
  stale binary on an incremental build.
- Know that a clean build (`make clean && make`) is always correct because
  it recompiles everything regardless of timestamps -- only incremental
  builds expose a missing-dependency bug.
- Be able to write a Makefile rule with a complete prerequisite list, for
  example `sieve.o: sieve.cpp limits.h`, so that changing a header
  triggers recompilation of every source file that includes it.
- Be able to use the automatic variables `$@` (the target name) and `$<`
  (the first prerequisite) inside a compile recipe.
- Know that a phony target (declared with `.PHONY`) is a Makefile target
  name that does not correspond to a real output file, such as `clean` or
  `test`.
- Be able to define a `CXXFLAGS` variable and reuse it across every
  compilation command in a Makefile.

Concept: CMake project structure
- Know the standard opening boilerplate of a `CMakeLists.txt`:
  `cmake_minimum_required`, `project`, and setting `CMAKE_CXX_STANDARD`.
- Know that `add_library(name STATIC source.cpp)` defines a static library
  target -- a bundle of compiled `.o` files packaged into a single archive
  file (`libname.a` on Linux/macOS) that gets linked into whatever links
  against it.
- Know that `target_include_directories(name PUBLIC path)` makes a path
  available both to the library itself and to anything that links against
  it, while `PRIVATE` restricts it to the library itself only.
- Know that `target_link_libraries(target PRIVATE dep)` links `dep` into
  `target`, and that dependencies propagate transitively: if `text` links
  `math`, then anything linking `text` also gets `math`'s public include
  paths automatically.
- Be able to register tests with `enable_testing()` followed by
  `add_test(NAME ... COMMAND ...)`, and know that `add_test` does not build
  anything -- the executable must already be defined with `add_executable`
  first.
- Know that CMake is declarative (you describe what to build and how
  targets relate) while Make is procedural (you describe the literal
  commands to run), and that CMake generates the actual build files
  (Makefiles, Ninja files, IDE project files) for whichever generator it
  targets.
- Know the CMake invocation sequence: `cmake -B build` configures the
  project into a build directory, `cmake --build build` compiles it, and
  `ctest --test-dir build` runs the registered tests.

## Study checklist

- [ ] Explain why an incremental build can silently go stale after editing
      a header, and how to fix the Makefile that allows it.
- [ ] Write a Makefile compile rule using `$@` and `$<`.
- [ ] Explain the difference between `PUBLIC` and `PRIVATE` in
      `target_include_directories`.
- [ ] Explain why `add_test` requires a prior `add_executable` call.
- [ ] Contrast Make's procedural approach with CMake's declarative approach
      in your own words.

## Practiced in

`stale-build`, `cmake-heist`, `dual-build`
