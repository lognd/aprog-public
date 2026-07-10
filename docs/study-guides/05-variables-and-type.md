# Study Guide 5: Variables & Type

This module is about how C++ actually stores and interprets values at the
bit level. It covers bitwise operators and two's-complement arithmetic,
the many silent (implicit) type conversions C++ performs without warning,
and exactly how many bytes each primitive type occupies on different
platforms.

## Know before you start

- A working C++ compiler (`g++` and/or `clang++`) [assumed: row 2 --
  Environment Setup]
- Basic C++ variable declarations and primitive types (`int`, `char`,
  `double`, etc.) [assumed: GAP -- no earlier row formally introduces
  declaring a typed variable; env-setup's `hello.cpp` example is the only
  prior exposure]

## Taught here

Concept: two's complement and bitwise operators
- Know that two's complement is the standard way computers store negative
  integers, with the sign baked directly into the bit pattern.
- Know the two's-complement negation rule: to negate a value x, flip every
  bit then add 1.
- Know the four bitwise operators and what each does per bit: AND (1 only
  if both bits are 1), OR (1 if either bit is 1), XOR (1 if the bits
  differ), NOT (flips every bit of one operand).
- Know that `<<` and `>>` slide every bit left or right by some number of
  positions, filling vacated positions with 0 for a left shift or an
  unsigned right shift.
- Be able to trace a bitwise expression by hand in binary and convert
  between decimal, binary, and hexadecimal.
- Be able to implement arithmetic (like a Collatz-sequence step) using only
  bitwise shifts as a substitute for multiplication/division by powers of
  two, and reason about `unsigned long long` overflow (a value growing past
  the largest representable number and wrapping around) when validating
  input ranges.

Concept: implicit conversions
- Know that an implicit conversion happens automatically, with no error or
  warning, which is what makes it dangerous compared to an explicit cast.
- Know that assigning -1 to an `unsigned int` wraps around to a huge
  positive number, because unsigned types cannot represent negative values.
- Know that assigning a floating-point value to an integer truncates
  (discards the fractional part) rather than rounding.
- Know that in a signed/unsigned comparison, the signed operand is
  converted to unsigned before the comparison happens, which can make a
  negative number appear larger than a positive one.
- Know that integer division (`int / int`) produces an integer result --
  the fractional part is discarded -- even if the result is later assigned
  to a `double`.
- Know that a non-zero integer converts to `bool` as `true`, and that a
  `bool` used in arithmetic promotes to the integer 0 (`false`) or 1
  (`true`).
- Know that a `char` used in arithmetic promotes to its underlying numeric
  ASCII value, not to the character it visually represents.
- Know that `float`/`double` cannot represent every decimal value exactly,
  which is why `0.1 + 0.2 != 0.3` and why a large integer can silently lose
  precision when stored in a `float`.

Concept: sizeof and data models
- Know that `sizeof(char)` is always 1 -- it is the definition of one byte
  in C++.
- Know that a character literal like `'a'` has type `char` in C++ (unlike
  C, where it is `int`), so `sizeof('a') == 1` in C++.
- Know that an unsuffixed floating-point literal (like `3.14`) is always
  type `double`; the `f` suffix forces `float`, and the `LL` suffix on an
  integer literal forces `long long`.
- Know that `signed`/`unsigned` variants of a type are always the same
  size as each other -- only the interpretation of the bits changes.
- Know that `int` is 4 bytes on essentially every common 32-bit and 64-bit
  platform.
- Know the three common data models and what they mean: ILP32 (Int, Long,
  Pointer all 32-bit), LP64 (Long and Pointer 64-bit, `int` stays 32-bit --
  64-bit Linux/macOS), and LLP64 (only `long long` and Pointer are 64-bit
  -- 64-bit Windows).
- Know that `long` is 8 bytes on 64-bit Linux/macOS but only 4 bytes on
  64-bit Windows, and that `long long` is guaranteed at least 8 bytes
  everywhere since C++11.

## Study checklist

- [ ] Trace a short expression using AND/OR/XOR/NOT and shifts by hand in
      binary.
- [ ] Predict the printed output of a snippet that assigns -1 to an
      `unsigned int`.
- [ ] Explain why `0.1 + 0.2 == 0.3` is false in C++.
- [ ] State the size of `long` on 64-bit Linux vs. 64-bit Windows and name
      the data model each uses.
- [ ] Explain why `sizeof('a')` differs between C and C++.

## Practiced in

`bit-manipulation-re`, `implicit-conversion-minefield`, `sizeof-bingo`, `collatz-conjecture`

## Gaps detected

- Basic C++ variable declaration/type syntax is assumed by all four
  artifacts in this module but not formally taught by any earlier row.
  [assumed: GAP]
