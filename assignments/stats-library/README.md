# Stats Library

## Overview

You will implement a statistics library in C++ and organize it as a proper
multi-target CMake project (a CMake project that builds more than one output --
here, one library and one test executable -- from a single configuration).
The library provides eight functions that operate on a `std::vector<double>`.
You will also write your own test suite using a provided lightweight testing
harness.

Every one of these eight functions shows up constantly in real code -- a
dashboard averaging response times, a grading script finding the median
score, an anomaly detector flagging values far from the mean. The catch is
always the edge cases: what does "the average" even mean for an empty list
of numbers? What happens when several values are tied for "most common"?
This assignment is about implementing the arithmetic correctly AND deciding,
deliberately, what each function does when there is no good numeric answer
to give.

---

## Learning goals

- Implement descriptive statistics (mean, median, mode, variance, stddev, range) from scratch
- Organize a C++ project as a multi-target CMake build: one library, one test executable
- Write your own test suite using a provided harness, including edge cases
- Signal an undefined result at a function boundary using a sentinel value
  (a special, reserved value like NaN -- "Not a Number", a bit pattern that
  stands in for "no valid answer" instead of a real result), and distinguish
  population vs sample statistics

---

## Examples at a glance

To make all eight functions concrete, here is **one** dataset and what every
function returns for it:

```
data = {2.0, 4.0, 4.0, 4.0, 9.0, 10.0}
```

| Call | Returns | Why |
|------|---------|-----|
| `mean(data)`     | `5.5`              | sum is `2+4+4+4+9+10 = 33`, divided by count `6` gives `5.5` |
| `median(data)`   | `4.0`              | sorted, there are 6 values (even count), so the median is the average of the two middle values, `data[2]` and `data[3]` (both `4.0`); an odd-count dataset would instead return the single middle value with no averaging |
| `mode(data)`     | `{4.0}`            | `4.0` appears three times, more than any other value, so it is the only mode |
| `variance(data)` | `8.583333...`      | population variance: average of the squared distance from each value to the mean `5.5`, dividing by `n = 6` (not `n - 1`) |
| `stddev(data)`   | `2.929732...`      | the square root of `variance(data)` |
| `minimum(data)`  | `2.0`              | the smallest value in the dataset |
| `maximum(data)`  | `10.0`             | the largest value in the dataset |
| `range(data)`    | `8.0`              | `maximum(data) - minimum(data)`, i.e. `10.0 - 2.0` |

## Worked example: computing `variance` and `stddev` step by step

This traces `variance({2.0, 4.0, 4.0, 4.0, 9.0, 10.0})` by hand, the same
dataset as above, ending at the `8.583333...` shown in the table.

| Step | Value | Deviation from mean (`value - 5.5`) | Squared deviation | Running sum |
|------|-------|--------------------------------------|--------------------|-------------|
| 1 | `2.0`  | `2.0 - 5.5 = -3.5` | `(-3.5)^2 = 12.25` | `12.25` |
| 2 | `4.0`  | `4.0 - 5.5 = -1.5` | `(-1.5)^2 = 2.25`  | `14.5` |
| 3 | `4.0`  | `4.0 - 5.5 = -1.5` | `(-1.5)^2 = 2.25`  | `16.75` |
| 4 | `4.0`  | `4.0 - 5.5 = -1.5` | `(-1.5)^2 = 2.25`  | `19.0` |
| 5 | `9.0`  | `9.0 - 5.5 = 3.5`  | `(3.5)^2 = 12.25`  | `31.25` |
| 6 | `10.0` | `10.0 - 5.5 = 4.5` | `(4.5)^2 = 20.25`  | `51.5` |

The mean (`5.5`) is computed first, using the same `mean` function -- that
is why `mean` is one of the eight required functions even though `variance`
also needs it internally. After all six deviations are squared and summed,
the running total is `51.5`. Dividing by the count (`n = 6`, NOT `n - 1` --
this is **population** variance, not sample variance) gives:

```
variance = 51.5 / 6 = 8.583333...
```

