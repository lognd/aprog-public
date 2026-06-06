# sizeof Bingo

How large is an `int`?  What about a `long` on 64-bit Windows versus 64-bit
Linux?  Does `sizeof(T&)` give you the size of a pointer or the size of `T`?

This activity walks you through sixteen `sizeof` expressions across different
types, architectures, and data models.  For each one, predict the result
before you see the answer.  Wrong guesses are explained and re-prompted --
you must get every answer correct to receive the passcode.

## Getting started

    python3 launch.py

The program asks you one question at a time.  Type a whole number and press
Enter.  If you are wrong, you will see an explanation and get another chance.
All sixteen must be correct to unlock the passcode.

## You'll know you're done when...

You have answered all sixteen questions correctly and the program prints the
passcode.

## Background reading

You do not need to memorize a table.  Think through each question using these
rules:

- `sizeof(char)` is always 1 -- it is the definition of "one byte" in C++.
- `sizeof(T&)` equals `sizeof(T)` -- references have no overhead in sizeof.
- Pointer width equals the address-bus width of the target platform.
- `int` is 4 bytes on every common 32-bit and 64-bit platform (ILP32, LP64, LLP64).
- `long` is 8 bytes on 64-bit Linux/macOS (LP64) but 4 bytes on 64-bit Windows (LLP64).
- `long long` is guaranteed to be at least 8 bytes everywhere since C++11.
- Struct members are padded so each member is aligned to a multiple of its own size.
