# Contributor Quickstart

Complete walkthrough: creating an assignment from nothing to submitted private bundle.

Uses `linked-list-insertion` (Python, function-based) as the running example.

---

## 0. Prerequisites

Install AProg:

```bash
pip install aprog
```

Set a staging directory for private working files (so they are never in `aprog-public`):

```bash
export APROG_STAGING_DIR=~/aprog-staging
```

This persists in your shell profile. `aprog new` will create private skeletons at `$APROG_STAGING_DIR/<slug>/`.

---

## 1. Browse available templates

```bash
aprog templates list --language python
aprog templates info python-function
```

For a Python assignment where students implement functions: `python-function`.

---

## 2. Scaffold the assignment

```bash
aprog new linked-list-insertion --template python-function
```

Because `APROG_STAGING_DIR` is set, this creates both:

**Public** (in `aprog-public`):

```text
assignments/linked-list-insertion/
├── assignment.toml
├── README.md
├── visible-tests/
│   └── test_visible.py
├── expected/
└── assets/
    └── starter.py
```

**Private** (in `$APROG_STAGING_DIR`):

```text
~/aprog-staging/linked-list-insertion/
├── solution/
│   └── solution.py
├── hidden-tests/
│   └── tests/
│       └── test_hidden.py
└── grader/
    └── pipeline.py
```

---

## 3. Fill in `assignment.toml`

Open `assignments/linked-list-insertion/assignment.toml`:

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
labels = []

[template]
slug = "python-function"

[grader]
visibility = "after_due_date"
stdout_visibility = "after_due_date"
```

Edit `author`, `description`, `topics`, `concepts`, and `difficulty`. Use `aprog list --status draft` to see your registered topics. Leave `[grader]` defaults unless you need to change visibility.

---

## 4. Fill in `README.md`

Write the assignment statement. Include:

- what the student must implement
- function signature(s) and types
- constraints and edge cases
- example inputs and expected outputs

---

## 5. Add visible tests

Edit `assignments/linked-list-insertion/visible-tests/test_visible.py`.

These tests are public — students can see and run them. Keep them representative but not exhaustive.

```python
from starter import insert

def test_insert_into_empty():
    assert insert([], 1) == [1]

def test_insert_at_end():
    assert insert([1, 2], 3) == [1, 2, 3]
```

---

## 6. Validate the public files

```bash
aprog validate linked-list-insertion
```

Common issues:

| Error | Fix |
|---|---|
| Slug mismatch | Directory name must match `slug` in `assignment.toml` |
| Unknown language/topic | Add the value to `aprog.toml` (maintainer) |
| Missing README | Create `assignments/linked-list-insertion/README.md` |
| Generated files stale | Run `aprog generate-config linked-list-insertion` |

---

## 7. Open a public PR

Commit and push the `assignments/linked-list-insertion/` directory to a branch and open a pull request. Do not commit anything from `~/aprog-staging/`.

---

## 8. Write the reference solution

In `~/aprog-staging/linked-list-insertion/solution/solution.py`, implement the correct solution:

```python
def insert(lst, value):
    return lst + [value]
```

This is what `aprog verify` runs the grader pipeline against.

---

## 9. Write hidden tests

In `~/aprog-staging/linked-list-insertion/hidden-tests/tests/`, add test inputs that students do not see.

For a Python function assignment, hidden tests are typically additional inputs the grader passes to the student's code. The exact format depends on how `pipeline.py` invokes the artifact.

---

## 10. Fill in `grader/pipeline.py`

Open `~/aprog-staging/linked-list-insertion/grader/pipeline.py`. Replace the placeholder cases:

```python
from lograder.pipeline.input.local_directory import LocalDirectory
from lograder.pipeline.pipeline import Pipeline
from lograder.pipeline.test.output_compare import OutputCompareTest, OutputCompareCase
from lograder.pipeline.score import TestCaseScorer

