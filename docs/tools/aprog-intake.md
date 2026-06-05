# Tool Design: `aprog intake`

Maintainer command for importing private submissions.

## Usage

```bash
aprog intake dist/linked-list-insertion-private.tar.gz \
  --public ../aprog-public \
  --private ../aprog-private
```

Encrypted:

```bash
aprog intake dist/linked-list-insertion-private.tar.gz.gpg \
  --public ../aprog-public \
  --private ../aprog-private
```

## Responsibilities

`aprog intake` should:

- unpack or decrypt the bundle
- validate package manifest
- confirm assignment slug exists in public repo
- confirm `contains_grader` is true; reject bundle if `grader/pipeline.py` is missing
- copy solution into `aprog-private/solutions/<slug>/`
- copy hidden tests into `aprog-private/hidden-tests/<slug>/`
- copy grader into `aprog-private/grader/<slug>/`
- refuse to overwrite existing private files unless `--force` is passed
- optionally run full validation with `--validate`
- optionally generate private configs with `--generate`

## Non-responsibilities

`aprog intake` should not:

- merge GitHub PRs
- grant repository access
- publish hidden tests
- modify public assignment files unless explicitly requested
