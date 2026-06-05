# Scoring Reference

Scoring is opt-in per step. Set `step.scorer` on any step instance before passing it to `Pipeline`.

Steps with no scorer attached contribute nothing to the final score. Use this for purely structural steps (e.g., a check step that only stops the pipeline on violation).

---

## Attaching a scorer

```python
build = CMakeBuild()
build.scorer = AllOrNothingScorer(20.0, label="Build")

tests = OutputCompareTest("my_target", cases)
tests.scorer = TestCaseScorer({"test_a": 10.0, "test_b": 10.0}, label="Correctness")

pipeline = Pipeline([step, check, build, tests])
score: PipelineScore = pipeline()
```

---

## `TestCaseScorer`

```python
from lograder.pipeline.score import TestCaseScorer
```

Used with test steps (`OutputCompareTest`, `ValgrindTest`, `FileOutputTest`, `PerformanceTest`, `DifferentialTest`).

Awards points per passing test case. Works via `isinstance` check on `TestSuccess`/`TestFailure` -- the scorer is compatible with all test step types.

```python
TestCaseScorer(
    points_per_case: dict[str, float] | float,
    *,
    num_cases: int | None = None,
    extra_credit_cases: dict[str, float] | None = None,
    gimme: GimmeConfig | None = None,
    label: str | None = None,
)
```

**`points_per_case`**: Either a `dict` mapping case name -> points, or a flat `float` applied to all cases (requires `num_cases` when flat).

**`extra_credit_cases`**: Cases that award bonus points on pass. They are not counted in `possible`. Use for optional challenges.

**`gimme`**: If the student passes at least `min_pass_fraction` of attempted cases (excluding cases stopped by fatal error), their score is floored to `gimme.points`. Prevents students from earning zero for minor issues.

```python
from lograder.pipeline.score import GimmeConfig

tests.scorer = TestCaseScorer(
    {"test_a": 10.0, "test_b": 10.0, "test_c": 10.0, "bonus": 0.0},
    extra_credit_cases={"bonus": 5.0},
    gimme=GimmeConfig(min_pass_fraction=0.5, points=5.0),
    label="Correctness",
)
```

---

## `AllOrNothingScorer`

```python
from lograder.pipeline.score import AllOrNothingScorer
```

Used with build steps or check steps. Awards full points if the step returns `Ok`, zero if it returns a fatal `Err`.

```python
AllOrNothingScorer(
    points: float,
    *,
    extra_credit: float = 0.0,
    label: str | None = None,
)
```

Example: award 20 points if the build succeeds, 0 if it fails.

```python
build.scorer = AllOrNothingScorer(20.0, label="Build")
```

---

## `CleanRunScorer`

```python
from lograder.pipeline.score import CleanRunScorer
```

Used with check steps (e.g., source code analysis). Awards points if the number of non-fatal `Err` yields is at or below `max_errors`.

```python
CleanRunScorer(
    points: float,
    *,
    max_errors: int = 0,
    require_ok_return: bool = True,
    extra_credit: float = 0.0,
    label: str | None = None,
)
```

`require_ok_return=True` means a fatal `Err` return also zeroes the score. Set to `False` to award points for a clean run even when the step ultimately stops the pipeline.

Example: award 5 extra credit points if no forbidden symbols are used.

```python
from lograder.pipeline.check.source.source_check import SourceCheck

symbol_check = SourceCheck(...)
symbol_check.scorer = CleanRunScorer(0.0, extra_credit=5.0, label="No forbidden symbols")
```

---

## `PipelineScore`

`pipeline()` returns a `PipelineScore`.

```python
score: PipelineScore = pipeline()
```

**Key attributes:**

- `score.contributions` -- `list[tuple[Step, ScoreContribution]]` for all scored steps
- `score.total()` -- `ScoreContribution` summing all contributions

**`ScoreContribution` attributes:**

- `.earned` -- points earned (not including extra credit)
- `.possible` -- total points available
- `.extra_credit` -- extra credit earned
- `.total` -- `earned + extra_credit`

Steps **skipped by early pipeline exit** (e.g., a fatal build failure stops tests from running) still appear in `contributions` with `0/possible`. This means `score.total().possible` is always the full assignment total, regardless of how far the pipeline ran.

---

## `GradescopeTestConfig`

Attach per-step Gradescope metadata using `scorer.gradescope`:

```python
from lograder.pipeline.score import GradescopeTestConfig

tests.scorer = TestCaseScorer({"test_a": 10.0}, label="Correctness")
tests.scorer.gradescope = GradescopeTestConfig(
    visibility="after_due_date",
    number="1",
)
```

| Field | Type | Description |
|---|---|---|
| `output` | str \| None | Override the output text shown in Gradescope |
| `visibility` | str \| None | Per-test visibility override |
| `status` | `"passed"` \| `"failed"` \| None | Force a display status |
| `number` | str \| None | Display number for this test group |
| `tags` | list[str] \| None | Gradescope tags |