`stddev` is then just the square root of that number:

```
stddev = sqrt(8.583333...) = 2.929732...
```

If this had instead been **sample** variance (dividing by `n - 1 = 5`), the
result would be `51.5 / 5 = 10.3` -- a different, larger number. This
assignment always divides by `n`, never `n - 1`; see the Constraints
section below.

---

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

### Per-function examples

Concrete `call == result` examples for each function, covering ties, empty
input, and single-element input. All values below were checked against the
reference implementation.

- **`mean(data)`** -- the arithmetic mean (sum divided by count).
  - **Example:** `mean({1.0, 2.0, 3.0, 4.0, 5.0}) == 3.0`.
  - **Edge case (single element):** `mean({7.0}) == 7.0`.
  - **Edge case (empty):** `mean({})` is **`NaN`** (`std::isnan(mean({})) == true`).
- **`median(data)`** -- the middle value once sorted; the average of the two
  middle values when the count is even.
  - **Example (odd count):** `median({5.0, 1.0, 3.0}) == 3.0` (sorts to `{1, 3, 5}`, middle is `3.0` -- note the **input did not need to already be sorted**).
  - **Example (even count):** `median({1.0, 2.0, 3.0, 4.0}) == 2.5` (average of `2.0` and `3.0`).
  - **Edge case (empty):** `median({})` is `NaN`.
- **`mode(data)`** -- every value tied for the highest occurrence count,
  sorted ascending.
  - **Example (single mode):** `mode({1.0, 2.0, 2.0, 3.0}) == {2.0}` (only `2.0` repeats).
  - **Example (multiple modes):** `mode({1.0, 1.0, 2.0, 2.0, 3.0}) == {1.0, 2.0}` (`1.0` and `2.0` are **tied at two occurrences each**, `3.0` is not a mode).
  - **Edge case (empty):** `mode({})` is **`{}`** (empty in, empty out -- no exception, no NaN, since there is no single numeric value to signal "no mode" with).
- **`variance(data)`** -- population variance (divide by `n`, not `n - 1`).
  - **Example:** `variance({2.0, 4.0, 4.0, 4.0, 9.0, 10.0}) == 8.583333...` (see the worked example above).
  - **Edge case (all equal):** `variance({4.0, 4.0, 4.0}) == 0.0` (every value equals the mean, so every squared deviation is `0`).
  - **Edge case (empty):** `variance({})` is `NaN`.
- **`stddev(data)`** -- population standard deviation (`sqrt(variance(data))`).
  - **Example:** `stddev({2.0, 4.0, 4.0, 4.0, 9.0, 10.0}) == 2.929732...`.
  - **Edge case (all equal):** `stddev({4.0, 4.0, 4.0}) == 0.0`.
  - **Edge case (empty):** `stddev({})` is `NaN`.
- **`minimum(data)`** -- the smallest value.
  - **Example:** `minimum({3.0, 1.0, 4.0}) == 1.0`.
  - **Edge case (single element):** `minimum({7.0}) == 7.0`.
  - **Edge case (empty):** `minimum({})` is `NaN`.
- **`maximum(data)`** -- the largest value.
  - **Example:** `maximum({3.0, 1.0, 4.0}) == 4.0`.
  - **Edge case (single element):** `maximum({7.0}) == 7.0`.
  - **Edge case (empty):** `maximum({})` is `NaN`.
- **`range(data)`** -- `maximum(data) - minimum(data)`.
  - **Example:** `range({2.0, 4.0, 4.0, 4.0, 9.0, 10.0}) == 8.0` (`10.0 - 2.0`).
  - **Edge case (single element):** `range({7.0}) == 0.0` (a single element is both the min and the max, so the range is **`0`**).
  - **Edge case (empty):** `range({})` is `NaN`.

You must also:

- Write test cases in `tests/test_stats.cpp` using the provided harness (a
  harness is a small piece of support code that runs your test cases and
  reports pass/fail, so you do not have to write that bookkeeping yourself).
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
