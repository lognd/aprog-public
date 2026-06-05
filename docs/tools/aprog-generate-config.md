# Tool Design: `aprog generate-config`

Generates normalized config artifacts.

## Usage

```bash
aprog generate-config <assignment-slug>
aprog generate-config --all
```

With private data:

```bash
aprog generate-config <assignment-slug> --private ../aprog-private
```

## Public outputs

```text
aprog-public/generated/assignments/<slug>/assignment-manifest.json
aprog-public/generated/assignments/<slug>/run_autograder.py
aprog-public/generated/assignments/<slug>/run_autograder
```

`run_autograder` is a shell shim that calls `run_autograder.py`. Gradescope invokes the shell file directly.

`run_autograder.py` is generated from the assignment's `[grader]` section in `assignment.toml`. It imports `make_pipeline` from `grader.pipeline` and wires it into lograder's `config()` context and `score.write_results_json()`. It does not implement grading logic.

## Private outputs

```text
aprog-private/generated/assignments/<slug>/private-assignment-manifest.json
aprog-private/generated/assignments/<slug>/verification-config.json
```

## Responsibilities

The command should:

- parse root config
- parse assignment config
- resolve classification values
- resolve template metadata
- inspect public paths
- inspect private paths when `--private` is provided
- compute source hashes
- write generated outputs
- refuse to overwrite generated outputs when the source hash is unchanged (use `--force` to override)

## What is not generated

`grader/pipeline.py` is contributor-authored. `aprog generate-config` does not create or modify it. The pipeline is the assignment-specific grading logic (test cases, artifact names, scoring weights) and cannot be derived from metadata alone.
