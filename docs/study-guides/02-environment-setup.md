# Study Guide 2: Environment Setup

This module gets your machine ready for the entire course: a Unix-like
shell, Python plus its tooling and virtual environments, two C/C++ compiler
families, the CMake and Make build tools, SFML, an IDE, git/GitHub, and the
class Discord. Every later row assumes all nine of these activities are
complete.

## Know before you start

- Nothing. This is the first row of the course.

## Taught here

Concept: the shell
- Know that a shell (bash, zsh) is the program that reads commands you
  type in a terminal window and runs them.
- Know that this course requires a Unix/Linux-like environment because the
  standard C++ toolchain (gcc, make, cmake, gdb, valgrind) targets POSIX
  systems; Windows users get this via WSL2 (Windows Subsystem for Linux),
  which runs a real Linux kernel inside Windows.
- Be able to distinguish a compiled binary (ready to run) from source code
  (must be built first).
- Know what PATH is: an environment variable listing directories the shell
  searches, in order, for a program by name.
- Be able to add a directory to PATH permanently by editing `~/.bashrc`
  (bash) or `~/.zprofile` (zsh) and reloading it with `source`.
- Know that `chmod +x` sets the execute permission bit on a downloaded
  file, without which the shell refuses to run it.
- Know that `./program` runs a file in the current directory explicitly,
  while a bare `program` only searches PATH -- this is a deliberate safety
  feature against a malicious same-named file in the current folder.
- Know that `export` marks a shell variable to be inherited by child
  processes (programs launched from that shell); an unexported variable is
  invisible to anything you run.

Concept: Python and its tooling
- Know that Python is interpreted (a `python3` process reads and executes
  source directly) rather than compiled ahead of time like C++.
- Know the paired classic/modern Python tools and what each does: `black`
  vs `ruff format` (formatting), `mypy` vs `ty` (static type checking),
  and `ruff check` (linting, no classic equivalent named here); `pytest`
  runs tests in both worlds.
- Know that `uv tool install <name>` installs a command-line tool into its
  own isolated environment, avoiding conflicts with system Python or other
  tools.
- Know that "externally managed environment" errors on modern Linux exist
  to stop bare `pip install` from touching system-managed packages, and
  that a venv (or `uv tool install`) is the standard fix.

Concept: virtual environments
- Know that a virtual environment (venv) is a private, per-project copy of
  Python's package directory, created so that two projects needing two
  different versions of the same package cannot break each other, and so
  that `pip install` cannot damage the system Python installation.
- Know that a package is a reusable library installed rather than written,
  and that PyPI (the Python Package Index) is the public repository `pip`
  and `uv` download packages from -- so a first install needs a network.
- Know that `pip` installs a package into whichever environment is
  currently active, which is why activating the right venv first is what
  decides where the package lands.
- Be able to build a venv the classic way: `python3 -m venv venv` to create
  it (`-m` runs a stdlib module as a program), `source venv/bin/activate`
  to turn it on, `pip install <pkg>` to install into it, and `deactivate`
  to turn it back off.
- Know that activation is done with the `source` builtin because `source`
  runs the script's commands in the *current* shell, which is the only way
  an on/off switch can affect that shell; an activated venv announces
  itself by prefixing the prompt with `(venv)`.
- Be able to build a venv the modern way with `uv`: `uv venv <dir>` creates
  the environment and `uv pip install --python <dir> <pkg>` installs into
  it without activating anything first.
- Know that the two workflows are the same two ideas ("make an
  environment", "install a package into it") expressed by two different
  tools, and that `uv`'s fuller project workflow (`uv init`, `uv add`,
  `uv run`) removes manual activation entirely -- which is how this
  course's own `aprog` tool is run.
- Know that inside a venv folder, `pyvenv.cfg` records which base Python
  built it and `lib/python3.*/site-packages/` is where installed packages
  actually live -- that directory *is* the private package folder.

Concept: compilers
- Know that a compiler translates human-readable source code into machine
  code the CPU can execute directly.
- Know the two required compiler families: GCC/G++ (the GNU Compiler
  Collection) and Clang/Clang++ (the LLVM project's compiler), and that
  professional C++ shops commonly use both.
- Know that `clangd` is the Clang Language Server, which IDEs run in the
  background to provide inline errors, autocompletion, and go-to-definition
  via the Language Server Protocol (LSP).
- Know that `clang-tidy` performs static analysis (finds likely bugs
  without running the program) and `clang-format` auto-formats C/C++ code.

Concept: build tools
- Know that Make reads a `Makefile` and recompiles only the source files
  that changed since the last build (incremental build).
- Know that CMake is a build-system generator: you describe your project
  in a `CMakeLists.txt`, and CMake generates the actual platform-specific
  build files (Makefiles on Linux/macOS, Visual Studio projects on
  Windows).

Concept: SFML
- Know that SFML (Simple and Fast Multimedia Library) is a C++ library
  for 2D graphics, windows, audio, and input, used by this course's
  project.
- Know that having SFML's headers present is not enough: the program
  must also link against SFML's compiled library files (via `-l` flags
  such as `-lsfml-graphics -lsfml-system`) and actually run, which is
  why this activity's verification compiles, links, and runs a small
  `sf::Image` program instead of just checking for headers.

Concept: IDE
- Know that an IDE (Integrated Development Environment) differs from a
  plain text editor by understanding your code: inline error checking,
  autocompletion, go-to-definition, and an integrated debugger, powered by
  `clangd` for C++.

Concept: git and GitHub
- Know that every git commit is stamped with a name and email from your
  global git configuration.
- Know that the GitHub CLI (`gh`) authenticates git operations and can
  clone/create repositories from the command line.
- Know that `~/.gitconfig` is the global git configuration file and that
  every repository has a hidden `.git/` directory storing its full history.

## Study checklist

- [ ] Explain what PATH is and how the shell uses it to find a program.
- [ ] State which two compiler families this course requires and why both.
- [ ] Explain the difference between Make and CMake.
- [ ] Explain why `pip install` outside a virtual environment can fail on
      modern Linux, and what fixes it.
- [ ] Name one classic/modern tool pair used for Python formatting and one
      used for type checking.
- [ ] Create a virtual environment, activate it, install a package into it,
      and deactivate it -- using both `python3 -m venv`/`pip` and `uv`.
- [ ] Explain why activation uses `source` rather than running the activate
      script as a normal program.

## Practiced in

`env-setup-shell`, `env-setup-python`, `venv-workshop`, `env-setup-compiler`, `env-setup-build-tools`, `env-setup-sfml`, `env-setup-ide`, `env-setup-git`, `env-setup-discord`
