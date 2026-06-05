# Oracle and Case Generation

Two helpers in `lograder.pipeline.test.oracle` reduce the manual effort of writing test cases.

## When to use oracle helpers

Use **`oracle_cases`** when you have a reference binary and want to pre-capture its outputs as expected values. The expected outputs are stored in the case objects at grader-construction time — no reference binary is needed at Gradescope grading time.

Use **`DifferentialTest`** when you want to compare student output against the reference binary live, at grading time. The reference binary must be present on the Gradescope grading server.

Use **`cases_from_matrix`** with either of the above to generate all combinations of argument pools automatically.

---

## `OracleInput`

```python
from lograder.pipeline.test.oracle import OracleInput
```

A partial case specification used as input to both `oracle_cases` and `DifferentialTest`. It does not include `expected_stdout` — that is either captured from the reference binary or compared live.

```python
OracleInput(
    name: str,
    args: list[str],
    stdin: str,
    comparison: ComparisonMode = ComparisonMode.STRIP,
)
```

---

## `oracle_cases`

```python
from lograder.pipeline.test.oracle import oracle_cases
```

Runs a reference binary on each `OracleInput` and captures stdout + exit code as expected values. Returns a `list[OutputCompareCase]` ready to pass to `OutputCompareTest`.

```python
oracle_cases(
    binary: Path,
    inputs: Iterable[OracleInput],
    options: ExecutableOptions | None = None,
) -> list[OutputCompareCase]
```

The reference binary is run **when `make_pipeline()` is called** (i.e., at Gradescope grading time). For pre-captured expected outputs, run `oracle_cases` at bundle-build time and hardcode the resulting `OutputCompareCase` list instead.

Example:

```python
cases = oracle_cases(
    Path("hidden-tests/reference"),
    [
        OracleInput("small", args=["10"], stdin=""),
        OracleInput("large", args=["100000"], stdin=""),
    ],
)
tests = OutputCompareTest("solution", cases)
```

---

## `cases_from_matrix`

```python
from lograder.pipeline.test.oracle import cases_from_matrix
```

Returns the Cartesian product of argument pools as `OracleInput` objects. Raises `ValueError` if the total would exceed `max_cases`.

```python
cases_from_matrix(
    *arg_pools: Iterable[str],
    name_fn: Callable[[tuple[str, ...]], str] | None = None,
    stdin: str = "",
    comparison: ComparisonMode = ComparisonMode.STRIP,
    max_cases: int = 500,
) -> list[OracleInput]
```

The default `name_fn` joins the argument tuple with underscores.

Example:

```python
# 3 operations × 3 values = 9 cases
inputs = cases_from_matrix(
    ["add", "sub", "mul"],
    ["1", "10", "100"],
)

# Pre-capture expected outputs from staff binary
cases = oracle_cases(Path("hidden-tests/staff_solution"), inputs)

tests = OutputCompareTest("solution", cases)
```

---

## `DifferentialTest` with `cases_from_matrix`

For live comparison at grading time (reference binary present on grading server):

```python
from lograder.pipeline.test.differential import DifferentialTest

tests = DifferentialTest(
    artifact_name="solution",
    reference=Path("hidden-tests/staff_solution"),
    cases=cases_from_matrix(["add", "sub", "mul"], ["1", "10", "100"]),
    check_exit_codes=False,
)
```

The reference binary path is resolved relative to the grading server's working directory. Make sure it is included in the Gradescope zip by listing it in `hidden-tests/`.

---

## Choosing between oracle_cases and DifferentialTest

| | `oracle_cases` + `OutputCompareTest` | `DifferentialTest` |
|---|---|---|
| Reference binary needed at grading time | No | Yes |
| Expected outputs visible in bundle | Yes (stored in case objects) | No |
| Suitable for non-deterministic output | No | No |
| Suitable for large input sets | Yes (run once at build time) | Yes (run per submission) |