_CASES = [
    OutputCompareCase(
        name="insert_empty",
        args=[],
        stdin="[] 1\n",
        expected_stdout="[1]\n",
    ),
    OutputCompareCase(
        name="insert_end",
        args=[],
        stdin="[1, 2] 3\n",
        expected_stdout="[1, 2, 3]\n",
    ),
    OutputCompareCase(
        name="insert_middle",
        args=[],
        stdin="[1, 3] 2\n",
        expected_stdout="[1, 2, 3]\n",
    ),
]

_SCORER = TestCaseScorer(
    points_per_case={
        "insert_empty": 10.0,
        "insert_end": 10.0,
        "insert_middle": 20.0,
    },
    label="Linked List Insertion",
)


def make_pipeline() -> Pipeline:
    step = LocalDirectory()
    tests = OutputCompareTest("solution.py", _CASES)
    tests.scorer = _SCORER
    return Pipeline([step, tests])
```

See `docs/grader/steps.md` and `docs/grader/scoring.md` for the full step and scorer reference.

---

## 11. Submit the private bundle

```bash
aprog submit linked-list-insertion
```

Because `APROG_STAGING_DIR` is set, `aprog submit` finds the staging directory automatically. It runs `aprog package-private` and either prints the bundle path or uploads it if `APROG_INTAKE_URL` is configured.

If the maintainer uses a manual intake process:

```bash
aprog package-private linked-list-insertion \
  --solution ~/aprog-staging/linked-list-insertion/solution \
  --hidden-tests ~/aprog-staging/linked-list-insertion/hidden-tests \
  --grader ~/aprog-staging/linked-list-insertion/grader
# Output: dist/linked-list-insertion-private.tar.gz
# Send this file to the maintainer.
```

---

## 12. After submission (maintainer steps)

> **Staff / maintainers only.** Requires access to `aprog-private`.

### 12a. Intake the private bundle

```bash
aprog intake dist/linked-list-insertion-private.tar.gz \
  --public ../aprog-public \
  --private ../aprog-private
```

### 12b. Verify the reference solution

```bash
aprog verify linked-list-insertion \
  --public ../aprog-public \
  --private ../aprog-private
```

Verification passes when the reference solution earns full non-extra-credit points on all test cases. If it fails, work with the contributor to fix the solution or grader, then re-intake and re-verify.

### 12c. Build and upload the Gradescope autograder

Once verification passes:

```bash
# Ensure generated files are current
aprog generate-config linked-list-insertion --force

# Build the Gradescope zip
aprog package-gradescope linked-list-insertion \
  --public ../aprog-public \
  --private ../aprog-private
# Output: dist/linked-list-insertion-gradescope.zip
```

Then in Gradescope:

1. Open the course and find (or create) the programming assignment.
2. Go to **Configure Autograder** in the left sidebar.
3. Click **Upload Autograder** and select `dist/linked-list-insertion-gradescope.zip`.
4. Click **Update Autograder** and wait for the build (1–3 minutes).
5. Use **Test Autograder** with the reference solution to confirm the score is correct before students submit.

See `docs/maintainers/gradescope-upload.md` for the full upload guide and troubleshooting.

---

## Summary of commands

```bash
# One-time setup
export APROG_STAGING_DIR=~/aprog-staging

# Discover templates
aprog templates list --language python

# Scaffold
aprog new linked-list-insertion --template python-function

# Validate public files
aprog validate linked-list-insertion

# (edit assignment.toml, README.md, visible-tests/, grader/pipeline.py, solution/)

# Submit private bundle
aprog submit linked-list-insertion

# --- Maintainer steps (after intake) ---
aprog verify linked-list-insertion --public ../aprog-public --private ../aprog-private
aprog generate-config linked-list-insertion --force
aprog package-gradescope linked-list-insertion --public ../aprog-public --private ../aprog-private
# Upload dist/linked-list-insertion-gradescope.zip to Gradescope > Configure Autograder
```
