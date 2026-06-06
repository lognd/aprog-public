# Contributor Guide

Workflow reference for contributors. For a step-by-step walkthrough of creating your first assignment, see [quickstart.md](quickstart.md).

For grader pipeline authoring (`pipeline.py`), see the [lograder documentation](https://github.com/lognd/lograder).

---

## Contributor workflow

1. Browse templates and pick one that matches your assignment type.
2. Scaffold the assignment with `aprog new`.
3. Fill in `assignment.toml`, `README.md`, and visible tests.
4. Validate with `aprog validate`.
5. Open a public PR.
6. Write the reference solution, hidden tests, and `grader/pipeline.py`.
7. Submit the private bundle with `aprog submit`.

---

## Browse templates

```bash
aprog templates list
aprog templates list --language python
aprog templates info python-function
```

See [docs/templates/template-catalog.md](../templates/template-catalog.md) for descriptions of all templates.

Look at `examples/template-demos/` for a complete working example for each template type. Reading a demo `pipeline.py` before writing your own will save significant time.

---

## Create an assignment

```bash
aprog new linked-list-insertion --template python-function
```

This creates the public scaffold in `assignments/linked-list-insertion/` and the private scaffold in `$APROG_STAGING_DIR/linked-list-insertion/`.

---

## Fill in the grader pipeline

Open `$APROG_STAGING_DIR/<slug>/grader/pipeline.py`. This file defines the lograder `Pipeline` for your assignment.

The template scaffold provides a working skeleton with inline gotcha comments explaining the most common mistakes. Read them.

You must:

- Replace placeholder test cases with real inputs and expected outputs.
- Set point values in the scorer.
- Add a build step if the assignment requires compilation.

**Resources:**

- [lograder documentation](https://github.com/lognd/lograder) -- the primary reference for all step types, scorers, and configuration
- `examples/template-demos/` -- a complete working `pipeline.py` for each template
- [docs/grader/overview.md](../grader/overview.md) -- how the pipeline integrates with AProg

---

## Classification fields

```toml
[classification]
language = "python"
difficulty = "medium"
topics = ["data-structures", "linked-lists"]
concepts = ["mutation"]
labels = ["unit-tests"]
```

Valid values for `language`, `difficulty`, and `topics` are defined in `aprog.toml` at the repo root. Run `aprog list` to see what is registered. If you need a new topic or language, coordinate with the maintainer.

---

## What not to commit

Never commit to `aprog-public`:

- solutions
- hidden tests
- answer keys
- private notes
- `grader/pipeline.py`
- anything from `$APROG_STAGING_DIR`

The CI workflow runs `aprog scan-public --all` on every PR to catch accidental private file leaks.

---

## Submit private bundle

Package and submit the private bundle:

```bash
aprog submit linked-list-insertion
```

With `APROG_STAGING_DIR` set, `aprog submit` finds the staging files automatically.

If you need to package manually:

```bash
aprog package-private linked-list-insertion \
  --solution ~/aprog-staging/linked-list-insertion/solution \
  --hidden-tests ~/aprog-staging/linked-list-insertion/hidden-tests \
  --grader ~/aprog-staging/linked-list-insertion/grader
# Output: dist/linked-list-insertion-private.tar.gz
```

Expected bundle shape:

```text
<slug>/
|-- package-manifest.json
|-- solution/
|-- hidden-tests/
`-- grader/
    `-- pipeline.py
```
