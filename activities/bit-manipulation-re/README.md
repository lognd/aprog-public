# Bit Manipulation Reverse Engineering

Five mystery functions.  No running the code.

Each function uses bitwise operators to compute something -- isolating a bit,
counting set bits, swapping bytes, encoding a value.  Your job is to trace
through each one by hand, using binary arithmetic, and predict exactly what it
returns for a given input.

Wrong answers come with a full explanation.  You must get all five correct to
receive the passcode.

## Getting started

    python3 launch.py

The program shows you all five functions up front, then asks one question at a
time.  Type your answer (a whole number, unless told otherwise) and press
Enter.

## Rules

- Do not compile or run the code.
- Trace by hand using binary arithmetic.
- Wrong answers are explained and re-prompted.
- All five must be correct to unlock the passcode.

## You'll know you're done when...

You have answered all five questions correctly and the program prints the
passcode.

## Background

You should be comfortable with:

- Two's-complement negation: to negate x, flip all bits then add 1.
- Bitwise AND, OR, XOR, and NOT.
- Left and right shifts (`<<`, `>>`).
- Converting between decimal, binary, and hex.

If any of those feel shaky, review them before starting -- the questions build
on all of them.
