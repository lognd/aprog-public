# Activity: GTest CMake Lab

Not every CMakeLists.txt you encounter will work.  This activity gives you a
GoogleTest project with three deliberate bugs -- the kind that appear when
someone copies a template and fills in the wrong values.  Your job is to find
all three bugs, fix them, and then extend the existing test suite with two new
`TEST` cases of your own.

## Concepts covered

- `FetchContent_Declare` package naming conventions for GoogleTest
- `FetchContent_MakeAvailable` and why omitting it is a silent failure
- The difference between `GTest::GTest` and `GTest::gtest_main`
- Writing `TEST(Suite, Name)` cases with `EXPECT_EQ` and `EXPECT_THROW`

## How it works

The launcher drops you into a shell with a `CMakeLists.txt` that has three
bugs and a `test_calculator.cpp` with three working tests and two `// TODO`
stubs.  Fix the CMake bugs so the project builds, then write the two new tests
and confirm they pass.  Type `exit` to return to the launcher, which asks three
questions about the bugs you fixed.  Answer them all correctly to receive the
passphrase.

## Getting started

```bash
python3 launch.py
```

### Step 1 -- read CMakeLists.txt and find the three bugs

```
cat CMakeLists.txt
```

The comments in the file point to the three problem areas.  Each bug is on or
near a line that uses FetchContent or `target_link_libraries`.

### Step 2 -- fix the bugs

Use any editor:

```
nano CMakeLists.txt
```

Bug areas to look at:
1. The name passed to `FetchContent_Declare`
2. A missing call after `FetchContent_Declare`
3. The target name in `target_link_libraries`

### Step 3 -- build and confirm the provided tests pass

```bash
cmake -B build .
cmake --build build
./build/calculator_tests
```

### Step 4 -- add two new TEST cases to test_calculator.cpp

Open `test_calculator.cpp` and replace the two `// TODO` comments with real
test cases.  Suggested tests are in the file, but feel free to test anything
on the `Calculator` class.

### Step 5 -- rebuild and run

```bash
cmake --build build
./build/calculator_tests
```

All five tests (three provided + two new) should pass.  Then type `exit`.

## You will know you are done when the launcher prints a passphrase.

## Hints

<details>
<summary>Hint 1 -- FetchContent_Declare package name</summary>

The correct package name for GoogleTest is `googletest` -- one word, all
lowercase, no separators.  CMake uses this name to locate the imported targets
later.  A misspelling creates a different internal name that no targets match.

</details>

<details>
<summary>Hint 2 -- the missing call</summary>

`FetchContent_Declare` registers where to fetch a package.  A second call is
required to actually download it and make its CMake targets available.  Without
this call, the `GTest::` targets do not exist.

</details>

<details>
<summary>Hint 3 -- which GTest target provides main()</summary>

`GTest::GTest` links the GoogleTest library only -- you would need to write
`int main(int argc, char** argv) { testing::InitGoogleTest(&argc, argv); return RUN_ALL_TESTS(); }`
yourself.  Use `GTest::gtest_main` to get a built-in `main()` instead.

</details>

## Going further

- Add a `TEST_F` fixture that creates a `Calculator` once and shares it across
  multiple tests using `SetUp()`.
- Try `EXPECT_DEATH(c.divide(1, 0), "")` -- does GoogleTest catch the exception
  as a death, or only as a throw?  Compare `EXPECT_DEATH` with `EXPECT_THROW`.
- Look up `--gtest_filter` and run only your two new tests by name.
