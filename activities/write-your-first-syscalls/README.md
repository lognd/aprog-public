# Activity: Write Your First Syscalls

Reading about `open()`, `read()`, `write()`, and `close()` is one thing.
Writing the calls yourself -- getting the flags right, handling the return
values, looping on partial reads (calls that return fewer bytes than you
asked for) -- is another.  This activity gives you a partial C++ program
with three clearly marked blanks.  You fill them in, compile, and verify
that the program prints a file's contents to the terminal using only the
four POSIX (Portable Operating System Interface, the standard for how
programs talk to Unix-like operating systems) calls.

No `printf`.  No `cout`.  No `fopen`.  Just the kernel interface -- these
four calls talk directly to the operating system's kernel (the core
program that controls the disk, memory, and CPU) instead of going
through a buffered C library helper.

## Concepts covered

- `open()` with `O_RDONLY` and correct error handling via `perror()`
- The read loop: `while ((n = read(...)) > 0)` and why this pattern is correct
- `write()` to fd 1 (stdout) with a buffer and byte count
- `close()` as an obligation paired with every `open()`
- Using the return value of `read()` to detect EOF and errors

## How it works

The launcher extracts a working directory containing three files:

- `io_tour.cpp` -- the partial program; three sections marked `FILL IN`
- `Makefile` -- provided; do not modify
- `sample.txt` -- a short text file to test against

You edit `io_tour.cpp` in the shell, compile with `make`, and test with
`./io_tour sample.txt`.  When the output matches `sample.txt` exactly,
type `exit`.  The launcher verifies your binary automatically and reveals
the passphrase if all checks pass.

Each `FILL IN` section includes the function signature and a description
of what to write.  The blanks are one expression each -- you are not
writing a function from scratch.

## Getting started

```bash
python3 launch.py
```

A shell opens inside a fresh working directory.

### Step 1 -- read the skeleton

```bash
cat io_tour.cpp
```

Read the three `FILL IN` comments.  Each one tells you the exact function
signature and what the return value means.

### Step 2 -- fill in the blanks

Open `io_tour.cpp` in any editor (`nano`, `vim`, or `code` if available)
and replace each `/* FILL IN */` with a real function call.

### Step 3 -- compile and test

```bash
make
./io_tour sample.txt
```

The output should be the exact contents of `sample.txt`.

### Step 4 -- exit

```bash
exit
```

The launcher runs verification automatically.  If anything fails, it
describes what went wrong and returns you to the shell.

## You will know you are done when...

After typing `exit`, the launcher prints "All checks passed." followed by
your passphrase between two horizontal lines.

## Hints

<details>
<summary>Hint 1 -- open() flags</summary>

For reading a file that already exists, the flag is `O_RDONLY`.  You do
not need `O_CREAT` or `O_TRUNC`.  The path is `argv[1]`, which is already
a `const char *` -- exactly what `open()` expects.

</details>

<details>
<summary>Hint 2 -- the read loop condition</summary>

`read()` returns the number of bytes read, 0 at EOF, and -1 on error.
The condition `while ((n = read(fd, buf, sizeof(buf))) > 0)` does exactly
the right thing: it reads into `buf`, stores the count in `n`, and loops
as long as there are bytes to process.  When `read()` returns 0 (EOF) or
-1 (error), the loop exits.

</details>

<details>
<summary>Hint 3 -- close() syntax</summary>

`close(fd)` takes one argument: the fd you got from `open()`.  It returns
0 on success and -1 on error.  For this exercise, calling it without
checking the return value is acceptable.

</details>

## Going further

- Modify `io_tour.cpp` to copy `argv[1]` to `argv[2]` instead of printing
  to stdout.  You will need `O_WRONLY | O_CREAT | O_TRUNC` and a second fd.
- Add a write loop inside the existing read loop to handle partial writes
  from `write()`.  Under what conditions would `write()` to stdout return
  less than `n`?
- Try opening `argv[1]` with `O_RDONLY | O_NONBLOCK`.  What changes?
  Look up `man 2 open` to understand the flag.

---

<details>
<summary>Extra -- what is a system call, and what does libc do?</summary>

This section is for curious students.  You do not need this to complete
the activity or to use `open()`, `read()`, `write()`, and `close()`.

**What is a system call?**

A system call (syscall) is a request from your program to the operating
system kernel.  The kernel runs in a privileged CPU mode called "kernel
mode."  Your program runs in "user mode."  User-mode code cannot directly
touch hardware, other processes' memory, or kernel data structures.

When your program needs to do something privileged -- open a file, send
a network packet, allocate memory from the OS -- it executes a special
CPU instruction (on x86-64: `syscall`; on ARM: `svc`; on RISC-V: `ecall`).  
This instruction does three things atomically:

  1. Saves the current program state (registers, instruction pointer).
  2. Switches the CPU to kernel mode.
  3. Jumps to a fixed address in the kernel called the syscall entry point.

The kernel reads the syscall number and arguments from specific registers,
does the work, writes the return value back to a register, and executes
`sysret` to return to user mode.  Your program resumes exactly where it
left off, as if a normal function returned.

The whole round-trip is fast -- typically 100--500 nanoseconds on modern
hardware -- but it is not free.  That is one reason high-performance code
tries to minimize syscall count (e.g., by reading large chunks at a time
rather than one byte per `read()` call).

**What does libc do?**

The functions you call -- `open()`, `read()`, `write()`, `close()` -- are
not in the kernel.  They live in libc, the C standard library (on Linux,
this is glibc).  Each one is a thin wrapper around the actual syscall.

What the wrapper does:

  1. Places the syscall number and arguments in the right registers.
  2. Executes the `syscall` instruction.
  3. On return, checks whether the kernel reported an error.
     If the raw return value is a large negative number (the kernel's
     error encoding), libc negates it, stores the result in `errno`,
     and returns -1.
  4. Otherwise, returns the kernel's result directly.

That is the entire job of the wrapper.  There is no magic.  `open()` in
glibc is roughly 20 lines of assembly.

You can see this yourself with `strace`:

  strace ./io_tour sample.txt

`strace` intercepts every syscall and prints it.  You will see lines like:

  openat(AT_FDCWD, "sample.txt", O_RDONLY) = 3
  read(3, "Every file...", 4096)           = 246
  write(1, "Every file...", 246)           = 246
  close(3)                                 = 0

Notice `openat` instead of `open`.  On modern Linux, `open()` in libc
actually invokes the `openat` syscall (which takes an extra directory fd
argument for relative paths).  This is a libc implementation detail; from
your code's perspective you called `open()`.

**The layers again, with more detail:**

```text
  Your call: open("sample.txt", O_RDONLY)
    |
    v
  libc wrapper: set syscall number (257 = openat on x86-64),
    set args in registers in the CPU, execute `syscall` instruction
    |
    v
  CPU: save user registers, switch to kernel mode, jump to entry
    |
    v
  kernel: look up "sample.txt" in the directory, check permissions,
    allocate an entry in this process's fd table, fill in file offset = 0
    |
    v
  kernel: write fd number (e.g., 3) into rax, execute `sysret`
    |
    v
  CPU: restore user registers, switch back to user mode
    |
    v
  libc: read rax; if negative, set errno and return -1; else return 3
    |
  Your code receives: fd = 3
```

Everything below the fd table -- how the kernel finds "sample.txt" on
disk, how it translates a filename to an inode, how it moves data from
the block device into memory -- is the subject of an Operating Systems
course.

</details>
