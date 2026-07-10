# Activity: sizeof Bingo

How large is an `int`? What about a `long` on 64-bit Windows versus 64-bit
Linux? Does `'a'` take up the same space in C++ as it does in C?

This activity walks you through sixteen `sizeof` expressions across
different primitive types, literal suffixes, and data models. For each
one, predict the result before you see the answer. Wrong guesses are
explained and re-prompted -- you must get every answer correct to receive
the passphrase.

## Background

You do not need to memorize a table. Think through each question using
these rules:

- `sizeof(char)` is always 1 -- it is the definition of "one byte" in C++.
- A character literal like `'a'` has type `char` in C++ (unlike C, where it
  is `int`), so `sizeof('a') == 1` in C++.
- An unsuffixed floating-point literal like `3.14` is always type `double`;
  the `f` suffix (`2.0f`) forces it to `float` instead.
- Integer literal suffixes select a wider type: `LL` forces `long long`.
- `signed`/`unsigned` variants of a type are always the same size as each
  other -- only the interpretation of the bits changes, never the width.
- `int` is 4 bytes on every common 32-bit and 64-bit platform. These
  platforms are grouped into "data models" -- naming conventions for how
  many bytes the basic types use: ILP32 (Int, Long, Pointer all 32-bit),
  LP64 (Long, Pointer 64-bit, but `int` stays 32-bit), and LLP64 (only
  `long long` and Pointer are 64-bit).
- `long` is 8 bytes on 64-bit Linux/macOS (LP64) but 4 bytes on 64-bit Windows (LLP64).
- `long long` is guaranteed to be at least 8 bytes everywhere since C++11.

## Concepts covered

- `sizeof(char)` is always 1 by definition -- all other sizes are multiples of this
- The C vs. C++ difference in the type of a character literal (`'a'`)
- Default types of floating-point literals, and how suffixes (`f`, `LL`) change them
- `signed`/`unsigned` variants of a type share the same size
- How data models (ILP32, LP64, LLP64) determine the width of `int` and `long`

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

- Write a struct (a user-defined type that groups several variables together
  under one name) with three members and predict its `sizeof` before
  compiling. Then add `__attribute__((packed))` and see how the size changes.
- Look up `alignof` and `alignas`. How do they relate to the padding rules?
- Find the size of `std::string` on your platform with `sizeof(std::string)`.
  The result is surprising -- read why in the libc++ or libstdc++ source.
