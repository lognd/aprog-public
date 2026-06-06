# Installation and Shell Setup

Complete guide for installing AProg and configuring your shell environment.

---

## Requirements

- Python 3.10 or later
- `pip` (bundled with Python)
- `git`
- For C++ assignments: `g++` (Ubuntu: `sudo apt install g++`, macOS: Xcode Command Line Tools)

---

## Step 1 -- Check your Python version

```bash
python3 --version
```

You need Python 3.10 or later. If yours is older, install a newer version from [python.org](https://python.org) or your system package manager before continuing.

---

## Step 2 -- Create a virtual environment

Installing AProg into a dedicated virtual environment keeps it isolated from your system Python packages and prevents version conflicts.

```bash
python3 -m venv ~/.venvs/aprog
```

This creates a new environment at `~/.venvs/aprog/`. You only need to do this once.

---

## Step 3 -- Activate the virtual environment

```bash
source ~/.venvs/aprog/bin/activate
```

Your prompt will change to show `(aprog)` when the environment is active. You need to activate it in every new terminal session, or follow Step 5 to make it automatic.

---

## Step 4 -- Install AProg

With the virtual environment active:

```bash
pip install aprog
```

This also installs [lograder](https://github.com/lognd/lograder) -- the grading pipeline library that `pipeline.py` files are written against.

Verify the install:

```bash
aprog --version
aprog --help
```

---

## Step 5 -- Persistent shell setup

Without persistent setup you must re-run `source ~/.venvs/aprog/bin/activate` in every new terminal. Add the following lines to your shell profile to make setup automatic.

**For bash** -- add to `~/.bashrc`:

```bash
# --- AProg ---
export APROG_STAGING_DIR=~/aprog-staging
source ~/.venvs/aprog/bin/activate
```

**For zsh** -- add to `~/.zshrc`:

```zsh
# --- AProg ---
export APROG_STAGING_DIR=~/aprog-staging
source ~/.venvs/aprog/bin/activate
```

After editing, reload your shell:

```bash
source ~/.bashrc   # or: source ~/.zshrc
```

### What these lines do

| Line | Purpose |
|---|---|
| `APROG_STAGING_DIR` | Tells `aprog new` and `aprog submit` where to write private working files. Must be **outside** `aprog-public`. |
| `source ... activate` | Adds the virtual environment's `bin/` to `PATH` so `aprog` is available in every terminal without a full path. |

---

## Step 6 -- Verify the full setup

Run all three of these to confirm everything is working:

```bash
aprog --version
echo $APROG_STAGING_DIR
aprog templates list
```

If `aprog --version` prints a version number, `$APROG_STAGING_DIR` prints a path, and `aprog templates list` lists available templates, you are ready to go.

---

## Alternative: PATH-only setup (no activate)

If you prefer not to activate the full virtual environment on every shell, you can add just the `bin/` directory to `PATH`:

```bash
# ~/.bashrc or ~/.zshrc
export APROG_STAGING_DIR=~/aprog-staging
export PATH="$HOME/.venvs/aprog/bin:$PATH"
```

This makes `aprog` available without activating the venv for the rest of the session.

---

## Upgrading AProg

```bash
source ~/.venvs/aprog/bin/activate   # skip if already active
pip install --upgrade aprog
```

---

## Environment variables reference

| Variable | Required | Description |
|---|---|---|
| `APROG_STAGING_DIR` | Recommended | Root directory for private working files. Created automatically on first use. |
| `APROG_INTAKE_URL` | Optional | URL for the maintainer intake endpoint. If set, `aprog submit` uploads directly instead of writing a local file. |
| `APROG_PUBLIC_ROOT` | Optional | Override the auto-detected `aprog-public` root. Useful for non-standard repo layouts. |

---

## Troubleshooting

**`aprog: command not found`**

The virtual environment is not active and not on `PATH`. Run `source ~/.venvs/aprog/bin/activate`, or add the `source` line to your `.bashrc` / `.zshrc` as shown in Step 5.

**`ModuleNotFoundError: No module named 'aprog'`**

AProg was installed into a different Python than the one currently running. Activate the venv that contains it, or reinstall:

```bash
source ~/.venvs/aprog/bin/activate
pip install aprog
```

**`APROG_STAGING_DIR is not set`**

`aprog new` and `aprog submit` require this variable. Add `export APROG_STAGING_DIR=~/aprog-staging` to your `.bashrc` and reload: `source ~/.bashrc`.
