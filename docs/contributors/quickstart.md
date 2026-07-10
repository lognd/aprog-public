# Contributor Quickstart

Complete walkthrough: creating an assignment from nothing to submitted private bundle.

Uses `linked-list-insertion` (Python, function-based) as the running example.

Before starting, complete [docs/setup/installation.md](../setup/installation.md) so that `aprog` is installed and `APROG_STAGING_DIR` is set.

---

## 0. Look at the examples first

Before writing any code, browse the complete worked examples in this repo. They show exactly what a finished assignment looks like -- including `pipeline.py`, hidden tests, and visible tests.

```text
examples/full-assignments/cpp-linked-list/   -- full C++ assignment (cpp-header-impl template)
examples/template-demos/                     -- one working demo per template
```

For `pipeline.py` authoring, the [lograder documentation](https://github.com/lognd/lograder) covers every step type, scorer, and configuration option.

---

## 1. Browse available templates

```bash
aprog templates list
aprog templates list --language python
aprog templates info python-function
```

Choose the template that matches your assignment type. See [docs/templates/template-catalog.md](../templates/template-catalog.md) for descriptions of all available templates and their expected file layouts.

For this walkthrough: `python-function` -- students implement one or more functions in a `.py` file.

---

## 2. Scaffold the assignment

```bash
aprog new linked-list-insertion --template python-function
```

Because `APROG_STAGING_DIR` is set, this creates files in two places:

**Public** (in `aprog-public/assignments/linked-list-insertion/`):

```text
assignment.toml          Assignment metadata
README.md                Assignment statement (fill this in)
visible-tests/
    test_visible.py      Tests students can see and run locally
assets/
    starter.py           Starter file handed to students
```

**Private** (in `~/aprog-staging/linked-list-insertion/`):

```text
solution/
    linked-list-insertion.py   Reference solution (fill this in)
hidden-tests/
    test_hidden.py             Hidden test cases (fill these in)
grader/
    pipeline.py                Grader pipeline (fill this in)
```

The private files are never committed to `aprog-public`. They travel to the maintainer via `aprog submit`.

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

Edit `author`, `description`, `topics`, `concepts`, and `difficulty`. Run `aprog list` to see registered topics. Leave `[grader]` defaults unless you need to change visibility.

---

## 4. Write the assignment statement (`README.md`)

Open `assignments/linked-list-insertion/README.md` and write the student-facing description. Include:

- what the student must implement (function name, signature, types)
- constraints and edge cases they must handle
- example inputs and expected outputs

---

## 5. Add visible tests

Edit `assignments/linked-list-insertion/visible-tests/test_visible.py`.

These tests are public -- students can see and run them locally. Keep them representative but not exhaustive (save the harder cases for hidden tests).

```python
from linked_list_insertion import insert

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

Fix any reported issues before opening a PR.

| Error | Fix |
|---|---|
| Slug mismatch | Directory name must match `slug` in `assignment.toml` |
| Unknown language/topic | Add the value to `aprog.toml` (maintainer task) or use an existing one |
| Missing README | Create `assignments/linked-list-insertion/README.md` |
| Generated files stale | Run `aprog generate-config linked-list-insertion` |

---

## 7. Open a public PR

Commit and push `assignments/linked-list-insertion/` to a branch and open a pull request. **Do not commit anything from `~/aprog-staging/`.** The CI workflow will run `aprog validate --all` automatically.

---

## 8. Write the reference solution

In `~/aprog-staging/linked-list-insertion/solution/linked-list-insertion.py`, implement the correct solution:

```python
def insert(lst, value):
    return lst + [value]
```

This is what `aprog verify` runs the grader pipeline against to confirm the grader works.

---

## 9. Write hidden tests

In `~/aprog-staging/linked-list-insertion/hidden-tests/test_hidden.py`, add test cases that students do not see until after the due date.

For `python-function` the hidden tests are pytest test functions that import the student's module directly. See the template scaffold and [lograder documentation](https://github.com/lognd/lograder) for the expected format.

---

## 10. Fill in `grader/pipeline.py`

Open `~/aprog-staging/linked-list-insertion/grader/pipeline.py`.

The template scaffold contains a working skeleton with placeholder test cases. Replace the placeholders with real inputs and point values.

**Before editing,** read:

- [lograder documentation](https://github.com/lognd/lograder) -- step types, scorers, build steps, and all available configuration
- [docs/grader/overview.md](../grader/overview.md) -- how the pipeline integrates with AProg
- `examples/template-demos/binary-search-staging/grader/pipeline.py` -- a complete `python-function` example

**Minimal example:**

```python
from pathlib import Path
from lograder.pipeline.input.local_directory import LocalDirectory
from lograder.pipeline.pipeline import Pipeline
from lograder.pipeline.test.pytest import PytestTest
from lograder.pipeline.score import TestCaseScorer, GimmeConfig

_GRADER_DIR = Path(__file__).parent
_HIDDEN_TESTS = _GRADER_DIR / "hidden-tests"

_POINTS = {
    "test_hidden::test_insert_into_empty": 10.0,
    "test_hidden::test_insert_at_end": 10.0,
    "test_hidden::test_insert_middle": 20.0,
}

def make_pipeline(submission_dir=Path("/autograder/submission")):
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

> **Gotchas** (see the template scaffold comments for details):
> - Score keys are `"module::function"` (e.g. `"test_hidden::test_name"`), not file paths.
> - Hidden tests can live in either of two places: embedded at `grader/<slug>/hidden-tests/`
>   (preferred -- the example above assumes this, since `_HIDDEN_TESTS` is resolved relative
>   to `grader/pipeline.py`), or as a sibling directory at `hidden-tests/<slug>/`. Both are
>   packaged automatically by `aprog package-gradescope`; pick whichever keeps your grader
>   pipeline's relative paths simplest.
> - PytestTest takes `paths=`, not `test_paths=`.

---

## 11. Submit the private bundle

```bash
aprog submit linked-list-insertion
```

`aprog submit` finds `~/aprog-staging/linked-list-insertion/` automatically (because `APROG_STAGING_DIR` is set). It packages the solution, hidden tests, and grader, then either sends the bundle to the maintainer or writes it to `dist/`.

If you need to package manually:

```bash
aprog package-private linked-list-insertion \
  --solution ~/aprog-staging/linked-list-insertion/solution \
  --hidden-tests ~/aprog-staging/linked-list-insertion/hidden-tests \
  --grader ~/aprog-staging/linked-list-insertion/grader
# Output: dist/linked-list-insertion-private.tar.gz
# Send this to the maintainer.
```

---

## 12. After submission -- maintainer steps

> **Maintainers only.** Requires access to `aprog-private`.

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

Verification passes when the reference solution earns full non-extra-credit points. If it fails, work with the contributor to fix the solution or grader, then re-intake and re-verify.

### 12c. Build and upload the Gradescope autograder

```bash
aprog generate-config linked-list-insertion --force

aprog package-gradescope linked-list-insertion \
  --public ../aprog-public \
  --private ../aprog-private
# Output: dist/linked-list-insertion-gradescope.zip
```

In Gradescope:
1. Open the course and find (or create) the programming assignment.
2. Go to **Configure Autograder** in the left sidebar.
3. Click **Upload Autograder** and select the zip file.
4. Click **Update Autograder** and wait for the build (1-3 minutes).
5. Use **Test Autograder** with the reference solution to confirm the score before students submit.

See [docs/maintainers/gradescope-upload.md](../maintainers/gradescope-upload.md) for the full upload guide.

---

## Summary of commands

```bash
# One-time setup (see docs/setup/installation.md)
pip install aprog
export APROG_STAGING_DIR=~/aprog-staging

# Browse templates
aprog templates list --language python
aprog templates info python-function

# Scaffold
aprog new linked-list-insertion --template python-function

# (edit assignment.toml, README.md, visible-tests/, solution/, hidden-tests/, grader/pipeline.py)

# Validate public files
aprog validate linked-list-insertion

# Open a PR, then submit the private bundle
aprog submit linked-list-insertion

# --- Maintainer steps (after intake) ---
aprog verify linked-list-insertion --public ../aprog-public --private ../aprog-private
aprog generate-config linked-list-insertion --force
aprog package-gradescope linked-list-insertion --public ../aprog-public --private ../aprog-private
# Upload dist/linked-list-insertion-gradescope.zip to Gradescope > Configure Autograder
```
