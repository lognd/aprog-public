# Activity: Struct Layout Bingo

When you declare a struct in C++, you might expect the compiler to pack the
fields together tightly, one byte after the next. It does not. The compiler
inserts invisible "padding" bytes between fields to keep each field starting
at the right address for its type. This activity makes that padding visible.
You will measure exactly where each field lives in memory, see how a pragma
can eliminate padding entirely, and understand the trade-off between size and
access speed.

## Background

### Why alignment exists

A CPU does not read memory one byte at a time. It reads a whole word at once
-- typically 4 or 8 bytes on a modern 64-bit machine. To do this efficiently,
the hardware expects data to start at an address that is a multiple of its
size. A 4-byte `int` should start at an address divisible by 4. An 8-byte
`double` should start at an address divisible by 8.

This is called **natural alignment**. It has nothing to do with cache (you
will study that later). It is about how the CPU's memory bus works at the
hardware level.

When a value is misaligned -- when a 4-byte `int` starts at address 1 instead
of address 4 -- one of two things happens depending on the CPU:

- On x86 (your laptop), the hardware fixes it transparently by issuing two
  memory reads and assembling the pieces. This works but takes extra time.
- On some other architectures (ARM in strict mode, many embedded chips), a
  misaligned access causes a hardware fault and the program crashes.

The safe default is to let the compiler align everything automatically.

### What the compiler inserts

Consider this struct:

```cpp
struct Unpacked {
    char   a;     // 1 byte
    int    b;     // 4 bytes
    char   c;     // 1 byte
    double d;     // 8 bytes
};
```

A naive packing would place them at offsets 0, 1, 5, 6. But then `b` would
start at offset 1, which is not divisible by 4, and `d` would start at offset
6, which is not divisible by 8. Both would be misaligned.

Instead, the compiler inserts padding:

```
offset 0:  char a        (1 byte)
offset 1:  [padding]     (3 bytes)
offset 4:  int b         (4 bytes)
offset 8:  char c        (1 byte)
offset 9:  [padding]     (7 bytes)
offset 16: double d      (8 bytes)
           ----
total:     24 bytes
```

The padding bytes are real memory. They are wasted from a size standpoint, but
they make every field naturally aligned.

The struct's total size (24) is a multiple of the largest alignment requirement
(8, from `double`). This ensures that if you put the struct in an array, the
second element also starts at an 8-byte boundary.

### What `#pragma pack(push, 1)` does

`#pragma pack(push, 1)` tells the compiler to forget about alignment and pack
fields as tightly as possible. The `push` saves the current packing setting
on an internal stack so it can be restored later. The `1` means "use 1-byte
alignment" -- no padding between fields.

With `#pragma pack(push, 1)`, the same struct becomes:

```
offset 0: char a         (1 byte)
offset 1: int b          (4 bytes)  -- NOT aligned to 4, but that is allowed now
offset 5: char c         (1 byte)
offset 6: double d       (8 bytes)  -- NOT aligned to 8
total:    14 bytes
```

Every field is at the very next available byte. The struct is 10 bytes smaller,
but reads to `b` and `d` may take extra CPU cycles on x86 and may fault on
stricter hardware.

### What `#pragma pack(pop)` does

`#pragma pack(pop)` restores the packing setting that was saved by the last
`push`. If you write `#pragma pack(push, 1)` to enable tight packing for one
struct, you must write `#pragma pack(pop)` afterward to restore normal packing
for all the structs that follow.

Forgetting the `pop` is a real bug. Without it, every struct defined after
the `push` -- including ones in other headers you include later -- will be
packed. The resulting structs will be smaller than expected, fields will be at
wrong offsets, and code that reads them will produce garbage. The bug can be
extremely hard to trace because it affects code far from the `#pragma`.

Always use `push` and `pop` together:

```cpp
#pragma pack(push, 1)
struct MyPackedStruct {
    // ...
};
#pragma pack(pop)   // restores the previous setting -- do not forget this
```

### Reordering as an alternative

You can also reduce padding without losing alignment by reordering fields --
largest types first:

```cpp
struct Reordered {
    double d;     // 8 bytes at offset 0
    int    b;     // 4 bytes at offset 8
    char   a;     // 1 byte  at offset 12
    char   c;     // 1 byte  at offset 13
    // 2 bytes trailing padding (total must be multiple of 8)
};
```

This struct is 16 bytes -- smaller than `Unpacked` (24 bytes), but still
naturally aligned. Every field starts at its natural alignment boundary. The
only padding is 2 trailing bytes so that the struct's size is a multiple of
8, keeping arrays of it aligned.

### The trade-off

| Approach | Size | Alignment | When to use |
|---|---|---|---|
| Default (compiler-padded) | Larger | Natural | General-purpose structs |
| `#pragma pack(push, 1)` | Smallest | None | Binary file formats, network packets, hardware registers |
| Reordered fields | Medium | Natural | When you want small size without sacrificing alignment |

Binary file formats like TGA images store their headers in packed structs.
If you read a packed file header into an unpadded C++ struct, the fields land
at the wrong offsets and your image will be garbage. When you work with binary
file formats, you will use `#pragma pack(push, 1)` and need to know exactly
how it works.

## Concepts covered

- Natural alignment: why each type prefers a specific starting address
- Struct padding: invisible bytes the compiler inserts to enforce alignment
- `sizeof` operator applied to structs (always counts padding)
- `offsetof` macro: the byte position of a field within a struct
- `#pragma pack(push, 1)` to disable padding
- `#pragma pack(pop)` to restore the previous packing setting
- Field reordering as a way to reduce padding without disabling alignment

## How it works

