# Architecture Overview

## Repositories

AProg uses two repositories:

| Repository | Visibility | Purpose |
|---|---:|---|
| `aprog-public` | Public | Public assignment definitions, visible tests, starter assets, templates, docs, generated public configs |
| `aprog-private` | Private | Reference solutions, hidden tests, contributor-authored grader pipelines, private generated configs, maintainer-only artifacts |

The repositories are matched by assignment slug.

```text
aprog-public/assignments/<assignment-slug>/
aprog-private/solutions/<assignment-slug>/
aprog-private/hidden-tests/<assignment-slug>/
aprog-private/grader/<assignment-slug>/
```

## Design constraints

1. Keep per-assignment TOML small.
2. Do not put grader behavior in per-assignment TOML (except Gradescope visibility settings).
3. Make assignment creation template-driven.
4. Make naming predictable enough that contributors can guess it.
5. Keep public and private files mechanically separable.
6. Generate configs instead of hand-editing them.

## Major concepts

| Concept | Description |
|---|---|
| Assignment | A single problem/project/exercise submitted to the repository |
| Template | A contributor-facing scaffold used to create a new assignment |
| Classification | Structured metadata used for discovery and filtering |
| Generated config | Reproducible output derived from metadata, files, templates, and integration rules |
| Public files | Files safe for students/contributors to read |
| Private files | Files containing solutions, hidden tests, grader pipelines, or maintainer-only data |

## What AProg owns

AProg owns repository orchestration:

- directory layout
- assignment identity
- assignment classification
- template selection
- file generation
- public/private boundary checks
- generated manifest/config placement
- GitHub Actions workflows
- contributor upload/intake process

## What the grader package owns

The grader package (`lograder`) owns:

- platform-agnostic subprocess execution and sandboxing
- the `Pipeline` / `Step` protocol and data flow
- build steps (`CMakeBuild`, `MakefileBuild`, `BashScriptBuild`, `PrebuiltArtifacts`)
- test steps (`OutputCompareTest`, `ValgrindTest`, `FileOutputTest`, `PerformanceTest`, `DifferentialTest`)
- scoring (`TestCaseScorer`, `AllOrNothingScorer`, `CleanRunScorer`)
- result generation (`PipelineScore`, `write_results_json`)
- Gradescope output format (`GradescopeConfig`, `GradescopeTestConfig`)

The grader is invoked through `make_pipeline()` in the contributor-authored `grader/pipeline.py`. AProg generates the surrounding entry point (`run_autograder.py`) but does not generate the pipeline itself.
