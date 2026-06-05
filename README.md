# aprog-public

Public repository for AProg — the assignment programming orchestration system.

This repository contains assignment definitions, visible tests, contributor templates, generated public configs, and the `aprog` CLI.

## What lives here

```text
aprog.toml              Classification values and organizational settings
assignments/            Public assignment files (statement, visible tests, starter assets)
templates/              Contributor-facing scaffolds for new assignments
generated/              Generated manifests and autograder entry points (committed, do not hand-edit)
src/aprog/              The aprog CLI source
docs/                   Full documentation
```

## Quick start

**For contributors** — creating and submitting an assignment:

```bash
pip install aprog

# Set a staging directory for private files (keep outside this repo)
export APROG_STAGING_DIR=~/aprog-staging

# Browse templates
aprog templates list --language python

# Scaffold a new assignment
aprog new my-assignment --template python-stdin-stdout

# Validate before opening a PR
aprog validate my-assignment

# Submit the private bundle to the maintainer
aprog submit my-assignment
```

See [docs/contributors/quickstart.md](docs/contributors/quickstart.md) for the full walkthrough.

**For maintainers** — intake and verification:

```bash
aprog intake dist/my-assignment-private.tar.gz \
  --public . --private ../aprog-private

aprog verify my-assignment \
  --public . --private ../aprog-private

aprog generate-config my-assignment \
  --public . --private ../aprog-private
```

See [docs/maintainers/intake-workflow.md](docs/maintainers/intake-workflow.md) for the checklist.

## Development setup

```bash
git clone https://github.com/lognd/aprog-public
cd aprog-public
make dev        # creates .venv and installs aprog + dev tools from ../lograder
make test       # runs changed tests only (pytest-testmon)
make test-all   # full test run
make check      # format + typecheck
```

The `Makefile` assumes `../lograder` is a local clone. Override with:

```bash
make dev LOGRADER=/path/to/lograder
```

## Repository layout

```text
aprog-public/
├── aprog.toml                          Classification values and org settings
├── assignments/
│   └── <slug>/
│       ├── assignment.toml             Assignment metadata
│       ├── README.md                   Assignment statement
│       ├── visible-tests/              Tests students can see and run
│       ├── expected/                   Expected outputs for visible tests
│       └── assets/                     Starter files
├── templates/
│   └── <template-slug>/
│       ├── template.toml
│       ├── public/                     Jinja2 templates for public scaffold
│       └── private/                    Jinja2 templates for private staging scaffold
├── generated/
│   └── assignments/
│       └── <slug>/
│           ├── assignment-manifest.json
│           ├── run_autograder.py       Generated Gradescope entry point
│           └── run_autograder          Shell shim
├── src/aprog/                          CLI source
└── docs/                               Full documentation
```

Private files (solutions, hidden tests, grader pipelines) live in `aprog-private` and are never committed here.

## Documentation

| Audience | Start here |
|---|---|
| Contributors | [docs/contributors/quickstart.md](docs/contributors/quickstart.md) |
| Maintainers | [docs/maintainers/intake-workflow.md](docs/maintainers/intake-workflow.md) |
| Implementers | [docs/architecture/overview.md](docs/architecture/overview.md) |
| All | [docs/README.md](docs/README.md) |

## License

MIT
