# Study Guide 40: Libraries (static vs. dynamic)

This module builds a static library (`.a`) and a dynamic library (`.so`)
by hand from the same two-function source, deliberately hits the loader
error a dynamic library produces without `LD_LIBRARY_PATH`, and covers the
three-phase build model (compile, link, run) for diagnosing linker error
messages.

## Know before you start

- Object files, undefined symbols, and what the linker does [assumed:
  row 4 -- Command-Line & Compilation]
- The compile/link/run pipeline mechanics [assumed: row 4 -- Command-Line
  & Compilation]
- Makefile targets and dependencies [assumed: row 8 -- Makefile & CMake]

## Taught here

Concept: what a library is
- Know a library packages already-compiled object files together so a
  caller does not have to hand the linker each `.o` individually or
  recompile them per build.
- Know a static library (`.a`, "archive") is a bundle of `.o` files glued
  together with `ar`; the linker copies the actual machine code for every
  used function straight out of the `.a` and into the executable, which
  is then fully self-contained.
- Know a dynamic library (`.so` on Linux) is NOT copied into the
  executable -- the linker only records that the executable needs a
  library with a given name, and the operating system's loader loads the
  actual code into memory separately when the program starts, sharing one
  copy in RAM across every running program that needs it.
- Know the static-vs-dynamic tradeoff table: static means a bigger,
  self-contained executable that needs nothing extra at run time but
  requires recompiling every dependent program to pick up an update;
  dynamic means a smaller executable, shared memory across programs, and
  a library file needed at every run, but an update only requires
  replacing the `.so`.
- Know `-fPIC` ("Position-Independent Code") tells the compiler to
  generate code that works correctly no matter what address it is loaded
  at, required for object files headed into a `.so` but not for plain
  executables or static libraries.

Concept: the loader and LD_LIBRARY_PATH
- Know that a dynamically-linked binary can compile and link with zero
  errors and still fail to START, because the operating system's loader
  cannot find the needed `.so` at run time -- a distinct, later failure
  from any compile or link error.
- Know `LD_LIBRARY_PATH` is an environment variable listing extra
  directories the loader should search for shared libraries beyond its
  built-in defaults.
- Know `ldd` lists every shared library a dynamically-linked binary
  needs and where (if anywhere) it was actually found.
- Know a statically-linked binary needs no `LD_LIBRARY_PATH` help to run,
  since its library code is already copied inside it at link time.

Concept: the three-phase build model and diagnosing linker errors
- Know the three phases: compile (source to `.o`, needs only a
  declaration of anything called), link (object files and libraries
  combined into one executable, needs the actual definitions), and run
  (the executable's own execution, including the loader resolving shared
  libraries for a dynamically-linked binary).
- Know "use of undeclared identifier" is a compile-phase error (no
  declaration was ever seen); "undefined reference" is a link-phase error
  (a declaration existed but no definition was found); "error while
  loading shared libraries" is a run-phase error (the executable already
  exists and started, but the OS could not find a needed `.so`).
- Know `-L` adds a directory to the linker's library search path; `-l`
  names a library to search for (expanding to `lib<name>.a`/`.so`).
- Know GNU `ld` scans a link command left to right exactly once: a static
  library is only searched for symbols already known to be undefined at
  the moment the linker reaches its `-l` flag, so object files that use a
  library's symbols must appear BEFORE that library's `-l` flag on the
  command line.
- Know the linker's default preference when both a static and dynamic
  version of a library exist in the same search path, and that `-static`
  forces static linking instead.

## Study checklist

- [ ] Explain the static-vs-dynamic tradeoff table from memory.
- [ ] Explain what -fPIC is for and why only .so-bound objects need it.
- [ ] Reproduce the "app_dynamic fails without LD_LIBRARY_PATH" failure
      and explain why it is a run-phase, not link-phase, error.
- [ ] Classify a given error message as compile-, link-, or run-phase.
- [ ] Explain why object-file order relative to a static library's -l
      flag matters to GNU ld.

## Practiced in

`library-forge`, `link-order-lab`
