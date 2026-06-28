# Activity: Pass-Mode Minefield

The three ways to pass a value to a function in C++: by value (a copy), by
reference (an alias), and by pointer (an address). Getting these wrong is
one of the most common sources of bugs in new C++ code.

## Concepts covered

- Pass by value: the caller's variable is unchanged because the function receives a copy
- Pass by reference: the function receives an alias -- modifications affect the caller's variable
- Pass by pointer: the function receives an address -- must dereference to read or modify
- When each mode is appropriate and the bugs that arise from choosing the wrong one

## How it works

You are shown six short C++ programs. Predict what each one prints before
running it. The activity locks until all six predictions are correct.

You do not need to compile the programs -- read them carefully and reason
about what happens to the variables as they pass through each function.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

All six predictions are correct and the program prints the passphrase.

## Going further

- Write a function that takes a large struct by value and the same function
  taking `const T&`. Compile both with `-O0` and compare the assembly. How
  many bytes are copied in each case?
- When does passing by pointer make more sense than passing by reference?
  Find a real example in a standard library function signature.
- Look up move semantics (`T&&`). How does pass-by-move relate to the three
  modes covered here, and when would you use it?
