# Stats Library

## Overview

You will implement a statistics library in C++ and organize it as a proper
multi-target CMake project.  The library provides eight functions that operate
on a `std::vector<double>`.  You will also write your own test suite using a
provided lightweight testing harness.

---

## Learning goals

- Implement descriptive statistics (mean, median, mode, variance, stddev, range) from scratch
- Organize a C++ project as a multi-target CMake build: one library, one test executable
- Write your own test suite using a provided harness, including edge cases
- Signal an undefined result at a function boundary using a sentinel value,
  and distinguish population vs sample statistics

## Task

Implement all eight functions declared in `include/stats.hpp` inside
`src/statslib/stats.cpp`.  Statistics are undefined on an empty vector, so
each function must signal that instead of computing garbage:

- The seven functions that return `double` (`mean`, `median`, `variance`,
  `stddev`, `minimum`, `maximum`, `range`) return
  `std::numeric_limits<double>::quiet_NaN()` when `data` is empty.
- `mode` returns an empty `std::vector<double>` when `data` is empty --
  there are no modes of nothing, so an empty result is already the natural
  sentinel.

Remember `#include <limits>` to get `std::numeric_limits`.  NaN never
compares equal to anything, including itself, so callers (and your tests)
must check for it with `std::isnan(x)` (from `<cmath>`), never `x == NaN`.

Later in the course you will learn better error-signaling mechanisms for
situations like this -- exceptions (`std::invalid_argument`) and
`std::optional` -- and revisit why a sentinel value like NaN is a limited
tool: it only works for types that have a value to spare, and it is easy for
a caller to forget to check for it.

```cpp
namespace stats {

// Returns the arithmetic mean.
double mean(const std::vector<double>& data);

// Returns the median (sorts a copy internally).
double median(std::vector<double> data);

// Returns all modes sorted ascending.
// If all values are distinct, every value is a mode.
std::vector<double> mode(const std::vector<double>& data);

// Returns population variance (mean of squared deviations from the mean).
double variance(const std::vector<double>& data);

// Returns population standard deviation (sqrt of variance).
double stddev(const std::vector<double>& data);

// Returns the minimum value.
double minimum(const std::vector<double>& data);

// Returns the maximum value.
double maximum(const std::vector<double>& data);

// Returns maximum - minimum.
double range(const std::vector<double>& data);

}  // namespace stats
```

You must also:

- Write test cases in `tests/test_stats.cpp` using the provided harness.
- Fill in `README.md`, `CONTRIBUTORS.md`, and `LICENSE` with real content
  (each must contain at least 20 non-whitespace characters).

---

## Files

The starter code you receive:

```
CMakeLists.txt                     -- build configuration (do not rename targets)
README.md                          -- this file; fill it in
CONTRIBUTORS.md                    -- list your name
LICENSE                            -- add license text
include/stats.hpp                  -- declarations (do not modify)
src/statslib/stats.cpp             -- YOUR implementation goes here
src/testing_harness/harness.hpp    -- provided harness (do not modify)
tests/test_stats.cpp               -- YOUR tests go here
scripts/build.sh                   -- convenience build script
```

---

## Compilation and Testing

Build with CMake from the project root:

```bash
mkdir -p build
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

Or use the provided script:

```bash
bash scripts/build.sh
```

Run your tests:

```bash
./build/stats_tests
```

You can also compile the visible tests standalone to check your implementation
before submitting:

```bash
g++ -std=c++17 -I include -I src \
    visible-tests/test_visible.cpp src/statslib/stats.cpp \
    -o test_visible
./test_visible
```

---

## Constraints

- Use C++17.
- Do not modify `include/stats.hpp` or `src/testing_harness/harness.hpp`.
- Do not rename the CMake targets `statslib` or `stats_tests`.
- On empty input, `mean`, `median`, `variance`, `stddev`, `minimum`,
  `maximum`, and `range` return `std::numeric_limits<double>::quiet_NaN()`;
  `mode` returns an empty vector. Do not throw.
- `median` must sort a copy of the input, not the original.
- `mode` must return results sorted in ascending order.
- `variance` and `stddev` are population statistics (divide by n, not n-1).

---

## Grading

| Component | Points |
|-----------|--------|
| Project structure (required files present) | 0 (blocking) |
| Documentation (README, CONTRIBUTORS, LICENSE non-empty) | 10 |
| CMake build (your CMakeLists.txt configures and builds cleanly) | 10 |
| Correctness (staff test suite) | 80 |
| Gimme (awarded if you pass at least half the correctness tests) | 5 |
| **Total** | **105** |

The project structure and compilation checks are gates: if either fails, no
further tests run.

## Going further

- Add a `trimmed_mean(data, fraction)` function that removes the top and bottom
  `fraction` of values before computing the mean. Write tests for it.
- Look up the difference between population variance (divide by n) and sample
  variance (divide by n-1). When would you use each, and which does this
  assignment use?
- Benchmark `median` on a 1,000,000-element vector. Is sorting the copy the
  bottleneck? Look up `std::nth_element` as a faster O(n) alternative.
