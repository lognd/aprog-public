# Activity: Implicit Conversion Minefield

C++ will silently convert between types in ways that are legal but
surprising -- it does this automatically, with no error or warning, which is
what makes an "implicit" conversion dangerous. Assigning -1 to an
`unsigned int` (a type that can only represent zero and positive numbers).
Dividing two `int` literals and storing the result in a `double`. Comparing
a signed value (can be negative) to an unsigned one (cannot).

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
- `float` precision loss on a large integer (a `float` cannot store every
  large whole number exactly, so it silently rounds to the nearest value it
  can represent)
- Floating-point equality (`0.1 + 0.2 == 0.3`)
- Integer division before floating-point addition
- Arithmetic right shift of a negative signed integer (shifting a negative
  number's bits right while preserving its sign)

## Concepts covered

- Unsigned integer wraparound: what happens when -1 is assigned to
  `unsigned int` -- since it cannot represent negative numbers, the value
  wraps around to a huge positive number instead
- Truncation (the fractional part is silently cut off, not rounded) when
  assigning floating-point to integer
- Signed/unsigned comparison: the signed operand converts to unsigned before
  the comparison happens, which can make a negative number appear larger
  than a positive one
- Integer division producing an integer result (the fractional part is
  discarded) before assignment to `double`
- `bool` arithmetic promotion: when a `bool` is used in arithmetic, it is
  converted to the integer 0 (`false`) or 1 (`true`) first, and what a
  non-zero integer becomes when converted the other way, into `bool`
- `char` in arithmetic (promotes to its underlying numeric ASCII value --
  the number that represents the character -- not the character itself)
- Floating-point representation limits: `float`/`double` cannot store every
  decimal value exactly, so results like `0.1 + 0.2 != 0.3` can occur

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
