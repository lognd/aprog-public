# Contributor Guide

## Quick start

```bash
aprog templates list
aprog new linked-list-insertion --template python-function
aprog validate linked-list-insertion
```

## Contributor workflow

1. Pick a template.
2. Generate an assignment scaffold.
3. Fill in `assignment.toml`.
4. Fill in `README.md`.
5. Add visible tests.
6. Run validation.
7. Open a public PR.
8. Fill in `grader/pipeline.py` from the private template skeleton.
9. Submit the private bundle.

## Pick a template

```bash
aprog templates list --language python
aprog templates info python-function
```

## Create an assignment

```bash
aprog new linked-list-insertion --template python-function
```

## Edit classification

```toml
[classification]
language = "python"
difficulty = "medium"
topics = ["data-structures", "linked-lists"]
concepts = ["mutation"]
labels = ["unit-tests"]
```

## Do not commit private files

Never commit:

- solutions
- hidden tests
- answer keys
- private notes
- generated private configs
- `grader/pipeline.py`

## Fill in the grader pipeline

The private template skeleton includes `grader/pipeline.py`. This file defines the lograder `Pipeline` for your assignment. You must:

- replace the placeholder test cases with real inputs and expected outputs
- set point values in the scorer
- add a build step if the assignment requires compilation

The pipeline file stays private. It is submitted in the private bundle.

## Submit private solution

Package the private bundle:

```bash
aprog package-private linked-list-insertion \
  --solution path/to/your/solution \
  --hidden-tests path/to/hidden-tests \
  --grader path/to/grader
```

Then follow the private submission workflow documented by maintainers.

Expected private bundle shape:

```text
<slug>/
|-- package-manifest.json
|-- solution/
|-- hidden-tests/
`-- grader/
    `-- pipeline.py
```
