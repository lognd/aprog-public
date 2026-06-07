# cmake-heist

A multi-module C++ project with no build system. Your job is to write
`CMakeLists.txt` from scratch -- or rather, from an outline.

## Getting started

    python3 launch.py

A shell opens inside a fresh copy of the project. A `CMakeLists.txt`
is already there with comments guiding each section. Fill it in.

## The project

    lib_math/    -- static library: gcd, is_prime, prime_count
    lib_text/    -- static library: digit_count, print_row, print_rule
                    (depends on lib_math internally)
    app/         -- main executable, uses both libraries
    lib_*/tests/ -- test harness for each library

## What you must write

A single `CMakeLists.txt` at the root of the project that:

- Declares the project and sets the C++ standard
- Defines a static library target `math` with public include paths
- Defines a static library target `text` that links against `math`
- Defines `app` as an executable linked against both libraries
- Enables testing and registers two test executables (`test_math`, `test_text`)

## Validation

The launcher runs four checks when you type `exit`:

1. `cmake -B build` -- CMakeLists.txt must configure without errors
2. `cmake --build build` -- everything must compile and link
3. `ctest --test-dir build` -- both test suites must pass
4. `./build/app` -- output must match expected

All four must pass.

## You will know you are done when...

The launcher prints the passphrase.

## Hints

<details>
<summary>Hint 1 -- where to start</summary>

Every CMakeLists.txt begins the same way: declare the minimum CMake version,
name the project, and set the C++ standard. Look up
`cmake_minimum_required`, `project`, `CMAKE_CXX_STANDARD`.

</details>

<details>
<summary>Hint 2 -- defining a library</summary>

`add_library(name STATIC source.cpp)` creates a static library target.
The name you choose becomes the CMake target name. The toolchain then
produces the actual file: `libname.a` on Linux/macOS, `name.lib` on
Windows. You name the target; the `lib` prefix is added for you.

To make a library's headers available to targets that link against it:

    target_include_directories(name PUBLIC path/to/include)

`PUBLIC` means: both the library itself AND anything that links against it
will get this include path. `PRIVATE` means only the library itself.

</details>

<details>
<summary>Hint 3 -- expressing dependencies</summary>

`target_link_libraries(target PRIVATE dep)` links `dep` into `target`.
`PRIVATE` is correct when `target`'s public headers do not expose types
from `dep`. Because `text_utils.h` does not include anything from `math`,
the dependency is private.

When `app` links against `text`, it transitively gets `math` too
(because `text` declared that dependency). You still need to link
`math` explicitly for `app` if `app/main.cpp` calls math functions
directly -- and it does.

</details>

<details>
<summary>Hint 4 -- tests</summary>

You need to build two separate test executables -- one for each library.
`add_executable` defines them just like `app`, with their own source files
and their own `target_link_libraries`. Call `enable_testing()` first, then
define both:

    add_executable(test_math lib_math/tests/test_runner.cpp lib_math/tests/test_math.cpp)
    target_link_libraries(test_math PRIVATE math)
    add_test(NAME math_tests COMMAND test_math)

    add_executable(test_text lib_text/tests/test_runner.cpp lib_text/tests/test_text.cpp)
    target_link_libraries(test_text PRIVATE text)
    add_test(NAME text_tests COMMAND test_text)

`add_test` does not build anything -- it only tells CTest "when tests are
run, execute this command." The executable must already exist, which means
it must be defined with `add_executable` first. `NAME` is the label that
appears in `ctest` output; `COMMAND` is the binary to invoke.

</details>

<details>
<summary>Hint 5 -- include paths inside tests</summary>

The test files include headers like `"lib_math/math_utils.h"`. These headers
live in `lib_math/include`. Because `math` was declared with
`target_include_directories(math PUBLIC lib_math/include)`, any target
that calls `target_link_libraries(... math)` automatically inherits that
include path. You do not need to repeat the `target_include_directories`
call for the test executables.

</details>
