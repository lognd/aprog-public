# Activity: C-String vs std::string

Six side-by-side comparisons between C-style strings (`const char*`,
`char[]`) and `std::string`. Each snippet shows both approaches doing the
same operation so you can see exactly where they differ -- and why
`std::string` was invented.

Topics covered: length, concatenation, equality comparison, in-place
mutation, bounds checking, and the `c_str()` bridge back to C functions.

## Concepts covered

- Length: `strlen` vs `.size()` and why C strings have no stored length
- Concatenation: manual buffer management (tracking a fixed block of
  memory yourself) vs `operator+`
- Equality: pointer comparison vs `strcmp` vs `operator==` --
  `std::string`'s content-based `==` exists because its author wrote a
  function named `operator==` for it; that technique, operator
  overloading, is its own topic taught in a later module
- In-place mutation: legal for `char[]`, undefined behavior for string
  literals (the C++ standard places no limit on what happens if you try)
- The `c_str()` bridge: getting a `const char*` out of a `std::string`

## How it works

Read each short program and predict what it prints. Correct predictions
unlock an explanation of the key difference between the two string
representations. All six correct answers together unlock the passphrase.

The launcher compiles and runs each snippet itself (with g++ or clang++)
to check your prediction against the real output -- you do not need to
compile anything yourself, but a C++ compiler must be installed.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

All six answers are correct and the program prints the passphrase.

## Going further

- Write a function that accepts a `const char*` and returns a `std::string`,
  and another that goes the other direction. What lifetime issues arise?
- Look up `std::string_view` (C++17): when does it outperform both `const char*`
  and `const std::string&`?
- Benchmark `std::string` concatenation in a loop vs building with `std::ostringstream`.
  At what size does the difference become measurable?
