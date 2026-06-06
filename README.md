# aprog-public

AProg is the assignment orchestration system -- it manages assignment definitions, contributor workflows, grader scaffolding, and Gradescope packaging. The grading logic itself is provided by [lograder](https://github.com/lognd/lograder).

## Repository layout

```text
aprog.toml              Classification values and organizational settings
assignments/            Public assignment files (statement, visible tests, starter assets)
templates/              Contributor scaffolds for new assignments
generated/              Generated manifests and autograder entry points (committed, do not hand-edit)
src/aprog/              The aprog CLI source
docs/                   Full documentation
examples/               Complete worked examples (full-assignments, template-demos)
```

Private files -- solutions, hidden tests, grader pipelines -- live in `aprog-private` and are never committed here.

## Getting started

### For contributors -- creating and submitting an assignment

See [docs/setup/installation.md](docs/setup/installation.md) for the full install and shell setup guide.

```bash
# 1. Install AProg
pip install aprog

# 2. Set a staging directory for private files (keep outside this repo)
export APROG_STAGING_DIR=~/aprog-staging

# 3. Browse available templates -- look at these before writing anything
aprog templates list --language python
aprog templates info python-function

# 4. Scaffold a new assignment
aprog new my-assignment --template python-function

# 5. Fill in assignment.toml, README.md, visible-tests/, and grader/pipeline.py
#    See: docs/contributors/quickstart.md for a step-by-step walkthrough
#    See: examples/full-assignments/cpp-linked-list/ for a complete worked example

# 6. Validate before opening a PR
aprog validate my-assignment

# 7. Submit the private bundle to the maintainer
aprog submit my-assignment
```

**Full walkthrough:** [docs/contributors/quickstart.md](docs/contributors/quickstart.md)

**Templates reference:** [docs/templates/template-catalog.md](docs/templates/template-catalog.md)

**Writing pipeline.py:** [lograder documentation](https://github.com/lognd/lograder)

### For maintainers -- intake and verification

```bash
aprog intake dist/my-assignment-private.tar.gz \
  --public . --private ../aprog-private

aprog verify my-assignment \
  --public . --private ../aprog-private

aprog generate-config my-assignment \
  --public . --private ../aprog-private

aprog package-gradescope my-assignment \
  --public . --private ../aprog-private
# Upload dist/my-assignment-gradescope.zip to Gradescope > Configure Autograder
```

**Full checklist:** [docs/maintainers/intake-workflow.md](docs/maintainers/intake-workflow.md)

## Documentation

| Audience | Start here |
|---|---|
| Contributors | [docs/contributors/quickstart.md](docs/contributors/quickstart.md) |
| Maintainers | [docs/maintainers/intake-workflow.md](docs/maintainers/intake-workflow.md) |
| Implementers | [docs/architecture/overview.md](docs/architecture/overview.md) |
| All | [docs/README.md](docs/README.md) |

For grader/pipeline.py authoring, see the [lograder documentation](https://github.com/lognd/lograder).

## Development setup

```bash
git clone https://github.com/lognd/aprog-public
cd aprog-public
make dev        # creates .venv, installs aprog + dev tools from ../lograder
make test       # runs changed tests only (pytest-testmon)
make test-all   # full test run
make check      # format + typecheck
```

The `Makefile` assumes `../lograder` is a local clone. Override with:

```bash
make dev LOGRADER=/path/to/lograder
```

## License

MIT
