# Study Guide 17: Testing Tools (Catch2, gtest, gdb)

This module introduces the two C++ test frameworks used across the course
(Catch2 and GoogleTest), how to wire each into CMake with FetchContent,
and gdb as the tool for freezing a crashed program in time. The html-parser
assignment then grades not just a parser but the student's own Catch2 test
suite, including its ability to detect deliberately seeded bugs.

## Know before you start

- CMake targets, `target_link_libraries`, and the `cmake -B build` /
  `cmake --build build` workflow [assumed: row 8 -- Makefile & CMake]
- `strncpy` and its silent null-terminator omission [assumed: row 12 --
  C-Style Strings & Arrays]
- Stack traces and frame numbering from crash reports [assumed: row 10 --
  Memory Model]
- Character-by-character string scanning with parser state [assumed:
  row 7 -- Standard Library Types]

## Taught here

Concept: what a test framework is
- Know that a test framework is a library for writing small automated
  checks (tests) on your code and running all of them with one command,
  instead of manually re-running the program and eyeballing output.
- Know that a test suite is a collection of labeled test cases, and that a
  hidden test is one the grader keeps private so code cannot be written to
  match it.

Concept: Catch2
- Know that `TEST_CASE` declares a labeled block of test code and `SECTION`
  declares a sub-block for one specific scenario inside it.
- Know that Catch2 re-enters a `TEST_CASE` once per `SECTION`, executing
  all code from the top of the test case down to that section -- so setup
  code before the first section runs once per section, not once total.
- Know that `REQUIRE` aborts the test case on failure while `CHECK` records
  the failure and continues, and that `REQUIRE` is the right choice when a
  failed condition would make the next line unsafe (for example, a
  division by zero).
- Know that tests can carry `[tag]` labels and be filtered by tag on the
  command line, and that `-v` produces verbose assertion output.
- Know the two Catch2 CMake link targets: `Catch2::Catch2` (library only)
  and `Catch2::Catch2WithMain` (library plus a generated `main()`, so you
  never write `int main` yourself).
- Be able to wire Catch2 into a project with `FetchContent_Declare` (a
  Git repository URL and a pinned `GIT_TAG` version) followed by
  `FetchContent_MakeAvailable`, then link the test executable against
  `Catch2::Catch2WithMain`.

Concept: GoogleTest
- Know that `TEST(Suite, Name)` declares a standalone test, while
  `TEST_F(Fixture, Name)` uses a test fixture class whose `SetUp()` runs
  before each test and `TearDown()` runs after, for shared stateful setup.
- Know that `ASSERT_` macros abort the current test function on failure
  while `EXPECT_` macros record the failure and keep running -- the same
  abort/continue split as Catch2's `REQUIRE`/`CHECK`.
- Know that `EXPECT_NEAR` compares floating-point values with an explicit
  tolerance instead of exact equality.
- Know the GTest CMake conventions: the FetchContent package name is
  `googletest` (one lowercase word), and `GTest::gtest_main` is the link
  target that supplies `main()` (unlike `GTest::GTest`, which links only
  the library).
- Know that forgetting `FetchContent_MakeAvailable` is a silent failure
  mode: the package is declared but never downloaded, so the `GTest::`
  targets simply do not exist.
- Be able to filter tests from the command line with `--gtest_filter`
  using `SuiteName.TestName` patterns and `*` wildcards.

Concept: gdb
- Know that gdb is a debugger: it runs your program under its control so
  you can pause execution, inspect variables, and see exactly which line
  was running when something went wrong.
- Be able to use the core gdb commands: `run` (start), `bt` (print a
  backtrace -- the chain of active function calls, innermost first as
  frame 0), `frame N` (jump to one call in that chain), `print var` (show
  a variable's value), `break func` (set a breakpoint), `next` (step over
  one line), and `x/Ncb addr` (examine N raw memory bytes as characters).
- Know that a null pointer prints as `0x0` in gdb, and that frame 0 of a
  backtrace is where execution actually stopped.
- Know that when `strncpy` copies a source whose length exactly equals the
  byte limit, it writes no null terminator, so a later `printf("%s")`
  reads past the buffer until it happens to find a zero byte -- an
  out-of-bounds read that gdb's memory examination makes visible.

Concept: writing a graded test suite
- Be able to organize a Catch2 test suite around named test cases covering
  explicit edge-case categories: empty input, no-match input, nesting,
  case-insensitivity, boundary text placement, adjacent/malformed tokens.
- Know that test quality is measured by fault detection: a suite is run
  against deliberately buggy implementations, and only tests that actually
  assert behavior (rather than always passing) can catch a seeded bug.
- Be able to implement a small tag parser by scanning character by
  character, recognizing `<...>` delimited tokens, treating an unmatched
  `<` as a literal character, lowercasing for case-insensitive tag-name
  comparison, and distinguishing open tags from close tags by a leading
  `/`.

## Study checklist

- [ ] Explain how many times setup code runs in a Catch2 `TEST_CASE`
      containing three `SECTION`s.
- [ ] State when to use `REQUIRE`/`ASSERT_` instead of `CHECK`/`EXPECT_`.
- [ ] Name the Catch2 and GTest CMake link targets that provide `main()`.
- [ ] Explain why omitting `FetchContent_MakeAvailable` breaks the build
      and what the error looks like.
- [ ] Walk through the gdb commands to find the function where a segfault
      occurred and print the offending pointer.
- [ ] Explain why a test that always passes earns nothing in fault
      detection.

## Practiced in

`catch2-tour`, `gtest-tour`, `catch2-first-contact`, `gtest-cmake-lab`, `gdb-time-machine`, `html-parser`
