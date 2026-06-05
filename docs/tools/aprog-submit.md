# Tool Design: `aprog submit`

Packages the private bundle and delivers it to the maintainer intake endpoint.

`aprog submit` is a contributor-facing convenience command. It runs `aprog package-private`, then either prints the bundle path with next steps or uploads to a configured intake URL.

## Usage

```bash
aprog submit <assignment-slug> \
  --solution path/to/solution \
  --hidden-tests path/to/hidden-tests \
  --grader path/to/grader
```

Or, if a staging directory is configured:

```bash
aprog submit <assignment-slug>
```

When `APROG_STAGING_DIR` is set, `aprog submit` resolves the private paths from `$APROG_STAGING_DIR/<slug>/solution`, `$APROG_STAGING_DIR/<slug>/hidden-tests`, and `$APROG_STAGING_DIR/<slug>/grader` automatically.

## Delivery

### Without `APROG_INTAKE_URL`

Packages the bundle and prints the output path with manual instructions:

```text
Bundle: dist/linked-list-insertion-private.tar.gz

Submit this file to your maintainer using the process documented at:
  https://your-org/instructions
```

### With `APROG_INTAKE_URL`

Packages the bundle and uploads it via HTTP POST:

```bash
APROG_INTAKE_URL=https://intake.example.com/upload aprog submit linked-list-insertion
```

The request is a multipart form upload with the bundle file and the assignment slug. The server should return a JSON body with `{"status": "received", "id": "..."}`.

## Environment variables

| Variable | Description |
|---|---|
| `APROG_STAGING_DIR` | Default base directory for private working files |
| `APROG_INTAKE_URL` | If set, upload the bundle to this URL after packaging |

## Encryption

Pass `--encrypt` to GPG-encrypt the bundle before uploading or printing the path:

```bash
aprog submit linked-list-insertion --encrypt
```

Requires `APROG_GPG_RECIPIENT` to be set (the maintainer's GPG key ID).

## What `aprog submit` does not do

- It does not run validation.
- It does not open a GitHub PR.
- It does not modify `aprog-public`.

Run `aprog validate <slug>` separately before submitting.
