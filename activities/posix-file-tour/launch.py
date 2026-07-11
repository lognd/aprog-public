#!/usr/bin/env python3
"""Activity: POSIX File I/O Tour

Paginated walkthrough: start at the full stack and peel back each layer
down to the kernel fd table.  A short checkpoint at the end of each
section confirms the student engaged with the content.  All seven
checkpoints correct unlocks the passphrase.
"""
import hashlib as _hl
import hmac as _hm
import sys
import textwrap as _tw

# -- Crypto --
_SALT      = bytes.fromhex("a3f1b2c4d5e6f7a8b9c0d1e2f3a4b5c6")
_KDF_ITERS = 100000

def _derive_key(answers):
    return _hl.pbkdf2_hmac("sha256", "|".join(answers).encode(), _SALT, _KDF_ITERS)

def _stream(key, length):
    ks, i = b"", 0
    while len(ks) < length:
        ks += _hl.sha256(key + i.to_bytes(4, "little")).digest()
        i += 1
    return ks[:length]

def _decrypt(blob_hex, answers):
    blob    = bytes.fromhex(blob_hex)
    key     = _derive_key(answers)
    ct, mac = blob[:-32], blob[-32:]
    if not _hm.compare_digest(mac, _hm.new(key, ct, _hl.sha256).digest()):
        return None
    return bytes(a ^ b for a, b in zip(ct, _stream(key, len(ct)), strict=False)).decode()

_BLOB = "d18d4dbc950a80cf126a87316dbdcbf221f165fb65b539a55ad4e475f9700d6579b0bd35ed15e2b1abd527fa5ddc7eee2eda4f22c8ab"

# sha256(correct_answer) for each checkpoint, in section order.
# Answers are validated immediately so students know right away.
_CHECKPOINT_HASHES = [
    "31856a3a3dec82edd678aaf512331d100a16f81427264e52231fe312673d430e",
    "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
    "1bad6b8cf97131fceab8543e81f7757195fbb1d36b376ee994ad1cf17699c464",
    "5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9",
    "6842addfad0d7b69f24d2857c9e7c2ed2e0ad1e5edf0f48bd91712e8e408207c",
    "7e6b710b765404cccbad9eedcff7615fc37b269d6db12cd81a58be541d93083c",
    "5504990ce649a0814c511b01a64f38627f53d29714bcabe09a87c84407630f3a",
]

# -- Display helpers --
_LINE_WIDTH = 70

