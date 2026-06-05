# Assignment TOML Schema

Per-assignment TOML describes the assignment identity and classification. It does not configure grading internals.

File:

```text
assignments/<assignment-slug>/assignment.toml
```

## Full example

```toml
[assignment]
slug = "linked-list-insertion"
name = "Linked List Insertion"
author = "your-github-handle"
description = "Insert values into a singly linked list."
version = "0.1.0"
status = "draft"

[classification]
language = "python"
difficulty = "medium"
topics = ["data-structures", "linked-lists"]
concepts = ["mutation"]
labels = ["unit-tests"]

[template]
slug = "python-function"
version = "0.1"

[grader]
visibility = "after_due_date"
stdout_visibility = "after_due_date"
```

## Required sections

- `[assignment]`
- `[classification]`
- `[template]`

## `[assignment]` fields

| Field | Type | Required | Rule |
|---|---|---|---|
| `slug` | string | yes | Must match directory name exactly |
| `name` | string | yes | Human-readable title |
| `author` | string | yes | GitHub handle of primary contributor |
| `description` | string | yes | One-line listing description |
| `version` | string | no | Semver string, e.g. `"0.1.0"` |
| `status` | string | no | See below |

### `status` values

| Value | Meaning |
|---|---|
| `"draft"` | Work in progress; may be incomplete |
| `"published"` | Complete and ready for students |

Default: `"draft"`. The validator does not block draft assignments, but they are excluded from `aprog list` unless `--status draft` is passed.

## `[classification]` fields

| Field | Type | Required | Rule |
|---|---|---|---|
| `language` | string | yes | Must be a key in `aprog.toml [classification.languages]` |
| `difficulty` | string | yes | Must be a key in `aprog.toml [classification.difficulties]` |
| `topics` | list of strings | yes | Non-empty; all values must be in `aprog.toml` |
| `concepts` | list of strings | no | All values must be in `aprog.toml` |
| `labels` | list of strings | no | All values must be in `aprog.toml [labels]` |
| `course` | string | no | Free-form course identifier, e.g. `"cop3502"` |
| `module` | string | no | Free-form module identifier, e.g. `"linked-lists"` |

## `[template]` fields

| Field | Type | Required | Rule |
|---|---|---|---|
| `slug` | string | yes | Must exist under `templates/<slug>/` |
| `version` | string | no | Template version used; informational only |

## `[grader]` fields

Controls Gradescope output visibility. Read by `aprog generate-config` and baked into `run_autograder.py`.

| Field | Type | Default | Allowed values |
|---|---|---|---|
| `visibility` | string | `"after_due_date"` | `"visible"`, `"hidden"`, `"after_due_date"`, `"after_published"` |
| `stdout_visibility` | string | `"after_due_date"` | same as `visibility` |

`[grader]` must not contain build commands, solution paths, point totals, or test case definitions. Those belong in `grader/pipeline.py`.

## `[grader.dependencies]` fields

Optional. Controls what `aprog package-gradescope` writes into `setup.sh`.

```toml
[grader.dependencies]
lograder = ">=0.1.0"
extra = ["numpy", "scipy"]
```

If omitted, `setup.sh` installs the latest `lograder` from PyPI.

## Forbidden fields

Do not add:

- `run_cmd`, `build_cmd`
- `solution_path`, `hidden_test_path`
- `points`, `hidden_cases`
- `stdout_visibility` at top level (must be under `[grader]`)
- `deploy_key`, `private_repo`
- `gradescope` (top-level — use `[grader]` instead)
