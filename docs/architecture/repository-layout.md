# Repository Layout

## `aprog-public`

```text
aprog-public/
|-- aprog.toml
|-- assignments/
|   `-- <assignment-slug>/
|       |-- assignment.toml
|       |-- README.md
|       |-- visible-tests/
|       |-- expected/
|       `-- assets/
|-- templates/
|   `-- <template-slug>/
|       |-- template.toml
|       |-- README.md
|       |-- public/
|       `-- private/
|-- generated/
|   `-- assignments/
|       `-- <assignment-slug>/
|           |-- assignment-manifest.json
|           |-- run_autograder
|           `-- run_autograder.py
|-- tools/
|-- docs/
|-- scripts/
`-- .github/
```

## `aprog-private`

```text
aprog-private/
|-- solutions/
|   `-- <assignment-slug>/
|-- hidden-tests/
|   `-- <assignment-slug>/
|       |-- tests/
|       |-- expected/
|       `-- assets/
|-- grader/
|   `-- <assignment-slug>/
|       `-- pipeline.py
|-- generated/
|   `-- assignments/
|       `-- <assignment-slug>/
|           |-- private-assignment-manifest.json
|           `-- verification-config.json
`-- maintainer/
```

## Naming Convention

Repository directories intended for humans use lowercase kebab-case:

```text
visible-tests/
hidden-tests/
assignment-manifest.json
run_autograder.py
```

Python modules still use snake_case:

```text
aprog_cli.py
generate_config.py
validate_assignment.py
pipeline.py
```
