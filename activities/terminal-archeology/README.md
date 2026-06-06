# Terminal Archeology

You have been dropped into an unfamiliar directory tree containing a broken C++ project.
Your job is to explore it using only terminal commands -- no GUI file browser, no IDE, no code reading.

## Getting started

    sudo python3 launch.py

## Your objectives

1. Find every `.cpp` file in the tree.
2. Determine which one contains `main`.
3. Figure out which headers that file is trying to include and which ones are actually missing.
4. Construct a single `g++` command that would compile the project. (You need to also find the correct headers!)
5. Run the compiled binary to obtain the passphrase.

## Rules

- Terminal navigation and inspection commands only (`ls`, `find`, `grep`, `cat`, etc.)
- No opening files in an editor to read through them
- No IDE, no file manager

## Getting started

You are already in the root of the project. Start exploring.

## You'll know you're done when...

You can write out a `g++` command, explain why each part of it is there, and produce the passphrase.
