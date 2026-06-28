# Activity: Terminal Archeology

You have been dropped into an unfamiliar directory tree containing a broken C++ project.
Your job is to explore it using only terminal commands -- no GUI file browser, no IDE, no code reading.

## Concepts covered

- `find`, `grep`, `cat`, `ls` as the primary tools for exploring an unfamiliar codebase
- Locating `main` in a multi-file project without an IDE
- Reading `#include` directives to identify missing headers and their locations
- Constructing a `g++` command with `-I` flags by hand

## How it works

A sandboxed directory tree is mounted and you are dropped into a shell.
Navigate using only terminal commands. No editor, no IDE, no file manager.

You must accomplish five things:

1. Find every `.cpp` file in the tree.
2. Determine which one contains `main`.
3. Figure out which headers are included and which are missing from the expected location.
4. Construct a `g++` command that compiles the project successfully.
5. Run the compiled binary to obtain the passphrase.

## Getting started

This activity requires root access to mount the sandbox filesystem.

```bash
sudo python3 launch.py
```

## You will know you are done when...

You can run `./program` (or whatever binary your `g++` command produces) and
it prints the passphrase.

## Going further

- After finishing, write down the exact `g++` command you used and explain
  each flag. Could you have used a Makefile instead? Write one.
- Look up `nm` and `objdump`. How could you use them to find which `.o` file
  defines a given symbol without reading the source?
- Explore what `ldd` tells you about the binary you compiled. What shared
  libraries does it depend on?
