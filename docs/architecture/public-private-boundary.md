# Public/Private Boundary

## Public files

These are allowed in `aprog-public`:

- assignment statements
- starter files
- visible tests
- visible expected outputs
- public assets
- root classification config
- assignment templates
- generated public assignment manifests
- generated autograder entry points (`run_autograder`, `run_autograder.py`)
- contributor documentation

## Private files

These must stay in `aprog-private`:

- reference solutions
- hidden tests
- hidden expected outputs
- contributor-authored grader pipelines (`grader/pipeline.py`)
- private solution notes
- maintainer notes
- generated private verification configs
- generated private manifests
- anything that reveals hidden grading behavior

## Mechanical matching

Assignments are matched by slug.

```text
aprog-public/assignments/<slug>/
aprog-private/solutions/<slug>/
aprog-private/hidden-tests/<slug>/
aprog-private/grader/<slug>/
```

No per-assignment TOML field should manually point to these private paths.

## Prohibited public names

The public validator should reject suspicious names under `assignments/<slug>/`.

Examples:

```text
solution.py
solution.cpp
solutions/
hidden-tests/
hidden_tests/
hidden/
private/
private-notes.md
answer-key.md
reference-solution.*
pipeline.py
grader/
```

## Intentional exceptions

Some words may be legitimate inside an assignment statement, for example "write a solution" in prose. The leak scanner should focus on paths and filenames first, then optionally scan contents.

Maintainer-only overrides should be explicit and auditable.

## Public assignment states

| State | Meaning |
|---|---|
| `draft` | Assignment exists but may be incomplete |
| `public-valid` | Public files pass validation |
| `private-missing` | No matching private grader or solution exists yet |
| `private-present` | Private solution and grader files exist |
| `verified` | Maintainer verification passes (reference solution earns full points) |
| `release-ready` | Generated configs are current and assignment is deployable |
