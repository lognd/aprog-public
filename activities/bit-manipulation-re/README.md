# Activity: Bit Manipulation Reverse Engineering

Five mystery functions. No running the code.

Each function uses bitwise operators to compute something -- isolating a bit,
counting set bits, swapping bytes, encoding a value. Your job is to trace
through each one by hand, using binary arithmetic, and predict exactly what
it returns for a given input.

Wrong answers come with a full explanation. You must get all five correct to
receive the passphrase.

## Background

You should be comfortable with:

- Two's-complement negation: to negate x, flip all bits then add 1.
- Bitwise AND, OR, XOR, and NOT.
- Left and right shifts (`<<`, `>>`).
- Converting between decimal, binary, and hex.

If any of those feel shaky, review them before starting -- the questions
build on all of them.

## Concepts covered

- Two's-complement representation and negation (flip all bits, add 1)
- Bitwise AND, OR, XOR, and NOT operators
- Left and right shift operators (`<<`, `>>`) and what they do to bits
- Tracing bitwise expressions by hand in binary
- Converting between decimal, binary, and hexadecimal

## How it works

The program shows you all five functions up front, then asks one question at
a time. Type your answer (a whole number, unless told otherwise) and press
Enter. Do not compile or run the code -- trace by hand using binary
arithmetic. Wrong answers are explained and re-prompted.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

All five questions are correct and the program prints the passphrase.

## Going further

- Write a function that counts the number of set bits in a 32-bit integer
  using only bitwise operators and no standard library functions.
- Look up what `-fsanitize=undefined` catches for shift operations on
  negative signed integers -- try it on a left-shift of a negative value.
- Write a bit-reversal function (reverse the order of all 32 bits) and
  verify it against the standard library's `__builtin_bitreverse32`.
