# Config Reference

## `EnvironmentConfig`

`run_autograder.py` sets up `EnvironmentConfig` before calling `make_pipeline()`. Contributors do not need to configure this — it is handled by the generated entry point.

Relevant fields (for awareness when writing `pipeline.py`):

| Field | Type | Description |
|---|---|---|
| `root_directory` | Path | Where the student submission lives. Set to `/autograder/submission` in production. |
| `executable_timeout` | float \| None | Default timeout for subprocess calls. `None` means no limit. |
| `executable_max_workers` | int | Max parallel subprocesses. Default: 16. |

`LocalDirectory` reads `root_directory` from the active config at call time. Do not hardcode paths in `pipeline.py`.

### Reading config in `pipeline.py` (rare)

If `pipeline.py` needs to read config (e.g., to compute a path relative to the submission):

```python
from lograder.pipeline.config import get_config

config = get_config()
submission_root = config.root_directory
```

---

## `GradescopeConfig`

Used by `run_autograder.py` when calling `score.write_results_json()`. Contributors do not set this directly — it is generated from the `[grader]` section in `assignment.toml`.

Shown here for reference:

```python
from lograder.pipeline.score import GradescopeConfig

GradescopeConfig(
    visibility="after_due_date",         # overall result visibility
    stdout_visibility="after_due_date",  # stdout visibility
    output_format="text",                # "text" | "html" | "simple_format" | "md" | "ansi"
    output="",                           # header string shown at top of Gradescope output
    execution_time=None,                 # optional reported execution time
)
```

The `visibility` and `stdout_visibility` values come from `assignment.toml`:

```toml
[grader]
visibility = "after_due_date"
stdout_visibility = "after_due_date"
```

Allowed values for both fields:

| Value | When results are shown |
|---|---|
| `"visible"` | Immediately after submission |
| `"hidden"` | Never shown to students |
| `"after_due_date"` | After the assignment due date |
| `"after_published"` | After the instructor publishes grades |

---

## `score.write_results_json()`

Writes `/autograder/results/results.json`. Called by the generated `run_autograder.py`.

```python
score.write_results_json(
    config=GradescopeConfig(...),
    output="",   # optional header text
    path=None,   # override output path (default: /autograder/results/results.json)
)
```

Creates parent directories automatically. If the pipeline produced no scored steps, the output file is still written with an empty test list.
