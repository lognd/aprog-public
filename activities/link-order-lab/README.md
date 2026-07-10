# Activity: Link Order Lab

A round of diagnosis questions on **linking** mechanics: what order
things must appear in on a link command line, which of three build
phases -- compile, link, or run -- produced a given error message, what
the `-L` and `-l` flags actually mean, and which library the linker
picks by default when both a static and a dynamic version of it exist
in the same place. There is no code to write here; every question is
a decision built from a short command line or error message, the same
kind of thing you saw first-hand while building Library Forge.

## Background

Every C++ program you build passes through three distinct phases, and
knowing which phase produced a given error is the fastest way to know
where to even start looking:

1. **Compile**: the compiler (`g++`, invoked once per `.cpp` file)
   turns source code into an object file (`.o`). It only needs a
   **declaration** of anything it calls (a function prototype in a
   header is enough) -- it does not need that function's actual
   **definition** to exist anywhere yet.
2. **Link**: the linker (invoked once, after every `.cpp` has been
   compiled) combines object files and libraries into one executable,
   resolving every call to an actual address. This is where it needs
   the **definitions** the compile phase was able to skip.
3. **Run**: the finished executable actually executes. For a
   dynamically-linked program, this is also when the operating
   system's loader has to find and load any shared libraries (`.so`
   files) the executable named at link time but did not copy any code
   from.

Errors from each phase look and mean different things, and this
activity is largely about telling them apart on sight: "use of
undeclared identifier" is compile-phase (the compiler never even saw a
declaration); "undefined reference" is link-phase (a declaration
existed, but no definition was ever found); "error while loading
shared libraries" is run-phase (the executable already exists and
started, but the OS could not find a `.so` it needs).

## Concepts covered

- The three-phase build model: compile, link, run
- Command-line argument order for static libraries (`.a`) and why it
  matters to GNU `ld`
- `-L` (search path) vs. `-l` (library name, with the `lib`/`.a`/`.so`
  expansion)
- The linker's default preference when both a static and dynamic
  version of a library are present
- Forcing static linking with `-static`

## How it works

Each question presents a short command line, or an error message, and
asks you to diagnose it -- which of a small enumerated set of choices
is correct (a letter, a phase name, a flag, or a short phrase). Type
your answer exactly as the prompt specifies. Getting a question wrong
shows a detailed explanation of the linking rule you missed; answer
every question correctly to reveal the passphrase.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have answered every question correctly and the launcher prints
the passphrase.

## Hints

<details>
<summary>Hint 1 -- GNU ld and static libraries are order-sensitive</summary>

GNU `ld` scans the link command left to right exactly once. A static
library (`.a`) is only searched for symbols that are ALREADY known to
be undefined at the moment the linker reaches that `-l` flag -- it is
never revisited later. Object files that USE a library's symbols must
therefore appear BEFORE that library's `-l` flag on the command line.

</details>

<details>
<summary>Hint 2 -- three phases, three kinds of "missing"</summary>

Compile-phase errors are about missing DECLARATIONS (the compiler
never even saw a prototype). Link-phase errors are about missing
DEFINITIONS (a declaration existed, but no compiled code implementing
it was found) or missing library FILES entirely. Run-phase errors are
about missing library files that the loader could not find at start
time, even though the executable itself already exists.

</details>

## Going further

- Build Library Forge's `app_dynamic` on purpose with `-lmathx` placed
  BEFORE `app.cpp` on the link line instead of after. Confirm you get
  the exact "undefined reference" failure this activity describes,
  then fix the order.
- Try linking a program with `-static -lmathx` where only `libmathx.so`
  exists (no `.a`). What error does the linker give you, and which of
  the three phases produced it?
- Research `--start-group` / `--end-group` (or `-Wl,--start-group`).
  What real-world situation with static libraries does this flag
  solve, and how does it relate to the left-to-right, never-revisited
  scanning rule this activity is built on?
