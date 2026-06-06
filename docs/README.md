# AProg Documentation

AProg is the assignment orchestration layer. It owns assignment discovery, classification, template scaffolding, public/private boundary enforcement, contributor upload, maintainer intake, config generation, and CI.

The grading pipeline library is [lograder](https://github.com/lognd/lograder). For anything related to writing `pipeline.py` -- step types, build steps, test types, scorers -- see the [lograder documentation](https://github.com/lognd/lograder).

---

## For contributors

1. [setup/installation.md](setup/installation.md) -- install AProg and configure your shell
2. [contributors/quickstart.md](contributors/quickstart.md) -- end-to-end walkthrough
3. [contributors/guide.md](contributors/guide.md) -- workflow reference
4. [templates/template-catalog.md](templates/template-catalog.md) -- available templates with demos
5. [lograder documentation](https://github.com/lognd/lograder) -- writing `pipeline.py`
6. [reference/assignment-schema.md](reference/assignment-schema.md) -- all `assignment.toml` fields
7. [reference/classification-model.md](reference/classification-model.md) -- language/difficulty/topic values

## For maintainers

8. [maintainers/intake-workflow.md](maintainers/intake-workflow.md) -- PR review and intake checklist
9. [maintainers/gradescope-upload.md](maintainers/gradescope-upload.md) -- building and uploading the autograder
10. [tools/overview.md](tools/overview.md) -- full command reference
11. [setup/github-and-ci.md](setup/github-and-ci.md) -- repository and CI configuration

## For implementers

12. [architecture/overview.md](architecture/overview.md) -- AProg vs lograder split, repository structure
13. [architecture/repository-layout.md](architecture/repository-layout.md) -- directory layout
14. [architecture/generated-configs.md](architecture/generated-configs.md) -- what is generated and why
15. [architecture/public-private-boundary.md](architecture/public-private-boundary.md) -- what belongs where
16. [grader/overview.md](grader/overview.md) -- how `pipeline.py` integrates with AProg
17. [templates/template-system.md](templates/template-system.md) -- template format and validation
