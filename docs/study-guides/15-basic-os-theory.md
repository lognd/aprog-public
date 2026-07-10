# Study Guide 15: Basic OS Theory

This module drops below C++'s standard library entirely and works directly
against the four POSIX system calls every file operation eventually reduces
to: `open()`, `read()`, `write()`, and `close()`. Students learn the
layered file I/O stack, the precise contracts and error conventions of
each call, and then write a raw-syscall hex dump utility.

## Know before you start

- `argv`/`argc` and passing a `const char*` filename argument [assumed:
  row 14 -- Command Line Arguments]
- Manual buffer management and byte-level reasoning about C strings
  [assumed: row 12 -- C-Style Strings & Arrays]

## Taught here

Concept: what an operating system is
- Know that an operating system (OS) is a resource manager and abstraction
  layer that mediates between every running program and the physical
  hardware -- it is not a user interface, not a programming language, and
  not the hardware itself.
- Know the distinction between a kernel (the privileged core program that
  directly manages the CPU, memory, and devices) and an OS distribution
  (that kernel bundled with a shell, utilities, libraries, and a package
  manager into one installable product): Linux is a kernel; Ubuntu,
  Fedora, and Debian are distributions built around it. macOS is built
  around a kernel called XNU; Windows is built around a kernel called NT.
- Know that the CPU itself enforces two privilege levels, user mode and
  kernel mode: ordinary programs run in user mode and cannot execute the
  instructions needed to touch hardware directly; only the kernel runs in
  kernel mode.
- Know that a system call (syscall) is the controlled doorway between the
  two: it switches the CPU from user mode into kernel mode so the kernel
  can perform privileged work, then returns control to user mode.
- Know the three problems every OS solves: sharing (refereeing many
  programs' access to one CPU, disk, and memory), isolation (containing
  one program's crash so it cannot corrupt another program's memory), and
  abstraction (letting a program say "open this file" without knowing the
  disk-block and filesystem details underneath).
- Know that a process is a running program plus its own private memory and
  its own fd table; two runs of the same compiled program are two separate
  processes, each with its own independent fd table.

Concept: the file I/O stack and system calls
- Know that `open()`, `read()`, `write()`, and `close()` are POSIX system
  calls -- requests a program sends to the kernel (the core OS program
  controlling disk, memory, and CPU) -- not C++ language features.
- Know the layered structure: program -> POSIX wrapper (in libc) -> kernel
  fd table (a per-process list mapping small integer file descriptors to
  open files) -> VFS (virtual file system, the kernel layer presenting many
  filesystem types through one interface) -> disk.
- Know that a file descriptor (fd) is a small per-process integer handle
  the kernel returns from `open()`; fd 1 is always standard output.
- Know that the kernel hands out the lowest currently unused fd number, not
  a random one.
- Know that a system call switches the CPU from user mode to a privileged
  kernel mode, and that libc wrappers are thin: they place arguments in
  registers, execute the `syscall` instruction, and translate a negative
  kernel return value into setting `errno` and returning -1.

Concept: contracts of open/read/write/close
- Know that `read()` and `write()` are allowed to transfer fewer bytes than
  requested in a single call (a partial read/write) -- this is not an
  error, and a caller that needs all N bytes must loop, accumulating bytes,
  until it has them all.
- Know that `read()` returns 0 to signal EOF (end of file, no more data),
  a positive count for bytes actually read, and -1 on error.
- Know that `errno` is only meaningful immediately after a call returns -1;
  on success it is not reset and may hold a stale value from an earlier
  failure, so the return value must be checked before consulting `errno`.
- Know common `errno` values for `open()`: ENOENT (no such file), EACCES
  (permission denied), EMFILE (too many open files for this process), and
  EBADF (bad file descriptor).
- Know that EINTR is the errno set when a slow system call is interrupted
  by a signal before completing, and that the correct response is to retry
  the call.
- Know that `perror()` prints a human-readable message for the last error
  to stderr, and that every `open()` should be paired with an eventual
  `close()` to avoid leaking a file descriptor (a resource leak).
- Be able to write a correct read loop of the form `while ((n = read(fd,
  buf, sizeof(buf))) > 0) { ... }` that stops on EOF (0) or error (-1).

Concept: raw syscall-level programming
- Be able to implement a small program (a text dumper or a hex dump
  utility) using only `open()`, `read()`, `write()`, `close()`, and
  `exit()` -- no `printf`, `cout`, `fopen`, or dynamic allocation.
- Be able to convert binary byte values to hex digit characters using only
  integer arithmetic (no formatting library).
- Be able to produce fixed-width, byte-exact formatted output by writing
  pre-assembled bytes with `write()`, including correct padding when a
  final line has fewer bytes than a full row.

## Study checklist

- [ ] Name the four POSIX calls this module centers on and one guarantee
      each makes.
- [ ] Explain why a `read()` loop must check for a partial read instead of
      assuming the buffer is always fully filled.
- [ ] Explain when `errno` is safe to read and when it is stale.
- [ ] Trace the layers a call to `open()` passes through from your code to
      the kernel and back.
- [ ] Convert a byte value to two lowercase hex digit characters using only
      arithmetic.

## Practiced in

`os-mental-models`, `posix-file-tour`, `file-io-contracts`,
`write-your-first-syscalls`, `hex-dump`
