# Activity: GoogleTest Tour

GoogleTest (GTest) is the test framework you will use in your Operating Systems
and Systems Programming assignments.  It is the dominant C++ testing framework
in industry and powers most of Google's own test suites.  This tour covers the
essentials: linking GTest with CMake, writing TEST() and TEST_F() cases, choosing
between ASSERT_ and EXPECT_ macros, and filtering tests on the command line.

## Concepts covered

- Declaring the `GTest::gtest_main` link target in CMake
- `TEST(Suite, Name)` vs `TEST_F(Fixture, Name)` for stateful setup
- `ASSERT_` macros abort; `EXPECT_` macros continue -- when to use each
- `EXPECT_NEAR` for floating-point comparisons with a tolerance
- `SetUp()` and `TearDown()` in a test fixture class
- The `--gtest_filter` wildcard syntax

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

The FetchContent package is named `googletest` (lowercase).  The CMake imported
targets it provides use the `GTest::` namespace.  You want the target that
supplies a `main()` so you do not have to write one yourself.  Compare with
`GTest::GTest`, which links only the library.

</details>

<details>
<summary>Hint -- Q3: ASSERT_ vs EXPECT_</summary>

Both macros check a condition.  ASSERT_ stops the current test function
immediately on failure.  EXPECT_ records a failure and keeps running.  If the
assertion on line A uses ASSERT_ and fails, ask yourself: can line B ever run?

</details>

<details>
<summary>Hint -- Q5: fixture setup method</summary>

Look at the method name in the fixture class body.  GTest calls it
automatically before each TEST_F.  The name follows PascalCase (both words
capitalized).

</details>

<details>
<summary>Hint -- Q6: --gtest_filter wildcard</summary>

The filter pattern is `SuiteName.TestName`.  An asterisk `*` matches any
sequence of characters in either position.  To match all tests in suites whose
names START with "Hash", put the asterisk after "Hash" without a dot.

</details>

## Going further

- Try `EXPECT_DEATH(stmt, regex)` to assert that a statement crashes with a
  matching error message -- useful for testing `assert()` guards.
- Explore `SCOPED_TRACE("msg")` to add context to assertion failures inside
  helper functions.
- Run your tests with `--gtest_repeat=10 --gtest_shuffle` to catch
  order-dependent test interactions.
- Compare GTest fixture TearDown() with RAII: which is safer when a test throws?
