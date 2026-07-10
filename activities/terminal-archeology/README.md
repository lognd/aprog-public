# Activity: Terminal Archeology

You have been dropped into an unfamiliar directory tree containing a broken
C++ project -- no editor, no IDE, no file browser, just a shell. This is
what joining an existing codebase actually feels like the first time: dozens
of files with plausible-sounding names, missing pieces, and no map. Your
job is to find your way around using nothing but terminal commands, figure
out what is broken, and fix it well enough to compile and run.

## Background

Exploring an unfamiliar filesystem from the shell comes down to a handful of
commands used over and over, in combination:

**Navigation** -- `pwd` prints where you are, `ls` lists what is in the
current directory, `ls -a` also shows hidden entries (anything starting with
a `.`, which `ls` hides by default), and `cd <path>` moves you there.
`ls -la` combines "show hidden" with a long-format listing that includes
permissions, size, and modification time -- useful for spotting something
that looks out of place.

**Reading files** -- `cat <file>` dumps a whole file to the terminal, which
is fine for short files but unwieldy for long ones. `head -n 20 <file>`
shows just the first 20 lines, useful for getting a feel for a file's
contents or its type without printing everything.

**Identifying files by content, not just name** -- a file's extension is a
hint, not a guarantee. The `file <path>` command inspects the actual bytes
and reports what kind of content it holds (ASCII text, an ELF binary --
the executable file format Linux uses for compiled programs -- a
compressed archive, and so on). `strings <path>` extracts every
printable run of characters from a file, including binaries -- useful for
finding readable text buried inside something that is not a plain text
file.

**Searching across a whole tree** -- `find <dir> -name <pattern>` walks a
directory tree recursively looking for files matching a name pattern, for
example `find . -name "*.cpp"` to locate every C++ source file no matter how
deeply nested. `grep -r "<text>" <dir>` walks a directory tree recursively
looking *inside* files for a string, for example `grep -r "main(" .` to find
which file defines the program's entry point. Combining the two -- first
narrowing with `find` to a set of files, then searching inside them with
`grep` -- is the core loop of exploring any codebase you did not write.

Once you know which files matter and what they need, compiling a multi-file
C++ project by hand means telling the compiler where to look for headers
that are not in the same directory as the source file including them. The
`-I<dir>` flag adds `<dir>` to the compiler's search path for `#include`
directives, so a command like `g++ -I include -o program src/main.cpp`
tells `g++` to also look inside `include/` whenever it sees an `#include`
that a bare relative lookup would not find.

## Concepts covered

- `pwd`, `ls`, `ls -a`, `cd` for navigating an unfamiliar directory tree
- Hidden files and directories (names starting with `.`) and why they are
  easy to miss
- `file`, `strings`, `head`, `cat` for inspecting file contents before
  committing to reading them fully
- `find -name` and `grep -r` as complementary search strategies: find by
  filename, then search inside file contents
- Locating `main` in a multi-file project and constructing a `g++ -I`
  command to compile it by hand

## How it works

A sandboxed directory tree is mounted from a disk image and you are dropped
into a shell rooted at it. Navigate using only terminal commands -- no
editor beyond what you need to add a couple of lines to one file, no IDE,
no file manager. You must accomplish five things:

1. Find every `.cpp` file in the tree.
2. Determine which one contains `main`.
3. Figure out which headers the entry-point file needs, and which of the
   files offered under the project's `include/` directory are the real
   ones versus decoys.
4. Add the correct `#include` lines and construct a `g++` command (with
   `-I` as needed) that compiles the project successfully.
5. Run the compiled binary to obtain the passphrase.

Not every file you find is trustworthy. Some exist specifically to waste
your time if you include them without checking first -- read before you
commit.

This activity requires root access to mount the sandbox filesystem as a
loopback device -- a way of treating a plain disk-image file as if it were
a real, mountable drive, without any physical hardware involved.

```bash
sudo python3 launch.py
```

### Step 1 -- get your bearings

```bash
pwd
ls -la
```

See what top-level directories exist. This tree is organized like a real
(if slightly over-organized) C++ project: source directories, a library
directory, tooling, and headers kept separately.

### Step 2 -- find every .cpp file

```bash
find . -name "*.cpp"
```

There are far more of these than you need. Most are filler -- realistic
looking source files that are not part of the path from `main` to the
passphrase. Do not try to read all of them.

### Step 3 -- find main

```bash
grep -rl "int main" .
```

This narrows the field to exactly one file. Read it with `cat`. It will
tell you, in its own comments, what is missing and warn you that not every
candidate header is trustworthy.

### Step 4 -- find and evaluate the headers

Look at what is available under the project's header directory, including
hidden entries (`ls -a`). Use `cat`, `head`, or `grep` to inspect candidates
before including them -- some contain deliberate compile errors as a signal
that they are not the ones you want. Read any error messages you trigger;
they are written to be informative; a candidate file that intentionally
fails to compile is telling you something.

### Step 5 -- edit main and compile

Add the `#include` lines the entry-point file is missing, then compile with
an explicit `-I` flag pointing at the header directory:

```bash
g++ -I <header-dir> -o program <path-to-main.cpp>
```

If the compiler complains about a missing symbol (a function or variable
it cannot find a definition for) or a triggered `#error` (a preprocessor
directive that deliberately halts compilation with a custom message),
that is signal, not failure -- go back to Step 4 and reconsider which
headers you included.

### Step 6 -- run it

```bash
./program
```

If it prints the passphrase, you are done. If it does not compile or does
not print anything, revisit which headers you chose in Step 4.

### Step 7 -- exit

```bash
exit
```

## You will know you are done when...

You can run `./program` (or whatever binary your `g++` command produces)
and it prints the passphrase.

## Hints

<details>
<summary>Hint 1 -- narrow before you read</summary>

Do not open every `.cpp` or `.hpp` file in the tree one at a time. Use
`grep -rl` to narrow to the one file that defines `main`, and let that
file's own comments tell you what to look for next.

</details>

<details>
<summary>Hint 2 -- hidden does not mean invisible</summary>

`ls` without `-a` never shows entries whose name starts with a `.`. If a
directory looks sparse or a comment hints that something is "hidden," try
`ls -a` in that directory specifically before concluding a file does not
exist.

</details>

<details>
<summary>Hint 3 -- a compile error is information, not a dead end</summary>

Some headers are built to fail on purpose, with a message explaining why
they are the wrong choice. Reading that message is faster than guessing
again -- it is part of the exploration, not a punishment for guessing
wrong.

</details>

<details>
<summary>Hint 4 -- grep is not just for main</summary>

Once you have narrowed to a handful of candidate headers, `grep` inside
them for suspicious markers (like `#error`) before you bother including
them at all -- you can rule out several candidates in one command instead
of compiling repeatedly.

</details>

## Going further

- After finishing, write down the exact `g++` command you used and explain
  each flag. Could you have used a Makefile instead? Write one.
- Look up `nm` and `objdump`. How could you use them to find which `.o` file
  defines a given symbol without reading the source?
- Explore what `ldd` tells you about the binary you compiled. What shared
  libraries does it depend on?
- Time yourself doing the same exploration with `find` and `grep` versus
  opening files one at a time in an editor. How much does having the right
  search commands change the time it takes to orient in an unfamiliar tree?
