# Activity: sizeof Bingo

How large is an `int`? What about a `long` on 64-bit Windows versus 64-bit
Linux? Does `sizeof(T&)` give you the size of a pointer or the size of `T`?

This activity walks you through sixteen `sizeof` expressions across
different types, architectures, and data models. For each one, predict the
result before you see the answer. Wrong guesses are explained and
re-prompted -- you must get every answer correct to receive the passphrase.

## Background

You do not need to memorize a table. Think through each question using
these rules:

- `sizeof(char)` is always 1 -- it is the definition of "one byte" in C++.
- `sizeof(T&)` equals `sizeof(T)` -- references have no overhead in sizeof.
- Pointer width equals the address-bus width of the target platform.
- `int` is 4 bytes on every common 32-bit and 64-bit platform (ILP32, LP64, LLP64).
- `long` is 8 bytes on 64-bit Linux/macOS (LP64) but 4 bytes on 64-bit Windows (LLP64).
- `long long` is guaranteed to be at least 8 bytes everywhere since C++11.
- Struct members are padded so each member is aligned to a multiple of its own size.

## Concepts covered

- `sizeof(char)` is always 1 by definition -- all other sizes are multiples of this
- `sizeof(T&)` equals `sizeof(T)` -- references carry no overhead in sizeof
- How data models (ILP32, LP64, LLP64) determine the width of `long` and pointers
- Struct alignment padding: each member aligns to a multiple of its own size

## How it works

The program asks you one question at a time. Type a whole number and press
Enter. If you are wrong, you will see an explanation and get another chance.
All sixteen must be correct to unlock the passphrase.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

All sixteen questions are correct and the program prints the passphrase.

## Going further

- Write a struct with three members and predict its `sizeof` before compiling.
  Then add `__attribute__((packed))` and see how the size changes.
- Look up `alignof` and `alignas`. How do they relate to the padding rules?
- Find the size of `std::string` on your platform with `sizeof(std::string)`.
  The result is surprising -- read why in the libc++ or libstdc++ source.
