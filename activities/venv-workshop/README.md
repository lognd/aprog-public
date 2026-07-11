# Activity: Virtual Environment Workshop

> Prerequisite: [Python setup](../env-setup-python/) (you need a working
> `python3`). Having [`uv`](../env-setup-python/) available is used in
> Part 2 -- see below if you do not have it yet.

This is a hands-on activity, not a quiz. You will actually build two
Python **virtual environments** and install a package into each, then a
checker confirms you did it and gives you a passphrase.

## What is a virtual environment, and why bother?

When you install a Python package (a reusable chunk of someone else's
code), by default it goes into one shared, system-wide folder that
*every* Python project on your computer sees. That sounds convenient
until two projects need two different versions of the same package --
now they fight over that one shared folder, and installing the version
one project needs quietly breaks the other.

A **virtual environment** ("venv" for short) fixes this: it is a private,
per-project copy of Python's package folder, living in a directory
*inside your project*. Each project gets its own, so their dependencies
never collide. Turning a venv "on" (called **activating** it) tells your
shell "for now, use this project's private packages instead of the
system-wide ones."

A few terms you will meet, defined once here:

- **package** -- a reusable library of Python code you install rather than
  write yourself (in this activity, the tiny `cowsay` package).
- **PyPI** (the Python Package Index, `pypi.org`) -- the public online
  repository that `pip` and `uv` download packages from. Installing a
  package needs internet access the first time, to reach PyPI.
- **`pip`** -- the classic command-line tool that installs packages *into*
  whichever environment is currently active.
- **activate / deactivate** -- turning a venv on for your current shell,
  and turning it back off. On Linux and macOS you activate with the
  `source` builtin (`source venv/bin/activate`); `source` runs a script's
  commands in your *current* shell so the on/off switch actually affects
  it.
- **`uv`** -- a newer, much faster all-in-one tool that does the same jobs
  (create environments, install packages) with shorter commands. This
  course's own tooling uses `uv`, so Part 2 practices it directly.

## What you will do

Run the activity:

```bash
python3 launch.py
```

It drops you into a shell inside a fresh, throwaway directory (nothing
here touches your real projects -- the directory is deleted when you
exit). Complete both parts, then type `exit` (or press Ctrl-D) to be
checked.

### Part 1 -- the classic workflow (`python3 -m venv` + `pip`)

```bash
python3 -m venv venv        # create an environment in ./venv
source venv/bin/activate    # turn it on -- your prompt now shows (venv)
pip install cowsay          # install the cowsay package INTO the active venv
cowsay -t "it works!"       # run the package you just installed
deactivate                  # turn the environment back off
```

- `python3 -m venv venv` runs the standard library's `venv` module
  (`-m` means "run this module as a program") and creates the environment
  in a new folder named `venv`.
- After `activate`, your prompt is prefixed with `(venv)` -- that is how
  you know an environment is on. Any `pip install` now lands inside it,
  not in the system-wide folder.
- `deactivate` returns you to the normal, system Python.

### Part 2 -- the modern workflow (`uv`)

```bash
uv venv uvenv                          # create an environment in ./uvenv
uv pip install --python uvenv cowsay   # install cowsay into that environment
```

`uv venv` is `uv`'s equivalent of `python3 -m venv`, and `uv pip install`
is its equivalent of `pip install`. The `--python uvenv` flag tells `uv`
which environment to install into (so you do not even have to activate it
first). Notice how the two parts mirror each other -- same two ideas
("make an environment", "install a package into it"), two different
tools.

<details>
<summary>I do not have `uv` installed</summary>

Install it with the official one-line installer:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then open a new terminal so `uv` is on your `PATH`, and re-run the
activity. (macOS users can also use `brew install uv`.)

</details>

## How you are checked

When you exit the shell, the activity inspects the working directory and
confirms:

1. A virtual environment named `venv` exists, and
2. `cowsay` is importable from *inside* it, and
3. A virtual environment named `uvenv` exists, and
4. `cowsay` is importable from *inside* it too.

All four must hold at the moment you exit. If a step is missing, the
checker tells you which one, and you can re-run and finish it. When they
all pass, it prints the passphrase -- submit that to record completion.

## Going further (not checked)

- The fullest `uv` workflow is project-based: `uv init myproj` creates a
  project with a `pyproject.toml` (the file that records your
  dependencies), `uv add cowsay` records and installs a dependency, and
  `uv run python ...` runs a command inside the project's environment
  automatically -- no manual activate/deactivate at all. This is exactly
  how you run this course's `aprog` tool (`uv run aprog ...`).
- Look inside a venv folder: `venv/pyvenv.cfg` is a small text file
  describing which base Python it was built from, and
  `venv/lib/python3.*/site-packages/` is where installed packages
  actually live. That directory *is* the "private package folder" a venv
  gives each project.
- A `requirements.txt` file (one package name per line) lets you record
  and re-install a project's packages with `pip install -r
  requirements.txt` -- the older counterpart to `uv`'s `pyproject.toml`.
