# Step Reference

## Input step

### `LocalDirectory`

```python
from lograder.pipeline.input.local_directory import LocalDirectory
```

Always the first step. Reads the submission directory from `EnvironmentConfig.root_directory` and returns a `Manifest` listing all files.

- Input: `PIPELINE_START` (sentinel -- no actual input)
- Ok output: `Manifest`
- Fatal Err output: none (always succeeds)

---

## Build steps

All build steps take a `Manifest` as input and return `dict[str, Artifact]` on success.

### `CMakeBuild`

```python
from lograder.pipeline.build.cmake import CMakeBuild
```

Runs CMake configure + build. Requires a `CMakeManifest` input (use `make_simple_manifest_checker` to generate the check step that produces one).

```python
from lograder.pipeline.check.project.simple_project import make_simple_manifest_checker
make_simple_manifest_checker("MyTarget", ["CMakeLists.txt", "main.cpp"])
# Injects CMakeManifest, CMakeManifestCheck, CMakeManifestCheckError into caller globals
```

Fatal on build failure. Returns `dict[str, Artifact]` keyed by CMake target name.

### `MakefileBuild`

```python
from lograder.pipeline.build.makefile import MakefileBuild
```

Runs `make`. Returns `Ok({})` -- artifact parsing is not implemented. Use `PrebuiltArtifacts` to specify the output manually.

### `BashScriptBuild`

```python
from lograder.pipeline.build.bash_script import BashScriptBuild
```

Runs an arbitrary shell script. Useful for `pip install`, pytest runners, or custom build steps.

```python
BashScriptBuild(script=Path("hidden-tests/setup.sh"))
```

Returns `Ok({})` on exit code 0, fatal `Err(BuildOutput)` on nonzero.

### `PrebuiltArtifacts`

```python
from lograder.pipeline.build.prebuilt import PrebuiltArtifacts
```

Skips building and provides a fixed artifact dict. Use for interpreted languages (Python, etc.) where there is nothing to compile.

```python
PrebuiltArtifacts({"solution.py": FileArtifact(Path("solution.py"))})
```

---

## Test steps

All test steps take `dict[str, Artifact]` as input and return it unmodified on success (pass-through). This allows chaining multiple test steps.

### `OutputCompareTest`

```python
from lograder.pipeline.test.output_compare import OutputCompareTest, OutputCompareCase
```

Runs an artifact and compares stdout against expected output.

```python
OutputCompareTest(artifact_name: str, cases: Iterable[OutputCompareCase], options?)
```

**`OutputCompareCase` fields:**

| Field | Type | Default | Description |
|---|---|---|---|
| `name` | str | required | Unique case name, used as scorer key |
| `args` | list[str] | required | Command-line arguments |
| `stdin` | str | required | Text written to stdin |
| `expected_stdout` | str | required | Expected stdout output |
| `comparison` | ComparisonMode | `STRIP` | How to compare output |
| `expected_exit_code` | int \| None | `None` | If set, checks exit code |

### `ValgrindTest`

```python
from lograder.pipeline.test.valgrind import ValgrindTest, ValgrindCase
```

Runs an artifact under Valgrind and checks for memory errors and leaks.

```python
ValgrindTest(artifact_name: str, cases: Iterable[ValgrindCase], options?)
```

**`ValgrindCase` fields:**

| Field | Type | Default | Description |
|---|---|---|---|
| `name` | str | required | Unique case name |
| `args` | list[str] | required | Command-line arguments |
| `stdin` | str | required | Text written to stdin |
| `check_leaks` | bool | `True` | Whether to fail on memory leaks |

### `FileOutputTest`

```python
from lograder.pipeline.test.file_output import FileOutputTest, FileOutputCase
```

Runs an artifact and compares a file it writes against expected content.

```python
FileOutputTest(artifact_name: str, cases: Iterable[FileOutputCase], options?)
```

**`FileOutputCase` fields:**

| Field | Type | Default | Description |
|---|---|---|---|
| `name` | str | required | Unique case name |
| `args` | list[str] | required | Command-line arguments |
| `stdin` | str | required | Text written to stdin |
| `output_file` | Path | required | File the program must write |
| `expected_content` | str | required | Expected file content |
| `comparison` | ComparisonMode | `STRIP` | How to compare content |
| `expected_exit_code` | int \| None | `None` | If set, checks exit code |

### `PerformanceTest`

```python
from lograder.pipeline.test.performance import PerformanceTest, PerformanceCase
```

Runs an artifact and checks that it completes within a time limit. The process is killed at `time_limit + 30s` if it has not exited.

```python
PerformanceTest(artifact_name: str, cases: Iterable[PerformanceCase], base_options?)
```

**`PerformanceCase` fields:**

| Field | Type | Description |
|---|---|---|
| `name` | str | Unique case name |
| `args` | list[str] | Command-line arguments |
| `stdin` | str | Text written to stdin |
| `time_limit` | float | Wall-clock time limit in seconds |

### `DifferentialTest`

```python
from lograder.pipeline.test.differential import DifferentialTest
from lograder.pipeline.test.oracle import OracleInput
```

Runs an artifact and a reference binary on the same input, compares their outputs. No expected output is hardcoded.

```python
DifferentialTest(
    artifact_name: str,
    reference: Path,
    cases: Iterable[OracleInput],
    options?,
    reference_options?,
    check_exit_codes: bool = False,
)
```

See `docs/grader/oracle.md` for `OracleInput` and `cases_from_matrix`.

---

## `ComparisonMode`

```python
from lograder.pipeline.test.output_compare import ComparisonMode
```

| Value | Behavior |
|---|---|
| `ComparisonMode.EXACT` | Byte-for-byte match |
| `ComparisonMode.STRIP` | Strip leading/trailing whitespace from each line (default) |
| `ComparisonMode.IGNORE_TRAILING_WHITESPACE` | Strip trailing whitespace only |

---

## Artifacts

Build steps return `dict[str, Artifact]`. Test steps receive this dict and look up artifacts by name.

The `artifact_name` argument to test steps must match a key in the dict produced by the preceding build step.

For `PrebuiltArtifacts`, you define the keys yourself:

```python
from lograder.pipeline.pipeline.types.artifacts import FileArtifact

PrebuiltArtifacts({
    "solution": FileArtifact(Path("solution.py")),
})
```

For `CMakeBuild`, keys are CMake target names as defined in `CMakeLists.txt`.
