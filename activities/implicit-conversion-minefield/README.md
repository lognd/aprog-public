# Activity: Implicit Conversion Minefield

C++ will silently convert between types in ways that are legal but
surprising. Assigning -1 to an `unsigned int`. Dividing two `int` literals
and storing the result in a `double`. Comparing a signed value to an
unsigned one.

## Concepts covered

- Unsigned integer wraparound: what happens when -1 is assigned to `unsigned int`
- Truncation when assigning floating-point to integer
- Signed/unsigned comparison: the signed operand converts to unsigned
- Integer division producing an integer result before assignment to `double`
- `bool` arithmetic promotion and what a non-zero integer becomes
- `char` in arithmetic (promotes to its ASCII value, not the character)
- Floating-point representation limits (`float` precision, `0.1 + 0.2 != 0.3`)

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

## How it works

This activity shows you twelve short code snippets. For each one, predict
what the program prints before the compiler runs it. The program compiles
and runs each snippet live so your prediction is checked against the real
output. You must match the actual output exactly to move on.

If you are wrong, you are shown the actual output and asked to type it
exactly -- this forces you to reconcile your mental model with reality
before continuing.

## Getting started

```bash
python3 launch.py
```

Requires `g++` or `clang++` on your machine. The program will tell you if
it cannot find a compiler.

## You will know you are done when...

You have matched the actual output for all twelve snippets and the program
prints the passphrase.

## Going further

- Enable `-Wsign-compare` and `-Wconversion` in your compiler flags. Run them
  against a small project and see how many implicit conversions they flag.
- Look up `static_cast` and rewrite each snippet so that every conversion is
  explicit. Do any of the surprising behaviors disappear?
- Read the C++ standard's "usual arithmetic conversions" section. Write a
  table of which type wins when two different numeric types meet in an expression.
