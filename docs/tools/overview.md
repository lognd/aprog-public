# Command Reference

All commands: `aprog --help` or `aprog <command> --help`.

## Contributor commands

| Command | What it does |
|---|---|
| `aprog new <slug> --template <t>` | Scaffold a new assignment (public + private staging) |
| `aprog templates list` | List available templates |
| `aprog templates info <slug>` | Show template details and expected file layout |
| `aprog validate <slug>` | Validate public files (schema, classification, generated files) |
| `aprog validate --all` | Validate all assignments |
| `aprog list` | List all assignments |
| `aprog info <slug>` | Show assignment metadata |
| `aprog submit <slug>` | Package and send the private bundle to the maintainer |

## Maintainer commands

| Command | What it does |
|---|---|
| `aprog intake <bundle.tar.gz>` | Import a private bundle into `aprog-private` |
| `aprog verify <slug>` | Run the grader against the reference solution |
| `aprog verify --all` | Verify all assignments |
| `aprog generate-config <slug>` | Regenerate `run_autograder.py` and manifests |
| `aprog generate-config --all` | Regenerate for all assignments |
| `aprog check-generated <slug>` | Check whether generated files are current |
| `aprog package-gradescope <slug>` | Build the Gradescope zip |
| `aprog scan-public <slug>` | Check for private file leaks in the public repo |

Most maintainer commands accept `--public <path>` and `--private <path>` to override the auto-detected repo roots.
