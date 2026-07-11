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
- **An empty file produces no output and exits with code 0.**
  - **Example (empty file):** running `hexdump` on a zero-byte file (e.g.
    `/dev/null`) prints nothing at all -- no lines, not even a blank one --
    and the process **exits with status 0**, same as `xxd -g 1 /dev/null`.

## Examples

Every example below was produced by compiling the reference solution and
running it against a real file, then diffed against `xxd -g 1` on the
same file -- nothing here is guessed.

Take this 17-byte input (shown here as hex bytes for reference):

```
00 01 02 1f 20 7e 7f 80 ff 41 42 0a 0d 09 78 79 7a
```

The exact output (every space significant -- this is a fenced code block
so nothing gets collapsed):

```
00000000: 00 01 02 1f 20 7e 7f 80 ff 41 42 0a 0d 09 78 79  .... ~...AB...xy
00000010: 7a                                               z
```

Why it looks like this:

- **Offset column (`00000000`, `00000010`):** always exactly **8 lowercase
  hex digits**, zero-padded on the left, no `0x` prefix. It is the byte
  offset of the FIRST byte on that line, so the second line -- which
  starts at the 17th byte (0-indexed byte 16, since 16 bytes already
  appeared on line one) -- reads `00000010` (**16 in hex is `10`**).
- **Hex block (byte-to-hex-digits rule):** each byte becomes exactly two
  lowercase hex digits (`ff` not `FF`, `0a` not `A`), each followed by one
  space, up to **16 bytes per line**. Line one is full (16 bytes, 16
  trailing spaces). Line two has only 1 real byte (`7a`) followed by 15
  columns' worth of blank padding (three spaces each, except the very last
  column which uses two spaces) so the ASCII column below still lines up
  in the same screen position on every line, whether the line is full or
  not.
- **ASCII column (printable-range rule):** one character per input byte,
  in the same left-to-right order. A byte is shown as its own ASCII
  character only if it falls in the printable range **0x20 (space) through
  0x7e (`~`) inclusive**; every other byte -- including `0x00`, `0x1f`,
  `0x7f` (DEL, one past the printable range), and `0x80`/`0xff` (high bytes
  with the top bit set) -- is shown as a literal `.` instead. **Note `0x20`
  itself (space) IS in the printable range**, so it appears as an actual
  space character in the ASCII column, not a dot -- easy to misread as a
  gap.

## Worked example: turning a few bytes into one output line, step by step

Take this 8-byte input: `48 00 2e 7f 41 0a 20 ff`. Since it is only one
line's worth of bytes (fewer than 16), `hexdump` writes a single output
line and no more `read()` calls return any data. Tracing each byte in
order:

| Byte (hex) | Hex column shows | Reason | ASCII column shows | Reason |
|------------|-------------------|--------|---------------------|--------|
| `0x48` | `48` | every byte prints as two lowercase hex digits, high nibble first | `H` | `0x48` falls in 0x20-0x7e, so it appears as its own printable character |
| `0x00` | `00` | same rule -- `0x00` is still two hex digits, not skipped | `.` | `0x00` is below 0x20 (it is the NUL byte), so it is not printable |
| `0x2e` | `2e` | two hex digits as always | `.` | `0x2e` IS the printable character `.` itself -- this happens to look identical to the "not printable" placeholder, which is a coincidence worth noticing |
| `0x7f` | `7f` | two hex digits | `.` | `0x7f` (DEL) is one past the printable range's upper bound (0x7e), so it is not printable |
| `0x41` | `41` | two hex digits | `A` | `0x41` falls in 0x20-0x7e |
| `0x0a` | `0a` | two hex digits | `.` | `0x0a` is the newline byte, below 0x20, not printable |
| `0x20` | `20` | two hex digits | ` ` (a real space) | `0x20` is the LOWER boundary of the printable range, inclusive, so it prints as an actual space character, not a dot |
| `0xff` | `ff` | two hex digits | `.` | `0xff` is above 0x7e, not printable |

**Example (short line still gets column padding):** since all 8 bytes fit
in one line, the hex block still needs **8 more "columns" of blank
padding** after them (so the ASCII block would line up if a shorter line
ever appeared next -- though here there is no next line) before the
mandatory two-space separator and the ASCII block. Putting every column
together, the exact final output line is:

```
00000000: 48 00 2e 7f 41 0a 20 ff                          H...A. .
```

Reading the tail end of that line carefully: `H...A. .` -- that is `H`
`.` `.` `.` `A` `.` (a real space) `.`, matching the table above
left to right, one character per input byte.

### A partial final row

**`hexdump` does not pad the LAST row with fake `00` bytes to reach 16** --
it only ever hex-dumps the real bytes it read, and pads the *columns*
(with blank spaces, never digits) so the ASCII block still lines up.

- **Example (5-byte input):** for input `41 42 00 ff 20`:

  ```
  00000000: 41 42 00 ff 20                                   AB.. 
  ```

  **Only 5 of the 16 hex columns hold real bytes** (`41 42 00 ff 20`);
  the remaining 11 columns are blank padding, not zeros. The ASCII column
  shows exactly 5 characters -- `A`, `B`, `.` (0x00), `.` (0xff), and a
  real space (0x20) -- **never 16**, because there is no byte to show for
  the columns that were never read.

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
