# Activity: Union Dissector

Every variable you write in C++ has a type, and that type tells the compiler
how to interpret the bits stored at that variable's address.  An `int` and a
`float` can occupy the same number of bytes, but the bits mean completely
different things depending on which type you use to look at them.  Normally
the compiler enforces this separation strictly -- you cannot just tell it "I
know these bytes are really a float, please read them that way."  If you try
using pointer casts to force a reinterpretation, you get undefined behavior.
If you use `memcpy` into a different type, you get the correct answer but at
the cost of a copy and a lot of boilerplate.

A `union` is the language's built-in solution to this problem.  It declares a
block of memory that can be legally read through any of its named members.
All members share the same starting address and the same bytes.  Writing to
one member and reading from another is the intended use -- no cast, no copy,
no undefined behavior (with some caveats you will explore in Going Further).

Why does this matter outside of academic exercises?  Here are three real
situations where unions appear:

- **Binary file formats and network protocols** store multi-byte integers in a
  specific byte order.  A union lets you write raw bytes into a buffer and
  read them back as a typed value without any casting gymnastics.
- **Hardware registers** are memory-mapped addresses where the same bytes must
  be read as bit fields, as a single integer, and sometimes as individual
  bytes -- all depending on which part of the driver is running.
- **Discriminated unions** (also called tagged unions or sum types) are a
  pattern for storing one of several possible types in the same space, with an
  enum alongside telling you which one is currently valid.  Languages like
  Rust and Swift build this in natively; in C and C++ you build it yourself
  with a `union` and a tag.

This activity connects directly to something surprising: **a floating-point
number is not a number you can see directly.**  It is a specific arrangement
of 32 bits defined by the IEEE 754 standard.  There is a sign bit, 8 exponent
bits, and 23 mantissa bits.  The value `1.0f` happens to have the bit pattern
`0x3F800000`.  You cannot normally see that pattern -- the compiler always
shows you the float value.  A union lets you see the raw bits by reading the
same memory through a `uint32_t` instead.

---

## Concepts covered

- `union` memory layout -- all members occupy the same bytes simultaneously
- `sizeof(union)` equals the size of its largest member, not the sum
- Type punning: reinterpreting bits without conversion
- Why reading through a non-active union member is defined in C but
  technically undefined in C++ (and why `memcpy` is the standard-safe route)
- Byte-level hex inspection with `printf` and `%02x`
- IEEE 754 floating-point representation: how `1.0f` and `-0.0f` look in bits

---

## How it works

You are given a file called `union_lab.cpp` with a `ByteView` union already
defined.  It has three members that all overlap the same 4 bytes:

```cpp
union ByteView {
    uint32_t      as_uint;   // 4 bytes, unsigned integer view
    float         as_float;  // 4 bytes, IEEE 754 float view
    unsigned char bytes[4];  // 4 bytes, one-at-a-time byte view
};
```

There are four TODO blocks.  Each one asks you to write one or two lines of
code and produces one line of output.  When all four TODOs are filled in and
the program compiles and runs, its output must match the expected output
exactly.  The launcher compares your program's stdout against the expected
output and unlocks the passphrase only if they match character-for-character.

The expected output (in order) is:

```
as_float: 1
bytes: 00 00 80 3f
neg_zero_bits: 80000000
sizeof(ByteView): 4
```

The second line -- `bytes: 00 00 80 3f` -- is the most surprising.  You
stored `0x3F800000` as a `uint32_t`, but the bytes appear reversed.  This is
**little-endian** byte order: on x86 and x64 machines, the least-significant
byte of a multi-byte integer is stored at the lowest address.  `bv.bytes[0]`
holds the least-significant byte of `0x3F800000`, which is `0x00`.
`bv.bytes[3]` holds the most-significant byte, which is `0x3F`.  This is not
a bug -- it is how your CPU stores integers.  Binary file formats that must be
portable across architectures have to account for this explicitly.

---

## Getting started

```bash
python3 launch.py
```

A shell opens inside a fresh copy of the workspace.

### Step 1 -- read the starter file

```bash
cat union_lab.cpp
```

