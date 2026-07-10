# Activity: Install Python and Course Tools

> **Activity 2 of 7**
>
> Prerequisites:
> - [1. Shell](../env-setup-shell/)
>
> Next: [3. Compiler](../env-setup-compiler/)

Several course utilities and activity launchers are written in Python.
You also need a set of standard development tools -- a package manager,
a formatter/linter, a type checker, and a test runner -- that you will
use throughout the course.

<details>
<summary>What is Python and why does this course use it?</summary>

Python is a high-level interpreted language used for scripting,
automation, data processing, and much more. Unlike C++, Python code
is not compiled to machine code ahead of time -- a program called the
interpreter (the `python3` executable) reads and executes the source
directly.

This course uses Python for:
- Activity launchers (`launch.py` files like this one)
- Build and grading scripts
- Assignments that involve scripting or automation

The tools you install below (uv, ruff, ty, pytest) are the modern
standard for Python development quality. You will see them in
professional codebases.

</details>

---

## Step 1: Install Python 3

This course requires Python 3.10 or later.

### Linux (Ubuntu / Debian / WSL)

Ubuntu 22.04 and later ship Python 3.10+. Check first:

```bash
python3 --version
```

If it is missing or too old:

```bash
sudo apt update
sudo apt install -y python3
```

### Linux (Fedora / RHEL / Rocky)

```bash
sudo dnf install python3
```

### Linux (Arch / Manjaro)

```bash
sudo pacman -S python
```

### macOS

macOS ships an outdated Python. Install a current version via
Homebrew:

```bash
brew install python
```

Verify:

```bash
python3 --version
```

### Windows (WSL -- recommended)

Inside your WSL terminal, follow the Linux/Ubuntu instructions above.

### Windows (native)

1. Download the installer from https://www.python.org/downloads/
2. Run it.
3. **On the first screen, check "Add python.exe to PATH".**
   This is the most important step. Without it, Python installs
   successfully but the `python` command will not be found in any
   terminal you open.

<details>
<summary>What does "Add to PATH" actually do on Windows?</summary>

The Python installer on Windows writes two directories into the
`PATH` environment variable in the Windows registry:

1. The Python install directory itself (e.g.,
   `C:\Users\YourName\AppData\Local\Programs\Python\Python314\`),
   which contains `python.exe`.
2. The `Scripts\` subdirectory (e.g.,
   `C:\...\Python314\Scripts\`), which contains executables for
   installed packages.

The registry PATH is read by every new terminal you open. Without
this checkbox, you would have to type the full path to `python.exe`
every time, or add the directories manually through "Edit the system
environment variables" in Control Panel.

</details>

4. Open a new Command Prompt or PowerShell and verify:
   ```
   python --version
   ```

---

## Step 2: Install uv

`uv` is a fast Python package and tool manager written in Rust. It
replaces the older `pip` workflow for this course: it installs tools
into isolated environments automatically, so nothing you install can
break your system Python.

### Linux / macOS / WSL

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows (native, PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

`uv` installs to `~/.local/bin/` and offers to add that directory to
your PATH. **Open a new terminal after installing**, then verify:

```bash
uv --version
```

<details>
<summary>What is uv and how is it different from pip?</summary>

`pip` is Python's traditional package installer: it downloads packages
from PyPI (the Python Package Index at pypi.org) and installs them
into whichever Python environment it belongs to. That "whichever" is
the classic source of pain -- packages end up in the wrong Python,
conflict with system packages, or require a virtual environment you
have to create and activate by hand.

`uv` solves the same problem with less ceremony and far more speed
(it is 10-100x faster than pip):

- `uv tool install <name>` installs a command-line tool into its own
  private, isolated environment and puts just the command (e.g.
  `ruff`) on your PATH. Tools can never conflict with each other or
  with your system Python.
- `uv venv` / `uv pip` manage per-project virtual environments when
  you need libraries for a project.
- On newer Linux distributions, `pip install` outside a virtual
  environment fails with an `externally-managed-environment` error.
  `uv tool install` sidesteps that whole problem by design.

</details>

---

## Step 3: Install the course tools

Install the three course tools with `uv tool install`:

```bash
uv tool install ruff
uv tool install ty
uv tool install pytest
```

<details>
<summary>What does each tool do?</summary>

**ruff** -- an extremely fast Python formatter and linter in one
tool. `ruff format myfile.py` reformats your code to a consistent
style (so diffs are about logic, not whitespace). `ruff check .`
lints it: it reads your code without running it and reports likely
bugs, unused imports, undefined variables, and hundreds of other
issues.

**ty** -- a fast static type checker for Python. Python is
dynamically typed (types are checked at runtime), but you can add
optional type annotations to your code. `ty check myfile.py` reads
those annotations and reports type errors before you run the
program -- similar to what a C++ compiler does at compile time.

**pytest** -- the standard Python testing framework. It discovers and
runs test functions (functions whose names start with `test_`) and
reports which pass and which fail. The course uses pytest for visible
tests you can run locally. Run it with `pytest` in a project
directory.

</details>

Verify each tool is installed and on your PATH:

```bash
uv --version
ruff --version
ty --version
pytest --version
```

If any command is not found, see Troubleshooting below.

---

## Verify completion

Once all four commands respond to `--version`, run the activity
script. Open your WSL terminal (or any terminal on macOS/Linux),
navigate to this activity's folder, and run:

```bash
python3 launch.py
```

<details>
<summary>What is launch.py and how do I navigate to it?</summary>

`launch.py` is a verification script included with this activity.
`python3` is the Python interpreter -- the program that reads and runs
Python source files. The script checks that your Python and all the
course tools are installed correctly, then prints a passphrase when
everything passes.

To get to the right folder, use `cd` (change directory). For example:

```bash
cd ~/Downloads/env-setup-python
python3 launch.py
```

`~` is shorthand for your home directory (`/home/yourname` on Linux).
If you are not sure where the activity files are, you can drag the
folder into the terminal window to paste its path automatically.

</details>

Follow the prompts. When the script succeeds it prints a passphrase --
submit that to record completion.

---

## TROUBLESHOOTING

### "python3: command not found" on Ubuntu/WSL

```bash
sudo apt install python3
```

### "python: command not found" (python3 works, python does not)

Modern Linux does not provide `python` as an alias for `python3`.
Either use `python3` explicitly, or:

```bash
sudo apt install python-is-python3    # Ubuntu 20.04+
```

### "uv: command not found" after installing

The installer puts `uv` in `~/.local/bin/`. New terminals pick that
up automatically if the installer updated your shell config; the
terminal you installed from does not. Open a new terminal, or run:

```bash
source ~/.local/bin/env
```

If it is still not found, add the directory to PATH permanently:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### "ruff: command not found" after uv tool install

`uv tool install` places tool executables in `~/.local/bin/` too --
the same PATH fix as above applies. You can also ask uv to repair the
PATH for you:

```bash
uv tool update-shell
```

Then open a new terminal and verify with `which ruff`.

### Windows: multiple Pythons installed, wrong one runs

```
where python
```

This lists all `python.exe` files found in PATH, in order. The first
one is what runs when you type `python`. Reorder PATH entries if
needed via "Edit the system environment variables".
