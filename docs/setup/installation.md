# Installation and Shell Setup

Complete guide for installing AProg and configuring your shell environment.

---

## Requirements

- Python 3.10 or later
- `pip` (bundled with Python)
- `git`
- For C++ assignments: `g++` (Ubuntu: `sudo apt install g++`, macOS: Xcode Command Line Tools)

---

## Install AProg

We recommend installing AProg into a dedicated virtual environment so it stays isolated from system Python packages.

```bash
# Create a virtual environment in your home directory
python3 -m venv ~/.venvs/aprog

# Activate it
source ~/.venvs/aprog/bin/activate

# Install AProg
pip install aprog
```

Verify the install:

```bash
aprog --version
```

---

## Persistent shell setup (`.bashrc` / `.zshrc`)

Without persistent setup you must `source ~/.venvs/aprog/bin/activate` in every new terminal. Add the following block to your shell profile instead:

**For bash** (`~/.bashrc`):

```bash
# --- AProg ---
export APROG_STAGING_DIR=~/aprog-staging
source ~/.venvs/aprog/bin/activate
```

**For zsh** (`~/.zshrc`):

```zsh
# --- AProg ---
export APROG_STAGING_DIR=~/aprog-staging
source ~/.venvs/aprog/bin/activate
```

After editing, reload your shell:

```bash
source ~/.bashrc   # or source ~/.zshrc
```

### What these lines do

| Line | Purpose |
|---|---|
| `APROG_STAGING_DIR` | Tells `aprog new` and `aprog submit` where to put private working files. Must be **outside** `aprog-public`. |
| `source ... activate` | Adds the virtual environment's `bin/` to `PATH` so the `aprog` command is available without a full path. |

---

## Alternative: PATH-only setup (no activate)

If you prefer not to activate the full virtual environment, you can add just the `bin/` directory to `PATH`:

```bash
# ~/.bashrc or ~/.zshrc
export APROG_STAGING_DIR=~/aprog-staging
export PATH="$HOME/.venvs/aprog/bin:$PATH"
```

This is lighter weight  --  it only makes `aprog` (and lograder's CLI tools) available, without activating the venv for the rest of the session.

---

## Environment variables reference

| Variable | Required | Description |
|---|---|---|
| `APROG_STAGING_DIR` | Recommended | Root directory for private working files. Created automatically on first use. |
| `APROG_INTAKE_URL` | Optional | URL for the maintainer intake endpoint. If set, `aprog submit` uploads directly. |
| `APROG_PUBLIC_ROOT` | Optional | Override the auto-detected `aprog-public` root. Useful for non-standard repo layouts. |

---

## Upgrade AProg

```bash
# Activate first (or use the full path)
source ~/.venvs/aprog/bin/activate
pip install --upgrade aprog
```

---

## Verify the full setup

```bash
# Should print the AProg version
aprog --version

# Should print the staging directory path
echo $APROG_STAGING_DIR

# Should list available commands
aprog --help
```

---

## Troubleshooting

**`aprog: command not found`**

The virtual environment is not active and not on `PATH`. Either run `source ~/.venvs/aprog/bin/activate`, add the `source` line to your `.bashrc`, or add the `export PATH=...` line.

**`ModuleNotFoundError: No module named 'aprog'`**

AProg was installed into a different Python than the one running. Activate the venv that contains it, or reinstall with the correct Python:

```bash
/path/to/correct/python3 -m pip install aprog
```

**`APROG_STAGING_DIR is not set`**

`aprog new` and `aprog submit` require this variable. Add `export APROG_STAGING_DIR=~/aprog-staging` to your `.bashrc` and reload with `source ~/.bashrc`.