Read the union definition and the four TODO comment blocks.  Each block shows
exactly what output line your code must produce.

### Step 2 -- fill in TODO 1

Open `union_lab.cpp` in your editor.  In the TODO 1 block:

1. Set `bv.as_uint = 0x3F800000u;`
2. Print `bv.as_float` with `printf("as_float: %g\n", bv.as_float);`

The `%g` format prints a float without unnecessary decimal places, so `1.0`
prints as `1`.  That is what the expected output requires.

### Step 3 -- fill in TODO 2

In the TODO 2 block, loop over `bv.bytes[0]` through `bv.bytes[3]` and print
each as a two-digit lowercase hex number.  The format string for one byte is
`" %02x"` -- the `02` means "pad with zeros to at least 2 digits."  Start the
line with `printf("bytes:");`, then print each byte inside the loop, then
finish with `printf("\n");`.

### Step 4 -- fill in TODO 3

In the TODO 3 block:

1. Set `bv.as_float = -0.0f;`
2. Print `bv.as_uint` with `printf("neg_zero_bits: %08x\n", bv.as_uint);`

Negative zero is a real IEEE 754 value: the sign bit is 1 and everything else
is 0, giving `0x80000000`.  The `%08x` format pads the output to 8 hex
digits, so you see `80000000` with no `0x` prefix.

### Step 5 -- fill in TODO 4

In the TODO 4 block, use `printf("sizeof(ByteView): %zu\n", sizeof(ByteView));`
The `%zu` format is correct for `size_t` (which `sizeof` returns).  The size
should be 4 because the union's size equals its largest member, and all three
members happen to be 4 bytes.

### Step 6 -- build and run

```bash
make
./union_lab
```

Compare your output against the expected lines above.  When they match, type
`exit` and the launcher will check your work and unlock the passphrase.

### Step 7 -- exit the shell

```bash
exit
```

---

## You will know you are done when...

The launcher displays the passphrase after `exit`.  If the output does not
match, it will print what your program produced so you can see exactly where
the difference is.

---

## Hints

<details>
<summary>Hint 1 -- why does %g print 1 instead of 1.000000?</summary>

The `%g` format removes trailing zeros and the decimal point when they are not
needed.  `1.0` has no meaningful decimal part, so `%g` prints `1`.  This is
exactly what the expected output requires.  Using `%f` would print `1.000000`,
which would not match.

</details>

<details>
<summary>Hint 2 -- why does the byte loop print 3f last instead of first?</summary>

Little-endian storage puts the least-significant byte at the lowest address.
The number `0x3F800000` in hex has bytes: most-significant `3F`, then `80`,
then `00`, then `00` least-significant.  In memory, that order reverses:
`bytes[0]` (lowest address) holds `0x00`, and `bytes[3]` holds `0x3F`.
Looping from `i=0` to `i=3` therefore prints `00 00 80 3f`.

</details>

<details>
<summary>Hint 3 -- what is -0.0f and why does it have a bit pattern at all?</summary>

IEEE 754 defines two representations of zero: positive zero (`+0.0f`, all
bits zero) and negative zero (`-0.0f`, sign bit set, all other bits zero).
They compare equal with `==` but have different bit patterns.  Negative zero
appears naturally in some floating-point operations, for example
`-1.0f / (1.0f / 0.0f)` on many platforms.  The bit pattern is `0x80000000`:
the top bit (bit 31) is the sign bit, and it is 1.

</details>

---

## Going further

- Change `bv.as_float = 2.0f` and predict the hex output before running.
  Then verify.  The IEEE 754 encoding for powers of two follows a pattern --
  can you figure out the rule?
- Try a union with `int32_t i` and `uint32_t u`.  Set `i = -1` and read `u`.
  What does that tell you about how negative integers are stored?
- Look up `std::bit_cast<uint32_t>(1.0f)` introduced in C++20.  It does the
  same thing as the union trick but in a way that is explicitly defined by the
  standard.  Does it produce the same result on your machine?
- The byte loop prints bytes in little-endian order.  Write a second loop that
  prints them in big-endian order (most-significant byte first) and verify
  that you get `3f 80 00 00`.
