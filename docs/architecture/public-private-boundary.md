# Public/Private Boundary

## What goes in `aprog-public`

- assignment statements (`README.md`)
- starter files (`assets/`)
- visible tests (`visible-tests/`)
- visible expected outputs (`expected/`)
- root classification config (`aprog.toml`)
- assignment templates (`templates/`)
- generated public manifests and autograder entry points (`generated/`)
- documentation

## What stays in `aprog-private`

- reference solutions (`solutions/`)
- hidden tests (`hidden-tests/`)
- grader pipelines (`grader/<slug>/pipeline.py`)
- generated private manifests and verification configs (`generated/`)

## What `aprog scan-public` catches

The scanner rejects suspicious filenames under `assignments/<slug>/`:

```text
solution.py, solution.cpp, solutions/
hidden-tests/, hidden_tests/, hidden/
private/, private-notes.md
answer-key.md, reference-solution.*
pipeline.py, grader/
```

CI runs `aprog scan-public --all` on every PR. If any of the above appear in a public PR, the build fails.
