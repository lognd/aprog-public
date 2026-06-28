# Activity: Call Stack Autopsy

When a C++ program crashes, the operating system (or a tool like
AddressSanitizer) prints a stack trace showing every function that was
active at the moment of the crash. Reading a stack trace is a fundamental
debugging skill. This activity teaches you to read one, identify the bug
that caused the crash, and reason about how to fix it.

## Concepts covered

- Stack trace format: frame numbering, addresses, function names, source lines
- Recognizing infinite recursion from an AddressSanitizer stack-overflow report
- Why a program survives many recursive calls before crashing (stack depth limit)
- The relationship between a missing base case and unbounded recursion

## How it works

You are shown:

1. A real stack-overflow crash report produced by AddressSanitizer,
   truncated to the first 8 frames.
2. The source code of the two functions that appear in the trace.

You answer four questions:

- What kind of bug does the trace indicate?
- Where exactly is the bug, and what should the code do instead?
- Why did the program survive thousands of calls before crashing?
- What does the fixed program print?

All answers must be correct to receive the passphrase.

## Getting started

```bash
python3 launch.py
```

The source file `crash_demo.cpp` is included if you want to compile and run
it yourself (requires g++ with `-fsanitize=address`):

```bash
g++ -std=c++17 -g -fsanitize=address -o crash_demo crash_demo.cpp
./crash_demo
```

## You will know you are done when...

All four questions are correct and the program prints the passphrase.

## Going further

- Compile `crash_demo.cpp` and run it under Valgrind instead of ASan. How
  does Valgrind's output differ from ASan's for a stack overflow?
- Introduce a heap-use-after-free bug in `crash_demo.cpp` and read what
  ASan reports. Compare the report format to the stack-overflow one.
- Look up what `-g` does to a compiled binary and why the line numbers in
  stack traces disappear without it.
