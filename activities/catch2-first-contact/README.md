# Activity: Catch2 First Contact

Reading about a test framework (a library for writing and running small,
automated checks on your code) is different from wiring one up yourself.  In
this activity you complete a real CMake project: fill in four blanks in a
`CMakeLists.txt` that pulls in Catch2 via `FetchContent` (a CMake mechanism
that downloads a third-party library's source and makes it part of your build,
so you do not have to install anything by hand), then write a test suite --
a collection of `TEST_CASE` blocks, each a labeled test -- for a small
statistics library and get every test to pass.

## Concepts covered

- `FetchContent_Declare` and `FetchContent_MakeAvailable` for a third-party library
- The `Catch2::Catch2WithMain` link target and why it exists
- Writing `TEST_CASE` bodies with `REQUIRE` assertions
- The `cmake -B build . && cmake --build build` workflow

## How it works

The launcher drops you into a shell with four source files: `stats.hpp`,
`stats.cpp`, `test_stats.cpp`, and a `CMakeLists.txt` that has four blanks
marked with `___FILL_IN___`.  You fill in the blanks, write test bodies, build,
and run your tests.  When they all pass, type `exit` to return to the launcher,
which then asks four questions about the values you used.  Answer them all
correctly to receive the passphrase.

## Getting started

```bash
python3 launch.py
```

### Step 1 -- open CMakeLists.txt and fill in the four TODOs

Use any editor available (`nano`, `vim`, `code .`):

```
nano CMakeLists.txt
```

The four blanks are:
1. `GIT_REPOSITORY` -- the GitHub URL for Catch2
2. `GIT_TAG` -- the version tag to pin
3. `FetchContent_MakeAvailable(...)` -- the package name to pass
4. `target_link_libraries(... PRIVATE ___)` -- the target that includes `main()`

### Step 2 -- write test bodies in test_stats.cpp

Open `test_stats.cpp` and replace each `// TODO` comment with a real assertion.
Example:

```cpp
TEST_CASE("mean of multiple elements") {
    REQUIRE(mean({1.0, 2.0, 3.0}) == 2.0);
}
```

### Step 3 -- build and run

```bash
cmake -B build .
cmake --build build
./build/stats_tests
```

Fix any compilation or test failures, then type `exit` when all tests pass.

## You will know you are done when the launcher prints a passphrase.

## Hints

<details>
<summary>Hint 1 -- GIT_REPOSITORY URL</summary>

The URL is the standard GitHub clone address for the catchorg/Catch2 repository.
It ends in `.git`.

</details>

<details>
<summary>Hint 2 -- FetchContent_MakeAvailable argument</summary>

The argument must match the first argument of `FetchContent_Declare` exactly,
including capitalization.  CMake uses this name to track the fetched package
internally.

</details>

<details>
<summary>Hint 3 -- which link target provides main()</summary>

There are two Catch2 targets: `Catch2::Catch2` (headers only, no `main()`) and
`Catch2::Catch2WithMain` (headers + a generated `main()`).  You want the second
one so you never have to write `int main()` yourself.

</details>

## Going further

- Add a third function `std::pair<double,double> range(const std::vector<double>&)`
  that returns `{min, max}` and write tests for it.
- Try `SECTION` inside a `TEST_CASE` to test multiple edge cases of `median()`
  without repeating setup code.
- Experiment with `REQUIRE_THROWS` to test what `mean` does with `NaN` values.
