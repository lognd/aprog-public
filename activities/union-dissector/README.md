# Activity: Union Dissector

Every variable you write in C++ has a type, and that type tells the compiler
how to interpret the bits stored at that variable's address.  An `int` and a
`float` can occupy the same number of bytes, but the bits mean completely
different things depending on which type you use to look at them.  Normally
the compiler enforces this separation strictly -- you cannot just tell it "I
know these bytes are really a float, please read them that way."

A `union` declares a block of memory that can be accessed through any of its
named members.  All members share the same starting address and the same bytes.
This activity explores what that means concretely, when it is useful, and where
C and C++ draw very different lines.

---

## Background

### Use case 1 -- saving space among mutually exclusive fields

Sometimes a data structure holds fields where only one can be meaningful at a
time.  Consider a simplified network packet:

```cpp
struct Packet {
    uint8_t protocol;   // 6 = TCP, 17 = UDP
    union {
        struct { uint32_t seq; uint32_t ack; } tcp;
        struct { uint16_t length;            } udp;
    } payload;
};
```

A packet is either TCP or UDP -- never both.  Storing both structs separately
would waste memory on whichever one is not active.  The union makes them share
the same bytes, so the packet is as small as possible.

The programmer is responsible for tracking which member is active.  In the
example above, `protocol` serves as the tag.  If you write `payload.tcp` and
then read `payload.udp`, the bytes you get are whatever `tcp` left behind --
which is almost certainly wrong.  The union does not stop you; it just shares
the memory.

---

### Use case 2 -- type punning (inspecting the raw bytes of a value)

Type punning means reading the raw bytes of one type as if they were a
different type.  The classic reason to do this is to inspect the bit pattern
of a `float` -- something the compiler normally hides from you entirely.

```cpp
union ByteView {
    uint32_t      as_uint;
    float         as_float;
    unsigned char bytes[4];
};

ByteView bv;
bv.as_float = 1.0f;
printf("%08x\n", bv.as_uint);  // prints 3f800000 -- the IEEE 754 bits of 1.0f
```

This is exactly what the activity asks you to do.  Before you write that code,
read this warning:

```
WARNING -- C vs C++
-------------------
In C (C11 section 6.5.2.3, footnote 95), reading a union member
you did not write is explicitly defined behavior.  C was designed
for systems programming where inspecting raw bytes is routine, and
the standard grants unions this special permission.

In C++, the same pattern is undefined behavior.  The C++ standard's
"strict aliasing rule" says the compiler may assume that two
pointers of different types never point to the same memory.  The
optimizer uses this assumption to eliminate or reorder reads --
which means reading through the wrong union member can silently
produce the wrong value, or no value at all, even if the bytes are
physically there.

GCC and Clang both support union type-punning as a documented
extension and will not miscompile it at -O2.  But the standard
does not require them to, and other compilers may not.

The safe alternatives in C++ are:

  std::memcpy(&result, &source, sizeof(result))   // C++11+
  std::bit_cast<TargetType>(source)               // C++20+

For memcpy, modern compilers recognize this pattern and optimize it
to a single register move -- no actual memory copy occurs.
```

The `memcpy` approach:

```cpp
float f = 1.0f;
uint32_t bits;
std::memcpy(&bits, &f, sizeof(bits));  // defined behavior in C++
printf("%08x\n", bits);               // prints 3f800000
```

The `bit_cast` approach (C++20):

```cpp
#include <bit>
uint32_t bits = std::bit_cast<uint32_t>(1.0f);  // clean, defined, C++20
printf("%08x\n", bits);
```

This activity uses the union approach because it makes the shared-memory model
**visible** -- you can see all three member names pointing at the same four
bytes.  That is its pedagogical value.  In production C++ code, use `memcpy`
or `bit_cast`.

---

### Use case 3 -- discriminated unions (the main C++ use case)

The primary legitimate use of a raw union in C++ is to build a **discriminated
union**, also called a **tagged union**.  The idea: pair a union with an enum
that records which member is currently active.  As long as you only ever read
the member that was last written, the behavior is well-defined in both C and
C++.