def _banner(title):
    print("=" * _LINE_WIDTH)
    pad = max(0, (_LINE_WIDTH - len(title) - 2) // 2)
    print(" " * pad + " " + title + " " + " " * pad)
    print("=" * _LINE_WIDTH)

def _hr():
    print("-" * _LINE_WIDTH)

def _print_block(text):
    for para in text.strip().split("\n"):
        if para.strip() == "":
            print()
        elif para.startswith("  ") or para.startswith("\t"):
            print(para)
        else:
            for ln in _tw.wrap(para, width=_LINE_WIDTH - 2,
                               initial_indent="  ", subsequent_indent="  "):
                print(ln)

def _show_passphrase(passphrase):
    print()
    _hr()
    print(f"  Passphrase: {passphrase}")
    _hr()
    print()

# -- Section definitions --
# Each section has: title, body text, checkpoint question, answer hash.
SECTIONS = [
    {
        "title": "Section 1 of 7 -- The Full Stack",
        "body": """\
Here is every layer your program passes through when it reads a file:

  Your C++ code
    |  calls POSIX functions: open(), read(), write(), close()
    v
  libc  (the C standard library)
    |  thin wrappers: save registers, invoke syscall, set errno on error
    v
  syscall instruction
    |  CPU switches from user mode to kernel mode
    v
  Kernel fd table        <-- we stop here
    |
    v  (Operating Systems class material below this line)
    |
  VFS  (Virtual File System -- abstracts the filesystem type)
    v
  Filesystem driver  (ext4, FAT32, NTFS, ...)
    v
  Block device driver
    v
  Disk  (SSD, HDD, network mount, RAM disk, ...)

This activity covers your code, the POSIX functions, and the kernel fd
table.  You need to know the vocabulary for the layers below -- VFS,
filesystem driver, block device -- because you will hear those terms in
an Operating Systems course.  You do not need to understand how they
work today.

CONTRACT at the user/kernel boundary:
  Your program makes a request via a system call.
  The kernel either fulfills it (returns a useful value)
  or refuses it (returns -1 and sets errno).
  The kernel never throws C++ exceptions; it only returns integers.\
""",
        "question": """\
What kernel data structure does the fd integer index into?

  Type exactly one of: inode / fd table / page cache / VFS\
""",
        "hash": "31856a3a3dec82edd678aaf512331d100a16f81427264e52231fe312673d430e",
        "ok":   "Correct.  The fd is an index into the kernel's per-process fd table.",
    },
    {
        "title": "Section 2 of 7 -- File Descriptors",
        "body": """\
The handle the kernel gives back is a small non-negative integer called a
file descriptor (fd).  The kernel maintains a per-process fd table: a
fixed-size array where each slot holds information about one open file.

Every process starts with three fds already open:
  fd 0 -- stdin   (keyboard by default)
  fd 1 -- stdout  (terminal by default)
  fd 2 -- stderr  (terminal by default)

These three will come up again when we cover streams.  For now, the
important thing is that write(1, ...) is how you send bytes to the
terminal -- you are writing to fd 1, which happens to be your screen.

When you open a new file, the kernel assigns the lowest available integer.
If 0, 1, and 2 are the only open fds, the next open() returns 3.

IMPORTANT -- did anyone say files had to be stored on disk?

An fd is not a "disk file handle."  It is a slot in the kernel's fd
table.  That slot can refer to:
  - A regular file on disk
  - A pipe between two processes
  - A network socket
  - A device like /dev/null, /dev/urandom, or a USB port
  - A timer, an event queue, or a block of shared memory

The POSIX interface -- open, read, write, close -- is the same regardless
of what is on the other side.  read() from a pipe looks identical to
read() from a disk file.  The kernel handles the difference; your code
does not.  This is the point of the abstraction.

We will see this again when we cover streams and network programming.

CONTRACT
  An fd is a small non-negative integer, valid only in this process.
  It is valid from the moment open() succeeds until you call close().
  Passing an invalid or closed fd to read() or write() is an error (EBADF).
  fd 0, 1, 2 are always pre-wired to stdin, stdout, stderr.\
""",
        "question": "Which fd number is stdout?  Type a number.",
        "hash": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
        "ok":   "Correct.  fd 1 is stdout in every POSIX process.",
    },
    {
        "title": "Section 3 of 7 -- open()",
        "body": """\
  #include <fcntl.h>

  int fd = open(const char *path, int flags);
  int fd = open(const char *path, int flags, mode_t mode);

'flags' is a bitmask.  Combine values with the | operator:
  O_RDONLY   -- open for reading only
  O_WRONLY   -- open for writing only
  O_RDWR     -- open for reading and writing
  O_CREAT    -- create the file if it does not exist (requires mode)
  O_TRUNC    -- if the file exists, truncate it to zero bytes
  O_APPEND   -- all writes go to the end of the file (atomically)

'mode' only matters when O_CREAT is set.  0644 is the conventional
default: owner can read and write; everyone else can only read.

Return values:
  >= 0   the new fd  (always the lowest available integer)
    -1   failure; errno is set to say why

Common errno values:
  ENOENT -- file does not exist and O_CREAT was not set
  EACCES -- permission denied
  EMFILE -- process has already reached its fd limit

CONTRACT
  Provide a path and flags.
  On success: you own an fd; you are responsible for closing it.
  On failure: no fd was allocated; read errno before doing anything else.\
""",
        "question": "What integer does open() return on any failure?  Type a number.",
        "hash": "1bad6b8cf97131fceab8543e81f7757195fbb1d36b376ee994ad1cf17699c464",
        "ok":   "Correct.  All POSIX I/O functions return -1 on failure.",
    },
    {
        "title": "Section 4 of 7 -- read() and write()",
        "body": """\
  #include <unistd.h>

  ssize_t read (int fd, void       *buf, size_t count);
  ssize_t write(int fd, const void *buf, size_t count);

ssize_t is a signed integer type (unlike size_t, which is unsigned) --
signed so it can represent -1 for "error" alongside a byte count.

read() asks the kernel for up to 'count' bytes from 'fd' into 'buf'.
Return values:
   > 0   bytes actually transferred (may be less than count -- normal)
     0   end of file; there are no more bytes to read
    -1   error; errno is set

write() sends up to 'count' bytes from 'buf' to 'fd'.
Return values:
   > 0   bytes actually written (may be less than count -- normal)
    -1   error; errno is set

Both calls may transfer FEWER bytes than requested.  This is not an
error -- it is called a partial transfer.  If you need all N bytes,
you must loop:

  ssize_t total = 0;
  while (total < (ssize_t)count) {
      ssize_t n = read(fd, buf + total, count - total);
      if (n == 0) break;        // EOF
      if (n  < 0) { perror("read"); break; }
      total += n;
  }

CONTRACT  read():
  Caller provides a buffer; kernel fills it (up to count bytes).
  Returns actual bytes moved, 0 for EOF, -1 for error.
  A short read is normal; looping is the caller's responsibility.

CONTRACT  write():
  Caller provides data; kernel drains as many bytes as it can.
  Returns actual bytes written, -1 for error.
  A short write is normal; looping is the caller's responsibility.\
""",
        "question": "What integer does read() return when it reaches end-of-file?  Type a number.",
        "hash": "5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9",
        "ok":   "Correct.  read() returning 0 means the kernel has no more bytes to deliver.",
    },
    {
        "title": "Section 5 of 7 -- close()",
        "body": """\
  #include <unistd.h>

  int close(int fd);

close() tells the kernel you are done with this fd.  The kernel frees
the slot; the integer may be reused by the next open() call.

Return values:
    0   success
   -1   error (EBADF if fd was not open; rarely, a write error on
        network filesystems -- always check)

IMPORTANT: every open() must be matched with exactly one close().

If a program opens files in a loop and never calls close(), the fd table
fills up.  When the process reaches the per-process limit (often 1024
on Linux), every subsequent open() returns -1 with errno EMFILE.  No
new files can be opened.  This is called an fd leak.  It behaves like
a memory leak: invisible in small tests, fatal in long-running programs.

close() only releases the kernel-side slot; it does not do any extra
bookkeeping on your program's side.  (Later, when you use C++ file
streams, you will meet a related function, fclose(), that also flushes
a buffer -- a temporary holding area in your own program's memory.
close() has no such buffer to flush.)

CONTRACT
  Every open() must be matched with exactly one close().
  After close(), the fd value is invalid; never pass it to read/write.
  close() on an already-closed fd is an error (EBADF, double-close).\
""",
        "question": """\
What is the name for the problem caused by calling open() without
ever calling close()?

  Type exactly one of: crash / fd leak / data loss / deadlock\
""",
        "hash": "6842addfad0d7b69f24d2857c9e7c2ed2e0ad1e5edf0f48bd91712e8e408207c",
        "ok":   "Correct.  An fd leak consumes limited kernel resources until the process can no longer open files.",
    },
    {
        "title": "Section 6 of 7 -- errno and perror()",
        "body": """\
  #include <errno.h>    // errno
  #include <stdio.h>    // perror()
  #include <string.h>   // strerror()

When a system call fails (returns -1), it sets the global integer errno
to a code describing why.  For every program you write in this course,
treat errno as one shared variable that the last failed call set.

Common errno values:
  ENOENT   -- No such file or directory
  EACCES   -- Permission denied
  EBADF    -- Bad file descriptor (fd is not open, or is invalid)
  EMFILE   -- Too many open files (process fd limit reached)
  EINTR    -- Interrupted by a signal (usually: retry the call)

RULE: errno is NOT reset on success.  If a syscall succeeds, errno
retains whatever value it had from the previous failure.  Always check
the return value of the syscall first; only read errno if the return
value was -1.

  int fd = open("file.txt", O_RDONLY);
  if (fd == -1) {
      perror("open");   // correct: we know it failed
      return 1;
  }
  // never read errno here -- open() succeeded; errno is stale

perror("prefix") prints the following to stderr (fd 2):
  prefix: <human-readable description of errno>\n

strerror(errno) returns the description as a C string, which you can
embed in a larger message or pass to write().

CONTRACT
  Check the return value first; it is the authoritative signal.
  Read errno only after a -1 return.
  perror() always writes to stderr (fd 2).  It does not exit.\
""",
        "question": """\
Which output stream does perror() always write to?

  Type exactly one of: stdout / stderr / stdin\
""",
        "hash": "7e6b710b765404cccbad9eedcff7615fc37b269d6db12cd81a58be541d93083c",
        "ok":   "Correct.  perror() always targets stderr so error messages reach the user even when stdout is redirected.",
    },
    {
        "title": "Section 7 of 7 -- Contracts in Review",
        "body": """\
Here is the complete picture of what this activity has covered:

  Layer              You work with
  -----------------  -----------------------------------------------
  Your code          Function calls, return values, errno
  POSIX functions    open / read / write / close
  Kernel fd table    Integer handle; per-process; tracks file position

The three rules that capture all of it:

  1. Check every return value.
     -1 means failure.  Read errno before doing anything else.

  2. Loop on partial transfers.
     read() and write() may move fewer bytes than requested.
     Keep going until you have moved all the bytes you need.

  3. Close every fd.
     Every open() must be matched with a close().
     An unclosed fd is a resource leak.

Below the fd table -- VFS, filesystem drivers, block devices, disk --
is material for an Operating Systems course.  You now have the
vocabulary to follow those discussions.  You do not need to implement
any of it here.

The handle the kernel returns when open() succeeds -- the integer you
pass to read(), write(), and close() -- has a specific name.\
""",
        "question": """\
What is the specific name for the integer handle the OS returns when
open() succeeds?

  Type exactly one of: fd / file descriptor / handle / descriptor\
""",
        "hash": "5504990ce649a0814c511b01a64f38627f53d29714bcabe09a87c84407630f3a",
        "ok":   "Correct.  The handle is called a file descriptor -- that is the precise term.",
    },
]


def _checkpoint(section, answers):
    while True:
        print()
        _hr()
        print()
        for ln in section["question"].strip().split("\n"):
            print(f"  {ln}")
        print()
        try:
            raw = input("  Your answer: ").strip()
        except EOFError:
            print()
            sys.exit(0)
        if not raw:
            continue
        h = _hl.sha256(raw.encode()).hexdigest()
        if h == section["hash"]:
            print()
            print(f"  {section['ok']}")
            answers.append(raw)
            return
        else:
            print(f"  [wrong] {raw!r} is not one of the listed options.")
            print("  Re-read the section above and try again.")


def main():
    _banner("Activity: POSIX File I/O Tour")
    print()
    print("  This activity walks through the full file I/O stack layer by")
    print("  layer, from the highest abstraction down to the kernel fd table.")
    print("  Each section ends with a short checkpoint question.  You must")
    print("  answer correctly to proceed.")
    print()
    input("  Press Enter to begin...")

    answers = []
    for section in SECTIONS:
        print()
        print()
        _banner(section["title"])
        print()
        _print_block(section["body"])
        _checkpoint(section, answers)

    print()
    print()
    _banner("All sections complete.")
    passphrase = _decrypt(_BLOB, answers)
    if passphrase is None:
        print("  [error] Decryption failed -- contact your instructor.")
        sys.exit(1)
    _show_passphrase(passphrase)


if __name__ == "__main__":
    main()
