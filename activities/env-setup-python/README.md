# Activity: Install Python and Course Tools

> **Activity 2 of 7**
>
> Prerequisites:
> - [1. Shell](../env-setup-shell/)
>
> Next: [3. Compiler](../env-setup-compiler/)

Several course utilities and activity launchers are written in Python.
You also need a set of standard development tools -- a formatter,
linter, type checker, and test runner -- that you will use throughout
the course.

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

The tools you install below (black, ruff, mypy, pytest, isort) are
the current industry standard for Python development quality. You will
see them in professional codebases.

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
sudo apt install -y python3 python3-pip python3-venv
```

<details>
<summary>What are python3-pip and python3-venv?</summary>

**pip** (the `pip3` executable) is Python's package installer. It
downloads packages from PyPI (the Python Package Index at pypi.org)
and installs them. When you run `pip install black`, pip fetches the
`black` package and its dependencies from PyPI and places them where
Python can find them.

**venv** is the standard module for creating virtual environments.
A virtual environment is an isolated Python installation with its own
set of installed packages. This lets different projects have different
package versions without conflicts. For example, one project might
need `requests==2.28` and another `requests==2.31` -- venv keeps
them separate.

`python3-pip` and `python3-venv` are Debian/Ubuntu packages that
provide these modules for the system Python. On other distributions
they are often bundled with the main Python package.

</details>

### Linux (Fedora / RHEL / Rocky)

```bash
sudo dnf install python3 python3-pip
```

### Linux (Arch / Manjaro)

```bash
sudo pacman -S python python-pip
```

### macOS

macOS ships an outdated Python. Install a current version via
Homebrew:

```bash
brew install python
```

This installs `python3` and `pip3`. Verify:

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
   packages you install with pip, such as `black.exe`, `ruff.exe`,
   etc.

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

## Step 2: Install pip tools

`pip` (or `pip3`) is the Python package manager. You will use it to
install packages from PyPI.

<details>
<summary>How does pip work internally?</summary>

When you run `pip install black`, pip:

1. Queries PyPI (https://pypi.org) for the `black` package.
2. Downloads the wheel (`.whl`) or source distribution for your
   platform.
3. Unpacks it into Python's `site-packages` directory, which is the
   folder Python searches when you `import` something.
4. Installs any packages that `black` depends on, recursively.

A wheel (`.whl`) is a pre-built binary package -- a zip file with a
specific naming convention. It installs faster than a source
distribution because no compilation step is needed.

Installed package executables (like the `black` command) land in
Python's `bin/` directory (`Scripts\` on Windows). That directory
must be on your PATH for those commands to be usable.

</details>

Upgrade pip itself first (the bundled version is often old):

```bash
python3 -m pip install --upgrade pip
```

<details>
<summary>Why python3 -m pip instead of just pip3?</summary>

`python3 -m pip` explicitly runs pip as a module of the Python
interpreter you just typed (`python3`). This avoids a common pitfall
where `pip3` on your PATH belongs to a different Python installation
than `python3`. Using `-m pip` guarantees you are installing into the
correct Python.

</details>

---

## Step 3: Install the course tools

Install all five tools with a single command:

```bash
python3 -m pip install black ruff mypy pytest isort
```

<details>
<summary>What does each tool do?</summary>

**black** -- an opinionated, uncompromising code formatter. It
reformats your Python code to a single consistent style with no
configuration choices. The point is that everyone's code looks the
same, so diffs are about logic changes not style changes. Run it with
`black myfile.py` or `black .` to format the entire current directory.

**ruff** -- an extremely fast Python linter written in Rust. A linter
reads your code without running it and reports potential bugs, unused
imports, undefined variables, style violations, and hundreds of other
issues. Ruff replaces flake8, pyflakes, pep8, and many other older
linters, running 10-100x faster. Run it with `ruff check .`.

**mypy** -- a static type checker for Python. Python is dynamically
typed (types are checked at runtime), but you can add optional type
annotations to your code. Mypy reads those annotations and reports
type errors before you run the program -- similar to what a C++
compiler does. Run it with `mypy myfile.py`.

**pytest** -- the standard Python testing framework. It discovers and
runs test functions (functions whose names start with `test_`) and
reports which pass and which fail. The course uses pytest for visible
tests you can run locally. Run it with `pytest` in a project directory.

**isort** -- sorts your import statements alphabetically and groups
them by category (standard library, third-party, local). This is a
style convention that makes it easy to see at a glance what a module
depends on. Run it with `isort myfile.py` or `isort .`.

</details>

Verify each tool is installed and on your PATH:

```bash
black --version
ruff --version
mypy --version
pytest --version
isort --version
```

If any command is not found, see Troubleshooting below.

---

---

## Verify completion

Once all five tools respond to `--version`, run the activity script.
Open your WSL terminal (or any terminal on macOS/Linux), navigate to
this activity's folder, and run:

```bash
python3 launch.py
```

<details>
<summary>What is launch.py and how do I navigate to it?</summary>

`launch.py` is a verification script included with this activity.
`python3` is the Python interpreter -- the program that reads and runs
Python source files. The script checks that your Python and all five
tools are installed correctly, then prints a passphrase when everything
passes.

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

## uv (optional, but faster)

`uv` is a modern Rust-based replacement for pip that is 10-100x
faster. It is not required for this course but is worth knowing about.

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh   # Linux/macOS
# or on Windows PowerShell:
# powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Use uv instead of pip
uv pip install black ruff mypy pytest isort
```

`uv` installs to `~/.local/bin/` and modifies your shell config to
add that to PATH. Open a new terminal after installation.

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

### "black: command not found" after pip install

pip installs executables to `~/.local/bin/` (Linux/macOS) or
`%APPDATA%\Python\PythonXY\Scripts\` (Windows). If that directory is
not on PATH, the commands install successfully but are not found.

On Linux/macOS, add `~/.local/bin` to PATH permanently:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Then verify: `which black`.

On Windows, the Scripts directory should have been added by the
Python installer if you checked "Add to PATH". If not, add it
manually via "Edit the system environment variables".

### "pip: externally-managed-environment" (Ubuntu 23.04+)

Newer Ubuntu versions prevent pip from installing into the system
Python to protect OS tools. The clean solution is a virtual
environment:

```bash
python3 -m venv ~/.venv
source ~/.venv/bin/activate
pip install black ruff mypy pytest isort
```

Add the activation to your `~/.bashrc` to make it permanent:

```bash
echo 'source ~/.venv/bin/activate' >> ~/.bashrc
```

Or use the `--break-system-packages` flag (not recommended, but
works for personal machines):

```bash
pip install --break-system-packages black ruff mypy pytest isort
```

### "SSL: CERTIFICATE_VERIFY_FAILED" on macOS

Run the certificate installer that ships with Python:

```bash
/Applications/Python\ 3.14/Install\ Certificates.command
```

(Adjust the version number to match your install.)

### Windows: multiple Pythons installed, wrong one runs

```
where python
```

This lists all `python.exe` files found in PATH, in order. The first
one is what runs when you type `python`. Reorder PATH entries if
needed via "Edit the system environment variables".
