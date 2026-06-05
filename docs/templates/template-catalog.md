# Template Catalog

This document lists planned templates.

## Python templates

### `python-function`

For assignments where students implement one or more functions.

Expected public files:

```text
assignment.toml
README.md
visible-tests/test_visible.py
assets/starter.py
```

Private grader pattern: `OutputCompareTest` or pytest-style `FileOutputTest`.

### `python-stdin-stdout`

For classic programming contest style assignments.

Expected public files:

```text
assignment.toml
README.md
visible-tests/test_visible.py
expected/sample-input.txt
expected/sample-output.txt
```

Private grader pattern: `OutputCompareTest` with stdin/stdout comparison.

### `python-pytest`

For assignments where students submit a module tested by pytest.

Expected public files:

```text
assignment.toml
README.md
visible-tests/test_visible.py
assets/
```

Private grader pattern: `BashScriptBuild` to run pytest, `FileOutputTest` to compare pytest output.

### `python-package`

For larger multi-file Python projects.

Expected public files:

```text
assignment.toml
README.md
visible-tests/
assets/pyproject.toml
assets/src/
```

Private grader pattern: `BashScriptBuild` (pip install + test runner).

## C/C++ templates

### `cpp-stdin-stdout`

For single-file C++ stdin/stdout assignments.

Private grader pattern: `CMakeBuild` + `OutputCompareTest`.

### `cpp-cmake`

For C++ assignments built with CMake.

Private grader pattern: `CMakeManifestCheck` + `CMakeBuild` + `OutputCompareTest` or `ValgrindTest`.

### `c-stdin-stdout`

For single-file C stdin/stdout assignments.

Private grader pattern: `CMakeBuild` or `MakefileBuild` + `OutputCompareTest`.

## Java templates

### `java-stdin-stdout`

For single-class Java stdin/stdout assignments.

### `java-gradle`

For larger Java project assignments.

## Generic templates

### `data-files`

For assignments centered around parsing supplied files.

Private grader pattern: `OutputCompareTest` or `FileOutputTest` with file inputs passed as arguments.

### `multi-file-project`

For projects with starter code spread across multiple files.

### `performance-benchmark`

For assignments with performance expectations.

Private grader pattern: `PerformanceTest` with `PerformanceCase(name, args, stdin, time_limit: float)`.

Each case specifies a `time_limit` in seconds. lograder measures wall time using `perf_counter` and kills the process at `time_limit + 30s` if it does not exit. Scoring uses `TestCaseScorer` keyed on case names.

Example grader scaffold:

```python
from lograder.pipeline.test.performance import PerformanceTest, PerformanceCase
from lograder.pipeline.score import TestCaseScorer

_CASES = [
    PerformanceCase(name="small", args=["10"], stdin="", time_limit=1.0),
    PerformanceCase(name="large", args=["100000"], stdin="", time_limit=5.0),
]

_SCORER = TestCaseScorer({"small": 5.0, "large": 10.0}, label="Performance")
```
