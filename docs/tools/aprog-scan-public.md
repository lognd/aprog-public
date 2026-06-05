# Tool Design: `aprog scan-public` and `aprog check-generated`

## `aprog scan-public`

Scans the public assignment directory for files that should not be committed to `aprog-public`.

```bash
aprog scan-public <assignment-slug>
aprog scan-public --all
```

Checks for:

- filenames matching the prohibited list (see `architecture/public-private-boundary.md`)
- directories named `solution`, `solutions`, `hidden`, `hidden-tests`, `private`, `grader`
- files named `pipeline.py` anywhere under `assignments/<slug>/`
- files with extensions matching reference solutions (`.py`, `.cpp`, `.c`, `.java`) that are not under `visible-tests/`, `assets/`, or have filenames starting with `solution`, `answer`, `reference`

Output on violation:

```text
ERROR: assignments/linked-list-insertion/solution.py — matches prohibited pattern 'solution.*'
ERROR: assignments/linked-list-insertion/grader/pipeline.py — 'grader/' directory is private
```

### Exit codes

| Code | Meaning |
|---:|---|
| 0 | No violations |
| 1 | Violations found |
| 2 | Usage error |

### Difference from `aprog validate`

`aprog validate` runs `scan-public` as one of its checks. Run `scan-public` directly to isolate public boundary issues without running full validation.

---

## `aprog check-generated`

Checks whether generated config files are current.

```bash
aprog check-generated <assignment-slug>
aprog check-generated --all
```

With private data:

```bash
aprog check-generated <assignment-slug> --private ../aprog-private
```

For each assignment, recomputes the source hash and compares it against the hash stored in `assignment-manifest.json`. Reports stale or missing generated files.

Output on stale:

```text
STALE: generated/assignments/linked-list-insertion/assignment-manifest.json
STALE: generated/assignments/linked-list-insertion/run_autograder.py
  Run: aprog generate-config linked-list-insertion
```

Output on missing:

```text
MISSING: generated/assignments/linked-list-insertion/assignment-manifest.json
  Run: aprog generate-config linked-list-insertion
```

### Exit codes

| Code | Meaning |
|---:|---|
| 0 | All generated files current |
| 1 | Stale or missing generated files |
| 2 | Usage error |
| 3 | Private repository required but unavailable |

`aprog validate` calls `check-generated` internally and returns exit code 4 when generated files are stale or missing. Run `check-generated` directly to focus on staleness without full validation.