The activity drops you into a shell with a single file: `layout_lab.cpp`. The
file contains four struct definitions and a `main` function with five TODO
blocks. Each TODO block asks you to print specific `sizeof` and `offsetof`
values in a fixed format.

Before touching the code, draw each struct on paper as a row of boxes. Label
each box with the field name and its size. Mark where you think the compiler
will insert padding. Then fill in the TODOs, build the program with `make`,
and run it. Compare your paper drawing to the actual output.

The passphrase is unlocked when your program's output exactly matches the
expected values. The launcher compiles and runs your modified `layout_lab.cpp`
automatically after you exit the shell.

## Getting started

```bash
python3 launch.py
```

A shell opens inside a fresh copy of the lab workspace. The banner displays
the steps.

### Step 1 -- read the struct definitions

Open `layout_lab.cpp` with any editor (`nano`, `vim`, `code`). Read all four
struct definitions and the comments explaining `#pragma pack(push, 1)` and
`#pragma pack(pop)`. On paper, draw the memory layout of `Unpacked` and mark
where you expect padding.

### Step 2 -- fill in TODO 1 (sizeof for all four structs)

In `main`, replace the `// TODO 1` comment with four `printf` calls:

```cpp
printf("sizeof(Unpacked) = %zu\n",  sizeof(Unpacked));
printf("sizeof(Packed) = %zu\n",    sizeof(Packed));
printf("sizeof(Reordered) = %zu\n", sizeof(Reordered));
printf("sizeof(Simple) = %zu\n",    sizeof(Simple));
```

### Step 3 -- fill in TODO 2 (offsetof for Unpacked)

```cpp
printf("offsetof(Unpacked, a) = %zu\n", offsetof(Unpacked, a));
printf("offsetof(Unpacked, b) = %zu\n", offsetof(Unpacked, b));
printf("offsetof(Unpacked, c) = %zu\n", offsetof(Unpacked, c));
printf("offsetof(Unpacked, d) = %zu\n", offsetof(Unpacked, d));
```

Do the offsets match your paper drawing? If not, update your drawing and
understand why the compiler inserted padding where it did.

### Step 4 -- fill in TODO 3 (offsetof for Packed)

Same format, same fields, but using `Packed`. Notice how every field is at the
very next available byte -- no gaps.

### Step 5 -- fill in TODO 4 and TODO 5

TODO 4 is `offsetof` for all fields of `Reordered` in the order `d, b, a, c`.
TODO 5 is `sizeof(Simple)` and `offsetof(Simple, z)`.

### Step 6 -- build and run

```bash
make
./layout_lab
```

Compare the output to your paper drawing. When the output matches your
expectations, exit the shell.

```bash
exit
```

The launcher checks your work automatically.

## You will know you are done when...

The launcher prints your passphrase. This happens only when your program's
output matches the expected format exactly -- every line, in order, with the
correct values.

## Hints

<details>
<summary>Hint 1 -- how to call sizeof and offsetof</summary>

`sizeof` is a compile-time operator that takes a type name or an expression.
You do not call it like a function -- you do not write `sizeof(Unpacked)()`.
You write:

```cpp
printf("sizeof(Unpacked) = %zu\n", sizeof(Unpacked));
```

`offsetof` is a macro defined in `<cstddef>`. It takes a struct type and a
field name and returns the byte offset of that field from the start of the
struct:

```cpp
printf("offsetof(Unpacked, b) = %zu\n", offsetof(Unpacked, b));
```

Both `sizeof` and `offsetof` produce values of type `size_t`, so use `%zu`
as the format specifier (not `%d` or `%lu`).

</details>

<details>
<summary>Hint 2 -- platform assumptions</summary>

This activity assumes a 64-bit Linux system where:

- `sizeof(char)` = 1
- `sizeof(int)` = 4
- `sizeof(double)` = 8
- `sizeof(uint8_t)` = 1

These are the values on the machine where you are running the activity. If you
see unexpected results, make sure you are compiling with `g++ -std=c++17` (the
Makefile does this for you) and that you are running on the lab machine, not
cross-compiling.

</details>

<details>
<summary>Hint 3 -- why #pragma pack(pop) is necessary</summary>

`#pragma pack(push, 1)` pushes the current packing setting onto a stack and
switches to 1-byte packing. Without the matching `pop`, the 1-byte packing
stays active for every struct defined after it -- including structs in headers
you include with `#include`. Those structs will be smaller than expected, their
fields will be at wrong offsets, and any code that uses them will read garbage.

The `pop` undoes the `push` by popping the saved setting back off the stack.
Think of it like `{}` braces: you always need a matching close for every open.
In this file, `Packed` is the only struct between the `push` and `pop`, so
`Reordered` and `Simple` are unaffected and get normal padding.

If you want to verify this yourself, try moving `#pragma pack(pop)` to after
`struct Reordered` and observe how `sizeof(Reordered)` changes.

</details>

## Going further

- Move `#pragma pack(pop)` to after `struct Reordered` and recompile. How does
  `sizeof(Reordered)` change? What is the new offset of `Reordered::b`? This
  demonstrates exactly what happens when you forget the `pop`.
- Add a fifth struct where you deliberately reorder the fields of `Unpacked`
  to get the smallest naturally-aligned layout. Verify your prediction with
  `sizeof` and `offsetof`.
- Look up the TGA image file format specification online. Find the TGA header
  definition. How many bytes is it? Do any of its fields require a packed
  struct to read correctly from a file?
- Read about `__attribute__((packed))` in GCC, which is the GCC-specific
  alternative to `#pragma pack(push, 1)`. Why might a codebase use one over
  the other?
