# GitHub and CI Setup

This document describes what must be configured manually by the repository owner.

## Create repositories

Create:

```text
aprog-public    (public)
aprog-private   (private)
```

## Branch protection

For `aprog-public/main`:

- require pull requests
- require at least one review
- require CI checks to pass
- block force pushes
- block direct pushes

For `aprog-private/main`:

- require pull requests
- require maintainer review
- block force pushes
- restrict write access to maintainers

## Deploy key for private checkout

Generate a read-only deploy key for CI:

```bash
ssh-keygen -t ed25519 -C "aprog-private-ci-deploy-key" -f aprog_private_deploy_key -N ""
```

Add the public key to `aprog-private`:

```text
Settings -> Deploy keys -> Add deploy key (read-only, no write access)
```

Add the private key to `aprog-public` Actions secrets:

```text
APROG_PRIVATE_DEPLOY_KEY
```

Delete both key files locally after configuration.

## Required GitHub secrets

In `aprog-public`:

```text
APROG_PRIVATE_DEPLOY_KEY
```

Optional (only if encrypted submission is used):

```text
APROG_GPG_PRIVATE_KEY
APROG_GPG_PASSPHRASE
```

## Public validation workflow

Runs on every PR that touches assignments, templates, or tools.

File: `.github/workflows/validate-public.yml`

```yaml
name: Validate Public Assignments

on:
  pull_request:
    paths:
      - "assignments/**"
      - "aprog.toml"
      - "templates/**"
      - "tools/**"
      - "generated/**"

jobs:
  validate-public:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install AProg
        run: pip install -e .
      - name: Validate all assignments
        run: aprog validate --all
      - name: Check generated files
        run: aprog check-generated --all
      - name: Scan for private file leaks
        run: aprog scan-public --all
```

`aprog validate --all` already calls `scan-public` and `check-generated` internally, but running them separately surfaces the specific failure reason more clearly in CI output.

## Full verification workflow

Runs on `workflow_dispatch` or when a maintainer applies the `verify` label to a PR.

File: `.github/workflows/verify-full.yml`

```yaml
name: Verify Assignments

on:
  workflow_dispatch:
    inputs:
      slug:
        description: "Assignment slug (leave empty to verify all)"
        required: false
        default: ""
  pull_request:
    types: [labeled]

jobs:
  verify-full:
    if: >
      github.event_name == 'workflow_dispatch' ||
      (github.event_name == 'pull_request' && github.event.label.name == 'verify')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          path: public

      - uses: actions/checkout@v4
        with:
          repository: ${{ github.repository_owner }}/aprog-private
          ssh-key: ${{ secrets.APROG_PRIVATE_DEPLOY_KEY }}
          path: private

      - name: Install AProg
        run: pip install -e public

      - name: Verify
        run: |
          SLUG="${{ github.event.inputs.slug }}"
          if [ -n "$SLUG" ]; then
            aprog verify "$SLUG" --public public --private private
          else
            aprog verify --all --public public --private private
          fi
```

## Standard decisions

These are the recommended settings. Override in your `aprog.toml` if your organization has different needs.

| Decision | Default |
|---|---|
| Generated public configs committed | Yes |
| Generated private configs committed | Yes |
| Encrypted submission required | No (optional with `--encrypt` flag) |
| Full verification on every PR | No (manual dispatch or `verify` label) |
| Hidden tests authored by | Contributors (required in private bundle) |
| Private bundles archived after intake | No (pass `--archive` to keep) |

## `aprog.toml` organizational overrides

```toml
[organization]
require_encryption = false        # set to true to reject unencrypted private bundles
require_hidden_tests = true       # set to false to allow assignments without hidden tests
default_grader_visibility = "after_due_date"
```
