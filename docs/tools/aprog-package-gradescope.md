# Tool Design: `aprog package-gradescope`

Builds a Gradescope-deployable zip from generated and private files.

This is a maintainer command. It requires access to both `aprog-public` (for generated files) and `aprog-private` (for the grader pipeline, hidden tests, and expected outputs).

## Usage

```bash
aprog package-gradescope <assignment-slug> \
  --public ../aprog-public \
  --private ../aprog-private
```

Output:

```text
dist/<assignment-slug>-gradescope.zip
```

## Requirements

Before running, the following must exist and be current:

- `aprog-public/generated/assignments/<slug>/run_autograder.py` (from `aprog generate-config`)
- `aprog-public/generated/assignments/<slug>/run_autograder` (shell shim)
- `aprog-private/grader/<slug>/pipeline.py`
- `aprog-private/hidden-tests/<slug>/` (if the assignment uses hidden tests)

Run `aprog generate-config <slug> --private ../aprog-private` first if generated files are missing or stale.

## Gradescope zip layout

```text
setup.sh
run_autograder
run_autograder.py
grader/
    pipeline.py
hidden-tests/
    tests/
    expected/
    assets/
```

## `setup.sh`

`aprog package-gradescope` generates a `setup.sh` that installs lograder and any other required dependencies.

Default generated `setup.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
pip install lograder
```

To install a specific version or additional packages, set `[grader.dependencies]` in `assignment.toml`:

```toml
[grader.dependencies]
lograder = ">=0.1.0"
extra = ["numpy"]
```

Generated `setup.sh` for the above:

```bash
#!/usr/bin/env bash
set -euo pipefail
pip install "lograder>=0.1.0" numpy
```

## Deploying to Gradescope

After building the zip, upload it to Gradescope:

1. Open the assignment in Gradescope.
2. Go to **Configure Autograder**.
3. Upload `dist/<slug>-gradescope.zip`.
4. Click **Update Autograder**.

Gradescope will run `setup.sh` to prepare the environment, then call `run_autograder` for each student submission.

## Relationship to CI

`aprog package-gradescope` is typically run manually by a maintainer after verification passes. It is not run on every PR. To automate it, add a `workflow_dispatch` GitHub Actions workflow that runs it and stores the zip as a workflow artifact.
