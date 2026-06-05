# AProg Documentation

This documentation describes the repository orchestration layer for AProg.

AProg owns:

- assignment discovery
- assignment naming
- label and category metadata
- public/private repository boundaries
- contributor-facing templates
- assignment scaffolding
- generated public/private config artifacts
- contributor upload workflows
- maintainer intake workflows
- GitHub Actions and CI/CD repository setup

The grader package is `lograder`. AProg generates the autograder entry point (`run_autograder.py`) but not the grading pipeline itself. The pipeline is contributor-authored via the template's `grader/pipeline.py` scaffold and submitted in the private bundle. See `docs/grader/` for the lograder reference.

## Recommended reading order

### For contributors

1. `contributors/quickstart.md` — end-to-end walkthrough
2. `contributors/guide.md` — workflow reference
3. `reference/assignment-schema.md` — TOML fields
4. `reference/classification-model.md` — language/difficulty/topic values
5. `templates/template-catalog.md` — available templates
6. `grader/overview.md` — writing `pipeline.py`
7. `grader/steps.md` — step types and case models
8. `grader/scoring.md` — scorers and point configuration
9. `grader/oracle.md` — generating test cases from a reference binary

### For maintainers

10. `maintainers/intake-workflow.md` — PR review and intake checklist
11. `tools/overview.md` — full command reference
12. `setup/github-and-ci.md` — repository and CI configuration

### For implementers

13. `architecture/overview.md` — what AProg owns vs. what lograder owns
14. `architecture/repository-layout.md` — directory structure
15. `architecture/generated-configs.md` — what is generated and how
16. `architecture/public-private-boundary.md` — boundary rules and states
17. `reference/naming-conventions.md` — names, paths, env vars
18. `templates/template-system.md` — template format and validation
19. `reference/open-questions.md` — resolved decisions and rationale
