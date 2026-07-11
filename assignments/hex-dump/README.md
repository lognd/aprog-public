# Hex Dump

A hex dump is one of the oldest and most useful diagnostic tools in systems
programming.  When a file is not valid text -- a compiled binary, an image,
a network packet capture -- a hex dump shows you exactly what bytes are
present and where.  Tools like `xxd`, `hexdump`, and `od` are standard
equipment for any systems programmer.

In this assignment you implement your own `hexdump` utility.  The twist:
you may only use `open()`, `read()`, `write()`, `close()`, and `exit()`.
No `printf`.  No `cout`.  No `sprintf`.  No `fopen`.  No `malloc`.  Every
byte of output must be constructed from raw arithmetic and written to fd 1
with `write()`.  ("fd" is short for **file descriptor** -- a small integer
the operating system hands your program to refer to an open file or stream.
fd 1 is always standard output, the same place `printf` and `cout` write
to; here you write to it directly with `write()` instead.)  This forces you
to work at exactly the level of abstraction the POSIX File I/O Tour
introduced.  (**POSIX** is a standard that defines a common set of
operating-system interfaces -- including `open`/`read`/`write`/`close` --
so that programs written against it behave the same way on Linux, macOS,
and other POSIX-compliant systems.)

## Learning goals

- Use `open()`, `read()`, and `close()` correctly for binary file I/O
- Implement a read loop that handles partial reads (a single `read()` call
  is not guaranteed to fill your whole buffer -- it may return fewer bytes
  than you asked for) and detects **EOF** (end of file, the point where
  `read()` returns 0 because there is no more data)
- Convert binary byte values to hex digits using integer arithmetic alone
- Produce fixed-width formatted output using `write()` without any formatting library
- Handle error conditions with `perror()` (a standard function that prints
  a human-readable message for the last system error, e.g. "No such file
  or directory") and `exit()` at the right call sites

## Task

Implement `hexdump <filename>` that produces output matching `xxd -g 1`:

```
00000000: 48 65 6c 6c 6f 2c 20 77 6f 72 6c 64 0a           Hello, world.
```

Format rules:

- **Offset field:** 8 lowercase hex digits, followed by `: ` (colon, space).
- **Hex block:** up to 16 bytes per line; each byte is two lowercase hex digits
  followed by a space.  If the last line has fewer than 16 bytes, pad the
  remaining columns with three spaces each so the ASCII block stays aligned.
- **Separator:** one additional space after the last hex column's own
  trailing space -- two spaces total between the last hex digit and the
  first ASCII character.
- **ASCII block:** each byte that is printable (0x20 through 0x7e inclusive)
  appears as itself; all other bytes appear as `.`.
- **Newline:** each output line ends with `\n`.
- An empty file produces no output and exits with code 0.

## Files

| File | Purpose |
|------|---------|
| `hexdump.cpp` | Write your implementation here |
| `CMakeLists.txt` | Build configuration -- do not modify |

## Compilation and Testing

Build with CMake:

```bash
mkdir build && cd build
cmake ..
make
```

This produces `build/hexdump`.

Test against `xxd`:

```bash
echo -n "Hello, world" | xxd -g 1
./build/hexdump <(echo -n "Hello, world")   # Linux process substitution
```

Or write a test file:

```bash
printf "Hello, world\n" > test.txt
xxd -g 1 test.txt
./build/hexdump test.txt
```

The outputs should match exactly.

You can also run the bundled visible tests, which check your binary against
a small set of sample files (plain ASCII text, non-printable bytes, an
exactly-16-byte file, an empty file, and a missing file):

```bash
bash visible-tests/run_tests.sh
```

The script assumes `build/hexdump` exists; pass an alternate path as the
first argument if you built somewhere else.

## Constraints

- Use only `open()`, `read()`, `write()`, `close()`, and `exit()` for I/O and process control.
- Do not use `printf`, `fprintf`, `sprintf`, `snprintf`, `fopen`, `fclose`, `fread`, `fwrite`, or any `std::` I/O.
- Do not use `malloc`, `new`, or `std::vector` for dynamic memory.  Stack buffers only.
- Do not modify `CMakeLists.txt`.
- The grader checks for prohibited symbols in your source at submission time.

## Grading

| Component | Points |
|-----------|--------|
| Correct output for a plain ASCII text file | 25 |
| Correct output for a binary file (non-printable bytes, padding) | 25 |
| Last line formatted correctly when file size is not a multiple of 16 | 20 |
| Empty file: no output lines, exit 0 | 10 |
| Missing or unreadable file: message to stderr, exit 1 | 10 |
| No prohibited symbols in source (`printf`, `sprintf`, `fopen`, `malloc`, etc.) | 10 |
| **Total** | **100** |

## Submission

Submit a single file named `hexdump.cpp`.  Do not rename it.

## Going further

- Extend the utility to accept an optional `-n <count>` flag that limits
  output to the first `<count>` bytes.  Parse `argv` manually -- no `getopt`.
- Add a `-s <offset>` flag that starts the dump at a byte offset, using
  `lseek()`.  Look up `man 2 lseek` to understand `SEEK_SET`.
- Measure the cost of one-byte-at-a-time reads vs.  reading 4096 bytes at
  a time.  Use `time ./hexdump /usr/bin/ls` with each approach and compare.
