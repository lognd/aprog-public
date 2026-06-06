# Architecture Overview

AProg uses two repositories matched by assignment slug:

| Repository | Visibility | Contents |
|---|---|---|
| `aprog-public` | Public | Assignment statements, visible tests, starter assets, templates, generated configs, docs |
| `aprog-private` | Private | Reference solutions, hidden tests, grader pipelines, private generated configs |

```text
aprog-public/assignments/<slug>/
aprog-private/solutions/<slug>/
aprog-private/hidden-tests/<slug>/
aprog-private/grader/<slug>/
```

## AProg vs lograder

**AProg** owns the repository layer: directory layout, assignment identity, classification, template scaffolding, public/private boundary enforcement, contributor upload, maintainer intake, config generation, and CI.

**lograder** owns the grading layer: the `Pipeline`/`Step` protocol, build steps, test steps, scoring, and Gradescope output formatting. See the [lograder documentation](https://github.com/lognd/lograder).

AProg generates `run_autograder.py` (the Gradescope entry point) from `assignment.toml` settings, but the grading logic itself is contributor-authored in `grader/pipeline.py` using lograder directly.
