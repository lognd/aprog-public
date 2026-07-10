# Activity: Library Forge

A **library** is just precompiled code that other programs can reuse
instead of recompiling from source every time. You have been calling
into libraries all course -- every time you `#include <cstdio>` and
call `printf`, you are calling into a library that was already
compiled long before your program existed. This activity has you build
one yourself, twice: once as a **static library**, once as a
**dynamic (shared) library**, so you can feel the actual difference
between them instead of just reading about it.

## Background

Recall the compilation pipeline: a `.cpp` file becomes an **object
file** (`.o`), a binary blob of machine code with a table of the
function names it defines and the function names it still needs
(**undefined symbols**). An object file alone is not runnable -- the
**linker** has to stitch multiple object files together, resolving
every undefined symbol to an actual address, before you get one
executable.

A library packages several already-compiled object files together so
you do not have to hand the linker each one individually, and so you
do not have to recompile them every time you build a new program that
uses them. There are two very different ways to package them:

- A **static library** (`.a`, "archive") is just a bundle of `.o`
  files glued together with the `ar` tool. When the linker builds your
  executable, it copies the actual machine code for every function you
  use straight out of the `.a` and into your executable. Once linking
  is done, the `.a` file is no longer needed -- your executable is
  fully self-contained.
- A **dynamic library** (`.so`, "shared object" on Linux; `.dll` on
  Windows, `.dylib` on macOS) is not copied into your executable at
  all. The linker only records that your executable NEEDS a library
  with a given name. The actual code is loaded into memory separately,
  by the operating system, at the moment your program starts running
  -- and if several running programs need the same `.so`, the
  operating system can share ONE copy of it in memory across all of
  them, rather than every program carrying its own copy.

This has real consequences:

| | Static (`.a`) | Dynamic (`.so`) |
|---|---|---|
| Library code lives... | copied inside your executable | in a separate file, loaded at run time |
| Executable size | bigger (carries its own copy) | smaller |
| Needs the library file to run? | no -- it is already copied in | yes -- every time it starts |
| Multiple programs sharing memory | each gets its own copy | one copy in RAM, shared |
| Updating the library | must recompile every program using it | replace the `.so` file; programs pick it up next run |

Neither one is simply "better" -- production software uses both, for
different reasons. System libraries like the C standard library are
almost always dynamic, so a single security fix updates every program
on the machine without recompiling any of them. A command-line tool
you want to hand someone as one self-contained file, with no
installation step, is often built statically instead.

## Concepts covered

- Object files, undefined symbols, and what the linker actually does
- Static libraries (`.a`): `ar rcs`, and code copied at link time
- Dynamic libraries (`.so`): `-fPIC`, `-shared`, and code loaded at run time
- `LD_LIBRARY_PATH` and why a dynamically-linked binary can fail to
  start even though it compiled and linked without a single error
- `ldd`, for inspecting which shared libraries a binary actually needs

<details>
<summary>What does -fPIC mean?</summary>

`-fPIC` stands for "Position-Independent Code." Ordinary compiled code
is free to assume it will end up loaded at one particular memory
address. Code destined for a shared library cannot assume that --
different programs loading the same `.so` may end up placing it at
different addresses in their own memory, and several programs might
even load it at different addresses from each other at the same time.
`-fPIC` tells the compiler to generate code that works correctly no
matter what address it is eventually loaded at. You only need it for
object files headed into a `.so`; plain executables and static
libraries do not need it.

</details>

## How it works

`repo.zip` contains a tiny two-function math library (`mx_add`,
`mx_mul`, declared in `mathx.hpp`, defined in `add.cpp` and `mul.cpp`)
and a small `app.cpp` that calls both. The `Makefile` has four TODO
targets: two for the static side (archiving into `libmathx.a`, then
linking `app_static` against it) and two for the dynamic side
(building `libmathx.so` with `-fPIC`/`-shared`, then linking
`app_dynamic` against it).

You fill in all four TODOs and build both binaries in the same
subshell. Somewhere along the way you will run `./app_dynamic` and
watch it fail with a loader error -- that failure is not a mistake to
avoid, it is the point of the activity. When you exit, the launcher
rebuilds everything itself and checks:

- both `libmathx.a` and `libmathx.so` actually exist,
- `app_static` runs successfully with **no** `LD_LIBRARY_PATH` set,
- `app_dynamic` **fails** to run with no `LD_LIBRARY_PATH` set,
- `app_dynamic` **succeeds** once `LD_LIBRARY_PATH` points at the
  library's directory, and produces the same output as `app_static`,
