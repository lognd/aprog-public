# Activity: Binary Stream Explorer

Text streams let you ignore the underlying bytes -- the stream handles newlines,
number formatting, and whitespace automatically.  Binary streams expose the
underlying bytes directly.  When you open a file with `std::ios::binary`, every
byte you read is exactly what is stored on disk.  This matters for binary file
formats, network protocols, serialized data, and any case where you need to
control the exact layout of bytes in memory.

This activity gives you a small binary file with a known format and a C++
reader program that has three blanks left in it.  Your job is to fill in the
blanks using the hex dump (a printout of a file's raw bytes, usually shown in
hexadecimal, two hex digits per byte) shown at startup and `sizeof()` to
compute the right byte counts and offsets.  When the program prints the
correct output, the passphrase unlocks.

## Concepts covered

- `std::ifstream` with `std::ios::binary` to read raw bytes
- `f.read(reinterpret_cast<char*>(&val), sizeof(val))` -- the binary read pattern
- `f.seekg(offset)` to navigate to a specific byte position
- `sizeof(struct)` to compute record sizes and file offsets
- `reinterpret_cast<char*>` to treat any object as a byte array
- Little-endian integer layout: low byte first

## How it works

The launcher shows a hex dump of `data.bin` and drops you into a shell with
`reader.cpp`.  The file contains three records in a custom format.  The program
has three blanks marked `BLANK_A`, `BLANK_B`, and `BLANK_C`.  Fill them in,
compile, and run the program.  When the output matches the expected result, type
`exit` and the launcher will verify your work.

The three blanks are:
- `BLANK_A` -- how many bytes to pass to `f.read()` for a `uint16_t`
- `BLANK_B` -- the byte offset (seekg argument) of the record at index 1
- `BLANK_C` -- how many bytes to pass to `f.read()` for one `Record`

Use `sizeof()` rather than magic numbers where possible.

## Getting started

```bash
python3 launch.py
```

A shell opens with `reader.cpp` and `data.bin`.

### Step 1 -- read the hex dump and the format spec

Study the hex dump printed in the banner.  Match each group of bytes to the
format spec: a magic number (a fixed, recognizable sequence of bytes at the
start of a file that identifies its format -- here, the ASCII text `APRO`),
count, and then the three records back-to-back.

Confirm in the hex dump that:
- Bytes 0-3 contain `APRO` in ASCII.
- Bytes 4-5 encode the record count as a little-endian `uint16_t`.
- Each record is `id` (4 bytes) + `score` (4 bytes) + `name` (8 bytes) = 16 bytes.

### Step 2 -- fill in BLANK_A

`BLANK_A` is the second argument to `f.read()` when reading `count`.
How many bytes does a `uint16_t` occupy?  Use `sizeof(count)` -- not a literal.

### Step 3 -- fill in BLANK_B

`BLANK_B` is the argument to `f.seekg()` to position the stream at record
index 1 (the second record, 0-indexed).  Compute it from the header size (6
bytes: 4 magic + 2 count) and the record size (`sizeof(Record)`).

Verify your answer in the hex dump: the offset you compute should point to the
bytes `02 00 00 00` (id=2, little-endian).

### Step 4 -- fill in BLANK_C

`BLANK_C` is the byte count for reading one full `Record` struct.  Use
`sizeof(r)` -- the same reason you use `sizeof` everywhere: it stays correct
if the struct ever changes.

### Step 5 -- compile and run

```bash
g++ -std=c++17 -o reader reader.cpp && ./reader
```

### Step 6 -- exit when the output matches

```bash
exit
```

## You will know you are done when...

The program prints four lines matching the expected output shown in the banner
and the launcher confirms all values are correct.

## Hints

<details>
<summary>Hint 1 -- computing BLANK_B</summary>

The file header is 6 bytes (4 magic + 2 count).  Record index 0 starts at byte
6.  Record index 1 starts at byte `6 + sizeof(Record) * 1`.  `sizeof(Record)`
is `sizeof(int32_t) + sizeof(int32_t) + 8` = 16 bytes.  So record index 1
starts at byte 22.  Verify: look at offset `0x0016` in the hex dump.

</details>

<details>
<summary>Hint 2 -- the reinterpret_cast pattern</summary>

`f.read()` expects a `char*` pointer.  To read bytes into a struct or integer,
cast its address: `reinterpret_cast<char*>(&r)`.  This tells the compiler
"treat the bytes at this address as a char array" -- no data is copied or
converted.  The read fills those bytes in place.

</details>

<details>
<summary>Hint 3 -- little-endian byte order</summary>

On x86/x64, integers are stored low-byte-first (little-endian).  The
`uint16_t` value 3 is stored as `03 00`, not `00 03`.  When you read 2 bytes
directly into a `uint16_t` on the same machine, the byte order matches and
you get the correct value automatically.

</details>

## Going further

- Change the seek offset to target record index 0 and record index 2.  Confirm
  the values match what you see in the hex dump.
- Add a loop that reads ALL records without using `seekg`.  Instead, read them
  sequentially after the header.  How does the code change?
- What happens if you open `data.bin` without `std::ios::binary` on Linux?
  Try it.  What would happen on Windows, where text mode translates `\n` to
  `\r\n`?
- Write a companion `writer.cpp` that creates a new `data.bin` from scratch
  using `std::ofstream` with `std::ios::binary` and `f.write()`.  Verify that
  your reader can read the file it writes.
