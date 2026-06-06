# Generated Configs

Files under `generated/` are produced by `aprog generate-config` and committed to the repo. Do not hand-edit them -- they will be overwritten on next regeneration and CI will fail if they are stale.

## What gets generated

**In `aprog-public/generated/assignments/<slug>/`:**

| File | Purpose |
|---|---|
| `assignment-manifest.json` | Normalized metadata snapshot (slug, name, author, classification, paths, source hash) |
| `run_autograder.py` | Gradescope entry point -- imports `make_pipeline` from `grader/pipeline.py` and calls it |
| `run_autograder` | Shell shim that Gradescope calls directly |

**In `aprog-private/generated/assignments/<slug>/`:**

| File | Purpose |
|---|---|
| `private-assignment-manifest.json` | Private counterpart to the public manifest |
| `verification-config.json` | Records paths and verification state for `aprog verify` |

## Regenerating

```bash
aprog generate-config <slug> --force
aprog generate-config --all --force

# Check whether generated files are current without regenerating
aprog check-generated <slug>
aprog check-generated --all
```

CI runs `aprog check-generated --all` on every PR and fails if any generated file is stale.

## What `run_autograder.py` does

The generated entry point is a thin wrapper. It does not contain grading logic. On execution it:

1. Adds the source directory to `sys.path`.
2. Creates a `GraderMetadata` object from the assignment name and author in `assignment.toml`.
3. Calls `make_pipeline(submission_dir=Path("/autograder/submission"))`.
4. Calls `pipeline(metadata=metadata)` to run grading.
5. Calls `score.write_results_json()` with the visibility settings from `assignment.toml [grader]`.

All grading logic is in the contributor-authored `grader/pipeline.py`.
