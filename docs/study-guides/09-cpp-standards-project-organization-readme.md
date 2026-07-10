# Study Guide 9: C++ Standards, Project Organization, README

This module covers three practical facts of life in a real C++ project:
which language standard a piece of code actually requires, what
documentation files every professional project ships, and how a
`CMakeLists.txt` dictates a specific directory layout that source files
must match. It closes with a full multi-target CMake library assignment
that exercises all three together.

## Know before you start

- Reading and writing a `CMakeLists.txt` with `add_library`,
  `add_executable`, and `target_include_directories`
  [assumed: row 8 -- Makefile & CMake]
- Compiling and building a CMake project (`cmake -B build`, `cmake --build
  build`) [assumed: row 8 -- Makefile & CMake]

## Taught here

Concept: C++ standard versions
- Know that the C++ standard has evolved through named versions (C++11,
  C++14, C++17, C++20, ...) and that features added in a later version are
  unavailable when compiling against an earlier one.
- Know that `CMAKE_CXX_STANDARD` is the CMake variable that tells the
  compiler which version of the C++ language spec to compile against.
- Be able to read a compiler error caused by a too-low standard setting as
  a clue, look up the offending feature on cppreference.com, and identify
  the minimum standard version that supports it.
- Know that using a higher-than-necessary standard is not the goal --
  identifying the true minimum required version is the point of the
  exercise.

Concept: standard project documentation files
- Know the purpose of each standard documentation file: README (what the
  project is and how to use it), LICENSE (legal terms for use/copy/modify),
  CHANGELOG (a running log of notable changes between released versions),
  CONTRIBUTORS (credits everyone who worked on the project), CODE_OF_CONDUCT
  (rules for how participants should treat each other), and SECURITY
  (instructions for privately reporting vulnerabilities).
- Know the conventional section headers expected inside a README
  (Description, Installation, Usage, Contributing, License) and a
  CHANGELOG (an `[Unreleased]` section with Added/Changed/Fixed
  subsections), matching this course's own README style guide.
- Know that these file names and locations are standardized across
  open-source projects so that tools, contributors, and platforms like
  GitHub can find them automatically.

Concept: project layout inferred from CMakeLists.txt
- Be able to read a `CMakeLists.txt` and infer the exact directory
  structure it expects from its `add_library`, `add_executable`, and
  `target_include_directories` calls.
- Be able to reorganize a flat pile of source files into that structure
  using `mkdir -p` (create nested directories in one command) and `mv`.
- Know that a locked, unmodifiable `CMakeLists.txt` is a common real-world
  situation: the build description is the source of truth, and source
  files must be moved to match it, not the other way around.

Concept: organizing a multi-target CMake library project
- Be able to implement a small statistics library (mean, median, mode,
  variance, standard deviation, min, max, range) operating on
  `std::vector<double>`.
- Know that population variance/standard deviation divide by n, while
  sample variance/standard deviation divide by n-1, and that a project
  must state explicitly which convention it uses.
- Know that a sentinel value (a special reserved value standing in for "no
  valid answer," such as `std::numeric_limits<double>::quiet_NaN()`) is one
  way to signal an undefined result (like statistics on an empty input) at
  a function boundary, without throwing.
- Know that NaN never compares equal to anything, including itself, so
  checking for it requires `std::isnan(x)`, never `x == NaN`.
- Be able to organize a project as a multi-target CMake build producing one
  library and one separate test executable from a single configuration,
  and write test cases against a provided lightweight test harness.

## Study checklist

- [ ] Given a snippet using a specific C++ feature, look up (or recall)
      which standard introduced it and set `CMAKE_CXX_STANDARD`
      accordingly.
- [ ] List the six standard documentation files and what each is for.
- [ ] Given a `CMakeLists.txt`, derive the directory structure it expects.
- [ ] Explain why NaN must be checked with `std::isnan` instead of `==`.
- [ ] Explain the difference between population and sample variance.

## Practiced in

`cpp-standards-hunt`, `project-docs`, `project-layout`, `stats-library`
