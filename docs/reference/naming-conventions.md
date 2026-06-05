# Naming Conventions

AProg should use boring, predictable names.

## General rules

Use kebab-case for repository paths and human-facing slugs.

Use snake_case for Python modules, functions, and variables.

Use uppercase snake_case for environment variables and GitHub secrets.

## Repository names

```text
aprog-public
aprog-private
```

## Assignment slugs

Assignment slugs use kebab-case.

Good:

```text
linked-list-insertion
binary-search-tree-traversal
matrix-chain-multiplication
```

Bad:

```text
LinkedListInsertion
linked_list_insertion
linkedListInsertion
```

## Directory names

Use:

```text
assignments/
visible-tests/
hidden-tests/
generated/
templates/
solutions/
expected/
assets/
```

Do not use:

```text
problems/
visible_tests/
hidden_tests/
testcases/
test-cases/
```

## File names

Use:

```text
assignment.toml
template.toml
assignment-manifest.json
private-assignment-manifest.json
run_autograder.py
verification-config.json
pipeline.py
```

## CLI command names

Use imperative, predictable verbs.

```text
aprog new
aprog validate
aprog scan-public
aprog check-generated
aprog list
aprog info
aprog templates list
aprog templates info
aprog package-public
aprog package-private
aprog package-gradescope
aprog submit
aprog intake
aprog generate-config
aprog verify
```

## Environment variables

```text
APROG_PUBLIC_REPO
APROG_PRIVATE_REPO
APROG_PRIVATE_URL
APROG_TEMPLATE_DIR
APROG_GENERATED_DIR
APROG_GPG_RECIPIENT
APROG_STAGING_DIR
APROG_INTAKE_URL
```

## GitHub secrets

```text
APROG_PRIVATE_DEPLOY_KEY
APROG_GPG_PRIVATE_KEY
APROG_GPG_PASSPHRASE
```

## Why avoid aliases?

Avoid supporting both `problem` and `assignment`, or both `hidden_tests` and `hidden-tests`. Aliases make docs harder to grep and validation harder to reason about.

The canonical word is assignment.
