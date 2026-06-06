# Implicit Conversion Minefield

C++ will silently convert between types in ways that are legal but surprising.
Assigning -1 to an `unsigned int`.  Dividing two `int` literals and storing
the result in a `double`.  Comparing a signed value to an unsigned one.

This activity shows you twelve short code snippets.  For each one, predict
what the program prints before the compiler runs it.  The program compiles and
runs each snippet live so your prediction is checked against the real output.
You must match the actual output exactly to move on.

## Getting started

    python3 launch.py

Requires `g++` or `clang++` on your machine.  The program will tell you if it
cannot find a compiler.

For each snippet, read the code carefully, type your prediction, and press
Enter.  If you are wrong, you are shown the actual output and asked to type it
exactly -- this forces you to reconcile your mental model with reality before
continuing.

## You'll know you're done when...

You have matched the actual output for all twelve snippets and the program
prints the passcode.

## Background

The snippets cover:

- Truncation when assigning floating-point to integer
- Unsigned wraparound (`-1` assigned to `unsigned int`)
- Signed/unsigned comparison (the signed value converts to unsigned)
- Integer division before floating-point assignment
- `bool` from a non-zero integer
- `bool` arithmetic promotion
- `char` in arithmetic expressions (ASCII value, not the character)
- Unsigned subtraction wraparound
- `float` precision loss on a large integer
- Floating-point equality (`0.1 + 0.2 == 0.3`)
- Integer division before floating-point addition
- Arithmetic right shift of a negative signed integer
