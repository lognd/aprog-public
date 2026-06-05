# Generated Configs

Generated configs are reproducible files derived from:

- `aprog.toml`
- `assignment.toml`
- assignment template metadata
- public file layout
- private file layout, if available
- AProg generation code

Generated configs should not be hand-edited.

## Public generated files

Public generated files live in:

```text
aprog-public/generated/assignments/<assignment-slug>/
```

Files:

```text
assignment-manifest.json
run_autograder.py
```

## Private generated files

Private generated files live in:

```text
aprog-private/generated/assignments/<assignment-slug>/
```

Files:

```text
private-assignment-manifest.json
verification-config.json
```

## Public assignment manifest

`assignment-manifest.json` is a normalized, generated representation of the public assignment.

It should contain:

- assignment slug
- display name
- author
- classification values
- selected template
- public paths
- generated config version
- source hash
- public validation state

Example:

```json
{
  "schema_version": "0.1",
  "assignment": {
    "slug": "linked-list-insertion",
    "name": "Linked List Insertion",
    "author": "github-handle",
    "description": "Insert values into a linked list."
  },
  "classification": {
    "language": "python",
    "difficulty": "medium",
    "topics": ["data-structures", "linked-lists"],
    "course": null
  },
  "template": {
    "slug": "python-stdin-stdout",
    "version": "0.1"
  },
  "paths": {
    "assignment_root": "assignments/linked-list-insertion",
    "readme": "assignments/linked-list-insertion/README.md",
    "visible_tests": "assignments/linked-list-insertion/visible-tests"
  },
  "state": "public-valid",
  "source_hash": "sha256:..."
}
```

## Autograder entry point

`run_autograder.py` is the generated Gradescope entry point.

It is a thin boilerplate file. It does not implement grading logic. Grading logic lives in the contributor-authored `grader/pipeline.py`, which `run_autograder.py` imports.

Responsibilities of `run_autograder.py`:

- read Gradescope visibility and output settings from the generated manifest
- set up `EnvironmentConfig` using Gradescope paths (`/autograder/submission`)
- import `make_pipeline` from `grader.pipeline`
- call the pipeline
- call `score.write_results_json()` with the configured `GradescopeConfig`

Example:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from lograder.pipeline.config import config
from lograder.pipeline.score import GradescopeConfig

from grader.pipeline import make_pipeline

if __name__ == "__main__":
    with config(root_directory=Path("/autograder/submission")):
        pipeline = make_pipeline()
        score = pipeline()
        score.write_results_json(
            config=GradescopeConfig(
                visibility="after_due_date",
                stdout_visibility="after_due_date",
            )
        )
```

The visibility settings are read from the assignment's `[grader]` section in `assignment.toml`.

`run_autograder.py` must be accompanied by a `run_autograder` shell shim:

```bash
#!/usr/bin/env bash
exec python3 "$(dirname "$0")/run_autograder.py" "$@"
```

Gradescope calls the `run_autograder` shell file directly.

## Contributor-authored grader

`grader/pipeline.py` is **not generated**. It is scaffolded from the template and filled in by the contributor.

It must export a `make_pipeline() -> Pipeline` function.

Example:

```python
from lograder.pipeline.input.local_directory import LocalDirectory
from lograder.pipeline.pipeline import Pipeline
from lograder.pipeline.test.output_compare import OutputCompareTest, OutputCompareCase
from lograder.pipeline.score import TestCaseScorer

def make_pipeline() -> Pipeline:
    step = LocalDirectory()
    cases = [
        OutputCompareCase(
            name="test_hello",
            args=[],
            stdin="hello\n",
            expected_stdout="hello\n",
        ),
    ]
    tests = OutputCompareTest("solution", cases)
    tests.scorer = TestCaseScorer({"test_hello": 10.0}, label="Correctness")
    return Pipeline([step, tests])
```

The grader file lives in `aprog-private` and is included in the private bundle.

## Private verification config

`verification-config.json` is maintainer-only.

It contains the information needed to run `aprog verify` without manually specifying paths.

Example:

```json
{
  "schema_version": "0.1",
  "assignment_slug": "linked-list-insertion",
  "solution_path": "solutions/linked-list-insertion",
  "hidden_tests_path": "hidden-tests/linked-list-insertion",
  "grader_path": "grader/linked-list-insertion",
  "has_solution": true,
  "has_hidden_tests": true,
  "private_source_hash": "sha256:...",
  "verification_state": "unverified"
}
```

`verification_state` values:

| Value | Meaning |
|---|---|
| `unverified` | Configs generated but `aprog verify` has not passed |
| `verified` | `aprog verify` passed at the hash recorded in `private_source_hash` |
| `stale` | Source hash has changed since last verification |

## Source hash

Generated files should record a source hash to detect staleness.

Hash inputs for public configs:

- root `aprog.toml`
- assignment `assignment.toml`
- template `template.toml`
- public file list
- generator version

Hash inputs for private configs:

All public inputs, plus:

- private file list
- grader file list

## Regeneration commands

```bash
aprog generate-config <assignment-slug>
aprog generate-config --all
aprog check-generated <assignment-slug>
aprog check-generated --all
```
