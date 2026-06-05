# Tool Design: `aprog validate`

Validates assignment structure and metadata.

## Usage

```bash
aprog validate <assignment-slug>
aprog validate --all
```

With private repository:

```bash
aprog validate <assignment-slug> --private ../aprog-private
```

## Public validation

Public validation checks:

- assignment exists
- assignment TOML parses
- slug matches directory
- classification values are known
- selected template exists
- README exists
- visible tests exist
- public/private boundary is not violated
- generated public configs are current, if required

## Private validation

Private validation checks:

- matching solution directory exists
- matching hidden-tests directory is valid, if present
- generated private configs are current
- private slug matches public slug

## Exit codes

| Code | Meaning |
|---:|---|
| 0 | Valid |
| 1 | Validation failed |
| 2 | Usage error |
| 3 | Private repository required but unavailable |
| 4 | Generated files stale |
