# Gradescope Upload Guide

How to build and deploy a finished autograder to Gradescope.

This guide is for **maintainers** (staff with access to both `aprog-public` and `aprog-private`). It picks up after verification passes.

---

## Prerequisites

- Both repositories cloned side-by-side:
  ```
  Projects/
  ├── aprog-public/
  └── aprog-private/
  ```
- `aprog` installed in your environment (`pip install aprog` or via the local venv)
- Verification already passing for the assignment (`aprog verify`)
- Access to the Gradescope course

---

## Step 1 — Regenerate configs (if stale)

```bash
cd aprog-public
aprog generate-config <slug> --force
```

This ensures `generated/assignments/<slug>/run_autograder` and `run_autograder.py` are current. Skip if `aprog validate <slug>` reports no stale-config errors.

---

## Step 2 — Verify the reference solution

If you have not already done so (or if anything changed since last verification):

```bash
aprog verify <slug> --public . --private ../aprog-private
```

Verification must pass before deploying. A failed deploy will silently give every student 0.

---

## Step 3 — Build the Gradescope zip

```bash
aprog package-gradescope <slug> \
  --public . \
  --private ../aprog-private
```

Output:

```
dist/<slug>-gradescope.zip
```

The zip contains:

| File | Source |
|---|---|
| `setup.sh` | Generated from `[grader.dependencies]` in `assignment.toml` |
| `run_autograder` | `generated/assignments/<slug>/run_autograder` |
| `run_autograder.py` | `generated/assignments/<slug>/run_autograder.py` |
| `grader/pipeline.py` | `aprog-private/grader/<slug>/pipeline.py` |
| `hidden-tests/` | `aprog-private/hidden-tests/<slug>/` (if present) |

---

## Step 4 — Upload to Gradescope

1. Go to **gradescope.com** and open the course.
2. Open (or create) the programming assignment.
3. Click **Configure Autograder** in the left sidebar.
4. Click **Upload Autograder** (or **Replace Autograder** if one already exists).
5. Select `dist/<slug>-gradescope.zip`.
6. Click **Update Autograder** and wait for the build to finish (usually 1–3 minutes).

> **Tip:** After the build completes, use **Test Autograder** with the reference solution to confirm scores before the assignment opens to students.

---

## Step 5 — Test with the reference solution

In Gradescope, go to **Test Autograder**:

1. Upload the file(s) from `aprog-private/solutions/<slug>/`.
2. Click **Run Autograder**.
3. Confirm the score matches the expected total (e.g., 100/100).

If the score is wrong, check the autograder logs in Gradescope and re-run `aprog verify` locally to diagnose.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Build fails on Gradescope | Bad `setup.sh` or missing dependency | Check `[grader.dependencies]` in `assignment.toml`; add missing packages to `extra` |
| Score is 0 for all submissions | Compile error in grader or wrong file path | Check Gradescope logs; re-run `aprog verify` locally |
| Reference solution scores less than 100 | Solution or grader bug | Fix in `aprog-private`, re-verify, re-package, re-upload |
| "Artifact not found" in logs | Wrong artifact name in `pipeline.py` | Ensure the artifact key in `_CompileStep` matches the name passed to `OutputCompareTest` |
| Stale config warning during package | `generate-config` not run | Run `aprog generate-config <slug> --force` before packaging |

---

## Full command sequence (copy-paste)

```bash
cd aprog-public

# 1. Ensure generated files are current
aprog generate-config <slug> --force

# 2. Verify reference solution passes
aprog verify <slug> --public . --private ../aprog-private

# 3. Build the Gradescope zip
aprog package-gradescope <slug> --public . --private ../aprog-private

# 4. Upload dist/<slug>-gradescope.zip in Gradescope > Configure Autograder
```