```cpp
enum class Kind { Int, Float, Bool };

struct Value {
    Kind kind;
    union {
        int   as_int;
        float as_float;
        bool  as_bool;
    };
};

Value v;
v.kind     = Kind::Float;
v.as_float = 3.14f;

// Later, to read safely:
if (v.kind == Kind::Float) {
    printf("%f\n", v.as_float);  // only read what we wrote -- defined
}
```

This pattern appears everywhere: interpreters store numbers and strings in the
same slot, compilers represent AST node values, configuration systems store
settings of mixed type.  The enum tag is what makes it safe -- without it, a
union is just a shared block of bytes with no memory of what was written.

---

### What is a sum type?

At this point it is worth stepping back and naming what you are looking at,
because it is a fundamental idea that appears in almost every programming
language.

Types can be combined in two basic ways.

A **product type** holds ALL of its parts simultaneously.  A `struct` with
fields `int x` and `float y` always holds both an `int` AND a `float` at the
same time.  The name comes from counting: if `int` has N possible values and
`float` has M, then the struct has N times M possible states.  Every struct and
class you have written so far is a product type.

A **sum type** holds EXACTLY ONE of its variants at a time.  A type that is
either an `int` OR a `float` OR a `bool` -- never more than one -- has N plus M
plus 2 possible states (the sum of the variant sizes).  The discriminated union
above is a sum type: at any given moment, a `Value` is one thing, not all three.

Raw unions in C++ are an unsafe, low-level version of a sum type.  They share
the memory correctly, but nothing in the language stops you from forgetting the
tag, reading the wrong member, and getting garbage.  That responsibility falls
entirely on you.

C++17 introduced `std::variant` as the safe, type-checked version:

```cpp
#include <variant>
#include <iostream>

std::variant<int, float, bool> v = 3.14f;

// std::get<int>(v);        // throws std::bad_variant_access -- v holds a float
std::cout << std::get<float>(v) << "\n";  // ok: prints 3.14

// Check before reading:
if (std::holds_alternative<float>(v)) {
    printf("it's a float: %f\n", std::get<float>(v));
}
```

`std::variant` carries the tag automatically and throws an exception if you
try to read the wrong variant.  Prefer it over raw unions in new C++ code.

Sum types appear across almost every modern language under different names.
In Rust, `Option<T>` (either a value or nothing) and `Result<T, E>` (either a
success or an error) are sum types enforced by the compiler.  In Haskell they
are called `Maybe` and `Either`.  In Swift, `enum` cases with associated values
are sum types, and `Optional` is one too.  Once you understand the idea at the
level of "one of these, not all of these," all of those constructs become
immediately recognizable.

An enum itself is actually a degenerate sum type where every variant carries no
data -- just a label.  A discriminated union adds data to each variant.
`std::variant` makes the whole thing safe and automatic.  The underlying idea
is the same all the way through.

---

## Concepts covered

- `union` memory layout -- all members occupy the same bytes simultaneously
- `sizeof(union)` equals the size of its largest member, not the sum
- Type punning through a union is **defined behavior in C** (C11 6.5.2.3)
  but **undefined behavior in C++** due to the strict aliasing rule
- The safe C++ alternatives: `std::memcpy` (C++11) and `std::bit_cast` (C++20)
- Discriminated (tagged) unions -- the primary safe C++ use case for raw unions
- Product types vs sum types, and `std::variant` as the modern C++ sum type
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
- Try the `std::memcpy` equivalent: `uint32_t bits; float f = 1.0f; std::memcpy(&bits, &f, sizeof(bits));`.
  Print `bits` in hex.  Do you get `3f800000`?  This is defined behavior in
  C++ unlike the union approach.  Check the assembly with `g++ -O2 -S` -- does
  the compiler actually emit a copy instruction, or does it optimize it away?
- In C++20, `std::bit_cast<uint32_t>(1.0f)` does the same thing as `memcpy`
  but as a single expression and is explicitly defined by the standard.  Try
  it with `-std=c++20` and confirm the result matches the union version.
- Write the discriminated union `Value` example from the Background section.
  Then write the same thing using `std::variant<int, float, bool>` and compare
  how much less code the variant version requires.
- The byte loop prints bytes in little-endian order.  Write a second loop that
  prints them in big-endian order (most-significant byte first) and verify
  that you get `3f 80 00 00`.
