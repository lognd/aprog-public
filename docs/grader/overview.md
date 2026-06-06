# Grader Overview

The grader package is [lograder](https://github.com/lognd/lograder). It is a Python library -- not a CLI and not a service.

Contributors write a `grader/pipeline.py` file that uses lograder to define how their assignment is graded. AProg generates the surrounding `run_autograder.py` entry point, but the grading logic is entirely in `pipeline.py`.

**For the full lograder reference -- step types, scorers, build steps, test types, and all configuration options -- see the [lograder documentation](https://github.com/lognd/lograder).**

---

## What `pipeline.py` must export

```python
from pathlib import Path
from lograder.pipeline.pipeline import Pipeline

def make_pipeline(submission_dir: Path = Path("/autograder/submission")) -> Pipeline:
    ...
```

`make_pipeline` constructs and returns a `Pipeline`. The generated `run_autograder.py` calls it inside the appropriate environment context.

---

## Pipeline structure

A `Pipeline` is a sequence of `Step` objects. Each step receives the output of the previous step, performs work, and yields log packets. Steps are connected by type: the `Ok` output of step N must match the `Input` type of step N+1.

The standard data flow is:

```
LocalDirectory -> [Build step] -> [Test step(s)]
```

- `LocalDirectory` reads the student submission directory and returns a `Manifest`.
- A build step (e.g. `CMakeBuild`, `MakefileBuild`) compiles the submission and returns artifacts.
- Test steps run the artifacts against test cases.

Steps have two return modes:

- `yield Err(...)` -- logs a non-fatal error and continues
- `return Err(...)` -- logs a fatal error and stops the pipeline

---

## Minimal example (Python, no build)

```python
from pathlib import Path
from lograder.pipeline.input.local_directory import LocalDirectory
from lograder.pipeline.pipeline import Pipeline
from lograder.pipeline.test.pytest import PytestTest
from lograder.pipeline.score import TestCaseScorer, GimmeConfig

_GRADER_DIR = Path(__file__).parent
_HIDDEN_TESTS = _GRADER_DIR / "hidden-tests"

_POINTS = {
    "test_hidden::test_case_1": 20.0,
    "test_hidden::test_case_2": 20.0,
}

def make_pipeline(submission_dir: Path = Path("/autograder/submission")) -> Pipeline:
    import os
    os.environ["SUBMISSION_DIR"] = str(submission_dir)

    pipeline = Pipeline()
    pipeline.add(LocalDirectory(root=submission_dir))
    pipeline.add(tests := PytestTest(paths=[_HIDDEN_TESTS]))
    tests.scorer = TestCaseScorer(
        _POINTS,
        gimme=GimmeConfig(min_pass_fraction=0.25, points=10.0),
        label="Correctness",
    )
    return pipeline
```

---

## C++ example (CMake build + tests)

```python
from pathlib import Path
from lograder.pipeline.input.local_directory import LocalDirectory
from lograder.pipeline.pipeline import Pipeline
from lograder.pipeline.build.cmake import CMakeBuild
from lograder.pipeline.test.output_compare import OutputCompareTest, OutputCompareCase, ComparisonMode
from lograder.pipeline.score import AllOrNothingScorer, TestCaseScorer, GimmeConfig, GradescopeTestConfig

_GRADER_DIR = Path(__file__).parent

_CASES = [
    OutputCompareCase(name="basic", args=[], stdin=b"1 2\n", expected_stdout="3\n",
                      comparison=ComparisonMode.STRIP),
]

def make_pipeline(submission_dir: Path = Path("/autograder/submission")) -> Pipeline:
    pipeline = Pipeline()
    pipeline.add(LocalDirectory(root=submission_dir))

    pipeline.add(build := CMakeBuild(source_dir=_GRADER_DIR))
    build.scorer = AllOrNothingScorer(10.0, label="Build")
    build.scorer.gradescope = GradescopeTestConfig(visibility="visible", number="1")

    pipeline.add(tests := OutputCompareTest("my-program", _CASES))
    tests.scorer = TestCaseScorer(
        {"basic": 20.0},
        gimme=GimmeConfig(min_pass_fraction=0.25, points=5.0),
        label="Correctness",
    )
    return pipeline
```

---

## Common gotchas

**Pytest score key format**

Score keys are `"module::function"` (e.g. `"test_hidden::test_name"`), not file paths. Run `pytest --collect-only` to confirm the exact IDs.

**hidden-tests path**

`_HIDDEN_TESTS = _GRADER_DIR / "hidden-tests"` -- inside the grader dir, not as a sibling. This is the only path that works both during `aprog verify` and inside the Gradescope zip.

**PytestTest argument**

The argument is `paths=`, not `test_paths=`.

**SUBMISSION_DIR for pytest pipelines**

Set `os.environ["SUBMISSION_DIR"] = str(submission_dir)` in `make_pipeline` before the pipeline runs. The pytest subprocess inherits this and uses it to locate the student module.

See `examples/template-demos/` for working implementations of each template type.

---

## Further reference

- [lograder documentation](https://github.com/lognd/lograder) -- primary reference for all step types, build steps, test types, and scorers
- `examples/template-demos/` -- complete working examples per template
- `examples/full-assignments/cpp-linked-list/` -- full C++ assignment example
- [docs/grader/steps.md](steps.md) -- step type summary
- [docs/grader/scoring.md](scoring.md) -- scorer and point configuration
- [docs/grader/config.md](config.md) -- EnvironmentConfig and GradescopeConfig
- [docs/grader/oracle.md](oracle.md) -- generating test cases from a reference binary
