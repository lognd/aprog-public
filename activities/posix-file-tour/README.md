# Activity: POSIX File I/O Tour

Every C++ program that reads or writes a file eventually makes the same
four calls: `open()`, `read()`, `write()`, and `close()`.  These are not
C++ -- they are POSIX system calls, and they are the same four calls
your shell, your text editor, and your compiler make.  Understanding
them at this level of detail will pay off every time you work with files,
processes, or sockets for the rest of your career.

This activity walks through the complete file I/O stack one layer at a
time, starting at the highest abstraction and working down to the kernel
fd table.  Each section ends with a short checkpoint question.

## Concepts covered

- The layered structure of the file I/O stack (program -> POSIX -> kernel fd table -> VFS, the virtual file system layer that lets the kernel present many different filesystem types through one interface -> disk)
- File descriptors as per-process integer handles
- The contracts of `open()`, `read()`, `write()`, and `close()`
- Partial reads and writes, and why callers must loop
- `errno` semantics: check return value first; read errno only on failure
- `perror()` and `strerror()` for human-readable error reporting

## How it works

The launcher walks through seven sections of content displayed in the
terminal.  Each section covers one layer or concept.  After the content,
a checkpoint question asks you to confirm what you just read.  The
question tells you exactly which answers are valid -- type one of them
precisely (case-sensitive).

Correct answers advance you to the next section.  Wrong answers replay
the prompt.  The passphrase is revealed after all seven checkpoints.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

After the seventh checkpoint, the terminal prints your passphrase between
two horizontal lines.

## Going further

- After the activity, open a terminal and run `man 2 open` to read the
  full POSIX specification.  Compare the flag list to what was covered here.
- Run `strace ./some_program 2>&1 | grep -E "open|read|write|close"` on
  any binary on your system.  Every file operation will appear as one of
  these four calls.
- Look up `ulimit -n` in your shell.  That is the per-process fd limit
  described in the close() section.  Try lowering it and see what breaks.
- Research what `O_NONBLOCK` does and why it matters for network sockets.
  This is a preview of how the same four calls handle network I/O.
