# Tool Design: Packaging Commands

AProg has separate public and private packaging commands.

## `aprog package-public`

Creates a public-safe assignment bundle.

```bash
aprog package-public <assignment-slug>
```

Output:

```text
dist/<assignment-slug>-public.tar.gz
```

Includes:

- `assignment.toml`
- `README.md`
- visible tests
- public expected files
- assets
- public generated manifest, if current

Excludes:

- solutions
- hidden tests
- private configs
- grader pipeline

## `aprog package-private`

Creates a private solution/hidden-test bundle.

```bash
aprog package-private <assignment-slug> \
  --solution path/to/solution-dir \
  --hidden-tests path/to/hidden-tests-dir \
  --grader path/to/grader-dir
```

Output:

```text
dist/<assignment-slug>-private.tar.gz
```

Optional encrypted output:

```text
dist/<assignment-slug>-private.tar.gz.gpg
```

## Private bundle layout

```text
<assignment-slug>/
├── package-manifest.json
├── solution/
├── hidden-tests/
└── grader/
    └── pipeline.py
```

`grader/pipeline.py` is the contributor-authored lograder pipeline definition. It must export `make_pipeline() -> Pipeline`. It is required for `aprog intake` to complete and for `aprog verify` to run.

## Package manifest

```json
{
  "schema_version": "0.1",
  "assignment_slug": "linked-list-insertion",
  "contains_solution": true,
  "contains_hidden_tests": true,
  "contains_grader": true,
  "created_by": "github-handle"
}
```
