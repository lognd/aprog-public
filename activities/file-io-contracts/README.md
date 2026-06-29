# Activity: File I/O Contracts

A contract is a precise statement of what a function requires from its
caller, and what the caller can rely on in return.  The four POSIX I/O
calls -- `open()`, `read()`, `write()`, and `close()` -- each have
contracts that are simple to state but easy to violate.  A partial read
is not an error.  `errno` is not reset on success.  An unclosed fd is a
resource leak.  These details do not show up as compile errors; they show
up as subtle bugs in production.

This activity tests whether you know the contracts precisely enough to
apply them correctly.

## Concepts covered

- `open()` return values and errno codes (ENOENT, EACCES, EMFILE, EBADF)
- The lowest-available-fd rule
- `read()` partial reads and the EOF sentinel (return value 0)
- `write()` partial writes and the retry obligation
- EINTR: what it means and what to do
- `errno` semantics: when it is set, when it is stale
- `perror()` output destination

## How it works

Ten questions, grouped in clusters by topic.  Each question shows you
exactly which answers are permitted.  Type one of them precisely
(case-sensitive, no surrounding spaces).  Wrong answers show an
explanation of why that answer is wrong; then the question re-prompts.
All ten correct unlocks the passphrase.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

After the tenth question, the terminal prints your passphrase between two
horizontal lines.

## Hints

<details>
<summary>Hint 1 -- on reading errno</summary>

errno is only meaningful immediately after a syscall returns -1.  If the
syscall succeeded, errno retains its value from whatever failed previously.
Always check the return value of the function before looking at errno.

</details>

<details>
<summary>Hint 2 -- on partial transfers</summary>

read() and write() are allowed to transfer fewer bytes than you requested.
This is not an error -- it is a property of the kernel's I/O model.  The
number returned is how many bytes actually moved.  If you need all N bytes,
you must keep calling until you have accumulated N total.

</details>

## Going further

- Look up the full list of errno codes for `open()` in `man 2 open`.
  How many are there?  What does ETXTBSY mean?
- Write a small C++ program that deliberately triggers EMFILE by opening
  files in a loop without closing them.  At what fd number does it fail?
- Research the POSIX guarantee on `write()` atomicity when using `O_APPEND`.
  Under what conditions is an append to a file guaranteed to be atomic?
