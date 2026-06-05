# Grader Overview

The grader package is `lograder`. It is a Python library -- not a CLI and not a service.

Contributors write a `grader/pipeline.py` file that uses lograder to define how their assignment is graded. AProg generates the surrounding `run_autograder.py` entry point, but the grading logic is entirely in `pipeline.py`.

## What `pipeline.py` must export

```python
from lograder.pipeline.pipeline import Pipeline

def make_pipeline() -> Pipeline:
    ...
```

`make_pipeline` constructs a `Pipeline` and returns it. AProg's generated `run_autograder.py` calls it inside the appropriate environment context.

## Pipeline and steps

A `Pipeline` is a sequence of `Step` objects. Each step receives the output of the previous step, performs work, and yields log packets. Steps are connected by type: the `Ok` output type of step N must match the `Input` type of step N+1.

The standard data flow is:

```
LocalDirectory -> [Build step] -> [Test step(s)]
```

- `LocalDirectory` reads the student submission directory and returns a `Manifest`.
- A build step compiles the submission and returns artifacts.
- Test steps run the artifacts against test cases.

Steps have two return modes:

- `yield Err(...)` -- logs a non-fatal error and continues
- `return Err(...)` -- logs a fatal error and stops the pipeline

## Minimal example (Python, no build)

```python
from lograder.pipeline.input.local_directory import LocalDirectory
from lograder.pipeline.pipeline import Pipeline
from lograder.pipeline.test.output_compare import OutputCompareTest, OutputCompareCase
from lograder.pipeline.score import TestCaseScorer

def make_pipeline() -> Pipeline:
    step = LocalDirectory()

    cases = [
        OutputCompareCase(name="basic", args=[], stdin="1 2\n", expected_stdout="3\n"),
    ]

    tests = OutputCompareTest("solution.py", cases)
    tests.scorer = TestCaseScorer({"basic": 10.0}, label="Correctness")

    return Pipeline([step, tests])
```

## C++ example (CMake build + tests)

```python
from lograder.pipeline.input.local_directory import LocalDirectory
from lograder.pipeline.pipeline import Pipeline
from lograder.pipeline.check.project.simple_project import make_simple_manifest_checker
from lograder.pipeline.build.cmake import CMakeBuild
from lograder.pipeline.test.output_compare import OutputCompareTest, OutputCompareCase
from lograder.pipeline.score import AllOrNothingScorer, TestCaseScorer

make_simple_manifest_checker("MyProject", ["CMakeLists.txt", "main.cpp"])

def make_pipeline() -> Pipeline:
    step = LocalDirectory()
    check = CMakeManifestCheck()
    build = CMakeBuild()
    build.scorer = AllOrNothingScorer(0.0, label="Build")

    cases = [
        OutputCompareCase(name="test_add", args=[], stdin="1 2\n", expected_stdout="3\n"),
    ]
    tests = OutputCompareTest("MyProject", cases)
    tests.scorer = TestCaseScorer({"test_add": 20.0}, label="Correctness")

    return Pipeline([step, check, build, tests])
```

`make_simple_manifest_checker` injects `CMakeManifest`, `CMakeManifestCheck`, etc. into the caller's global scope.

## Further reference

- `docs/grader/steps.md` -- all step types and their case models
- `docs/grader/scoring.md` -- scorers and point configuration
- `docs/grader/config.md` -- EnvironmentConfig and GradescopeConfig
- `docs/grader/oracle.md` -- generating test cases from a reference binary
