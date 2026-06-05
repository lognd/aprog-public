# Tool Design: `aprog new`

Creates a new assignment scaffold from a template.

## Usage

```bash
aprog new <assignment-slug> --template <template-slug>
```

Example:

```bash
aprog new linked-list-insertion --template python-function
```

Optional classification flags:

```bash
aprog new linked-list-insertion \
  --template python-function \
  --difficulty medium \
  --topic data-structures \
  --topic linked-lists
```

## Public output

Always creates public files under `assignments/<slug>/`:

```text
assignments/linked-list-insertion/
├── assignment.toml
├── README.md
├── visible-tests/
│   └── test_visible.py
├── expected/
└── assets/
    └── starter.py
```

The generated `assignment.toml` is pre-filled with the slug, template slug, and any classification flags provided on the command line. Fields that require human input (name, description, author) are left as placeholder strings.

## Private staging output

Pass `--staging-dir <path>` to also render the private template skeleton:

```bash
aprog new linked-list-insertion \
  --template python-function \
  --staging-dir ../my-staging
```

This creates:

```text
../my-staging/linked-list-insertion/
├── solution/
│   └── solution.py
├── hidden-tests/
│   └── tests/
│       └── test_hidden.py
└── grader/
    └── pipeline.py
```

`pipeline.py` is the template's `grader/pipeline.py.j2` scaffold, ready to be filled in. It is the contributor's responsibility to complete it before packaging the private bundle.

### Staging directory resolution

The staging directory is resolved in this order:

1. `--staging-dir <path>` flag
2. `APROG_STAGING_DIR` environment variable
3. `../aprog-staging` (default fallback, relative to the aprog-public root)

If the staging directory does not exist, `aprog new` creates it.

## Responsibilities

`aprog new` should:

- validate the assignment slug (kebab-case, no reserved words)
- validate the template slug exists
- create `assignments/<slug>/` with public template files
- generate initial `assignment.toml` with pre-filled values
- render the private staging skeleton if `--staging-dir` is provided (explicit or via env)
- refuse to overwrite an existing assignment unless `--force` is passed

## Non-responsibilities

`aprog new` should not:

- write any private files into `assignments/<slug>/`
- generate configs (`run_autograder.py`, manifests)
- run validation
- require access to `aprog-private`

## Output

```text
Created: assignments/linked-list-insertion/
Staging: ../aprog-staging/linked-list-insertion/   (private working directory)

Next steps:
  1. Edit assignments/linked-list-insertion/README.md
  2. Fill in assignments/linked-list-insertion/assignment.toml
  3. Add visible tests to assignments/linked-list-insertion/visible-tests/
  4. Fill in ../aprog-staging/linked-list-insertion/grader/pipeline.py
  5. Run: aprog validate linked-list-insertion
```

If `--staging-dir` is not provided and `APROG_STAGING_DIR` is not set, the staging output line is shown but notes that the default location was used.
