# Activity: Catch2 Tour

Catch2 is a **test framework**: a library that lets you write small, automated
checks (called tests) for your code and run all of them with one command,
instead of manually re-running your program and eyeballing the output each
time.  Catch2 is the test framework you will use in every Data Structures
assignment.  This tour walks you through the concepts you need before your
first graded submission: how to wire Catch2 into a CMake project, how
`TEST_CASE` (a labeled block of test code) and `SECTION` (a sub-block inside a
`TEST_CASE` for one specific scenario) work, when to use `REQUIRE` vs `CHECK`
(both check a condition and fail the test if it is false; the difference is
what happens next), and how to filter or inspect your tests from the command
line.

## Concepts covered

- Declaring the `Catch2::Catch2WithMain` link target in CMake
- Defining test cases with `TEST_CASE` and `SECTION`
- Difference between `REQUIRE` (abort on failure) and `CHECK` (continue on failure)
- How Catch2 re-runs setup code for each `SECTION`
- Tag-based test filtering with `[tag]` on the command line
- The `-v` flag for verbose assertion output

## How it works

The launcher shows you seven short C++ or CMake snippets and asks a question
about each one.  Type your answer and press Enter.  The launcher tells you
immediately whether you are right; if not, it explains the correct answer and
lets you try again.  Earn the passphrase by answering all seven questions
correctly.

## Getting started

```bash
python3 launch.py
```

There is no shell to open -- just read each snippet and answer the question.
The snippets are self-contained; no compiler needed.

## You will know you are done when the launcher prints a passphrase.

## Hints

<details>
<summary>Hint -- Q1: CMake link target</summary>

Look at the FetchContent block.  The package is named `Catch2`.  The generated
CMake targets follow the pattern `PackageName::TargetName`.  You want the target
that supplies a `main()` so you do not have to write one yourself.

</details>

<details>
<summary>Hint -- Q3: REQUIRE vs CHECK</summary>

Both macros test the condition.  One stops the test immediately; the other
records a failure and keeps going.  Think about which one would save you from
dividing by zero on the very next line.

</details>

<details>
<summary>Hint -- Q4: SECTION re-entry count</summary>

Catch2 does NOT run all SECTIONs in a single pass through the TEST_CASE body.
It enters the TEST_CASE once per SECTION, executing all code from the top until
it reaches that particular SECTION.  Count how many times the setup line
before the first SECTION must therefore execute.

</details>

## Going further

- Read the Catch2 v3 migration guide to see what changed from v2.
- Try `--list-tests` and `--list-tags` on a real test binary to explore what
  Catch2 can discover automatically.
- Experiment with nested SECTIONs: a SECTION inside a SECTION creates a
  combinatorial grid of test paths.
- Add `[!benchmark]` to a test and run it with `--benchmark-samples 100` to
  see Catch2's built-in microbenchmark support.