- `ldd` shows `app_dynamic` actually depending on `libmathx.so`.

## Getting started

```bash
python3 launch.py
```

A shell opens inside a fresh copy of the library-forge workspace.

### Step 1 -- build and link statically

Open `Makefile` and fill in TODO 1 (archive `add.o` and `mul.o` into
`libmathx.a` with `ar rcs`) and TODO 2 (link `app.cpp` against
`libmathx.a` to produce `app_static`). Then:

```bash
make app_static
./app_static
```

It should print two lines and need nothing else at run time -- the
library's code is already copied inside `app_static`.

### Step 2 -- build and link dynamically

Fill in TODO 3 (compile `add.cpp` and `mul.cpp` with `-fPIC`, then
link the position-independent objects into `libmathx.so` with
`-shared`) and TODO 4 (link `app.cpp` against `libmathx.so` to produce
`app_dynamic`). Then:

```bash
make app_dynamic
./app_dynamic
```

Watch closely -- this will very likely fail with something like:

```
./app_dynamic: error while loading shared libraries: libmathx.so: cannot open shared object file: No such file or directory
```

This is the loader (part of the operating system, not the compiler or
the linker) trying to find `libmathx.so` at the moment `app_dynamic`
starts, and failing, because the loader's default search path does
not include your current directory.

### Step 3 -- fix it with LD_LIBRARY_PATH

`LD_LIBRARY_PATH` is an environment variable listing extra directories
the loader should search for shared libraries, in addition to its
built-in defaults.

```bash
LD_LIBRARY_PATH=. ./app_dynamic
```

This time it should print the same two lines `app_static` did.

### Step 4 -- confirm the dependency with ldd

`ldd` lists every shared library a dynamically-linked binary needs and
where (if anywhere) it was found.

```bash
LD_LIBRARY_PATH=. ldd app_dynamic
```

You should see `libmathx.so` resolved to a path inside this directory.
Try it again without `LD_LIBRARY_PATH=.` and compare -- `libmathx.so`
will show as "not found" instead.

### Step 5 -- exit

```bash
exit
```

The launcher rebuilds your code and reruns all of the checks above
itself.

## You will know you are done when...

After you exit the shell, the launcher confirms both libraries exist,
that `app_static` needs no environment help to run, that `app_dynamic`
fails without `LD_LIBRARY_PATH` and succeeds with it, and that `ldd`
shows the resolved dependency -- then it prints the passphrase.

## Hints

<details>
<summary>Hint 1 -- the ar command</summary>

`ar rcs libmathx.a add.o mul.o` -- `r` inserts the given object files
into the archive (replacing any that are already there with the same
name), `c` creates the archive if it does not exist yet, and `s`
writes an index of symbols so the linker can find things inside the
archive quickly.

</details>

<details>
<summary>Hint 2 -- linking against a library on the command line</summary>

`g++ -std=c++17 -Wall -Wextra -o app_static app.cpp -L. -lmathx` --
`-L.` adds the current directory to the linker's search path, and
`-lmathx` tells it to look there (and in the default system
directories) for a file named `libmathx.a` or `libmathx.so`. This same
line works for both `app_static` and `app_dynamic`; which one actually
gets picked is a question this course's Link Order Lab activity digs
into.

</details>

<details>
<summary>Hint 3 -- building the shared object</summary>

`g++ -shared -o libmathx.so add_pic.o mul_pic.o` -- note there is no
`-std=c++17` needed here specifically for the `-shared` step itself
(though it does no harm to include it); the object files being linked
were already compiled with `-fPIC` and the right standard flag in the
earlier compile step.

</details>

## Going further

- Run `ldd app_static` (the statically-linked binary). What does it
  report about `libmathx.so`? Why does that make sense given
  everything static linking copies in at link time?
- Delete `libmathx.so` after building `app_dynamic` and try running it
  again with `LD_LIBRARY_PATH=.` set. What error do you get now, and
  how is it different from the original "cannot open shared object
  file" error?
- Look up `LD_LIBRARY_PATH` vs. baking a search path directly into the
  binary with the linker's `-Wl,-rpath,<dir>` option. Why might a real
  piece of shipped software prefer `-rpath` over asking every user to
  set an environment variable?
- Try `nm -D libmathx.so` (or `objdump -T libmathx.so`) to list the
  dynamic symbols the shared library exports. Compare it to
  `nm libmathx.a`.
