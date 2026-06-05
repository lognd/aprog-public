# Maintainer Intake Workflow

## Public PR review

Check:

- assignment name and slug
- README quality
- visible tests
- classification choices
- template choice
- no private files committed (no `solution`, `hidden-tests`, `grader/`)

Run:

```bash
aprog validate <slug>
```

## Private submission intake

Run:

```bash
aprog intake dist/<slug>-private.tar.gz --public ../aprog-public --private ../aprog-private
```

Intake will reject the bundle if `grader/pipeline.py` is missing.

Then verify:

```bash
aprog verify <slug> --public ../aprog-public --private ../aprog-private
```

## Generate configs

```bash
aprog generate-config <slug> --public ../aprog-public --private ../aprog-private
```

## Merge checklist

- [ ] Public validation passes
- [ ] Private solution exists
- [ ] Grader pipeline (`grader/pipeline.py`) exists and exports `make_pipeline`
- [ ] Hidden tests are present, if required
- [ ] Full verification passes (reference solution earns full points)
- [ ] Generated configs are current
- [ ] No private material is present in public repo
- [ ] Public PR and private bundle refer to the same slug

## After merge — deploy to Gradescope

See `maintainers/gradescope-upload.md` for the full upload guide.

Quick sequence:

```bash
aprog generate-config <slug> --force
aprog package-gradescope <slug> --public ../aprog-public --private ../aprog-private
# Upload dist/<slug>-gradescope.zip in Gradescope > Configure Autograder
```
