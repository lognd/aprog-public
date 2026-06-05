# AProg Tooling Design Overview

The `aprog` CLI is the main interface for contributors and maintainers.

## Command reference

| Group | Commands | Doc |
|---|---|---|
| Assignment creation | `new` | `tools/aprog-new.md` |
| Template discovery | `templates list`, `templates info` | `tools/aprog-list.md` |
| Validation | `validate` | `tools/aprog-validate.md` |
| Public boundary scan | `scan-public` | `tools/aprog-scan-public.md` |
| Generated file check | `check-generated` | `tools/aprog-scan-public.md` |
| Discovery | `list`, `info` | `tools/aprog-list.md` |
| Public packaging | `package-public` | `tools/aprog-package.md` |
| Private packaging | `package-private` | `tools/aprog-package.md` |
| Submission | `submit` | `tools/aprog-submit.md` |
| Maintainer intake | `intake` | `tools/aprog-intake.md` |
| Verification | `verify` | `tools/aprog-verify.md` |
| Config generation | `generate-config` | `tools/aprog-generate-config.md` |
| Gradescope packaging | `package-gradescope` | `tools/aprog-package-gradescope.md` |

## Command naming principles

- Use verbs.
- Prefer explicit names over clever aliases.
- Keep contributor commands safe by default.
- Require explicit flags for private operations.

## Contributor-safe commands

These commands never write private files into `aprog-public`:

```text
aprog new
aprog validate
aprog scan-public
aprog check-generated
aprog list
aprog info
aprog package-public
aprog submit
aprog templates list
aprog templates info
```

## Maintainer commands

These read or write private files:

```text
aprog package-private
aprog intake
aprog verify
aprog generate-config --private <path>
aprog package-gradescope
```
