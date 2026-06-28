# Activity: Const Maze

The `const` keyword in C++ and how its position in a declaration changes its
meaning. You will also distinguish `const` from `constexpr` and understand
why `const` references are the preferred way to pass large objects to
functions.

## Concepts covered

- `const` position relative to `*`: pointer-to-const vs const-pointer vs both
- `const` member functions and what they prevent
- `const` references as the idiomatic way to pass large objects without copying
- `constexpr` vs `const`: compile-time vs runtime immutability

## How it works

Eight questions on `const` pointer declarations, `const` member functions,
`const` references, and `constexpr`. Each question has a hint if you are
unsure where to start. The activity unlocks when all answers are correct.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

All eight questions are correct and the program prints the passphrase.

## Going further

- Look up the "east const" convention (`int const*` instead of `const int*`)
  and read the arguments for and against it. Which style is used in this course?
- Why can a `const` reference bind to a temporary (`const int& r = 5;`) but
  a non-const reference cannot? Find the rule in the C++ standard.
- Write a class with both `const` and non-const overloads of `operator[]` and
  verify that each overload is called in the right context.
