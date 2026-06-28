# Activity: Call Stack Autopsy

## What you will practice

When a C++ program crashes, the operating system (or a tool like
AddressSanitizer) prints a stack trace showing every function that was active
at the moment of the crash.  Reading a stack trace is a fundamental debugging
skill.  This activity teaches you to read one, identify the bug that caused the
crash, and reason about how to fix it.

## How it works

You are shown:

1. A real stack-overflow crash report produced by AddressSanitizer, truncated
   to the first 8 frames.
2. The source code of the two functions that appear in the trace.

You answer four questions:

- What kind of bug does the trace indicate?
- Where exactly is the bug, and what should the code do instead?
- Why did the program survive thousands of calls before crashing?
- What does the fixed program print?

All answers must be correct to receive the passphrase.

## Requirements

- Python 3.8 or later
- No external libraries required

## Running the activity

```
python3 launch.py
```

The source file `crash_demo.cpp` is included if you want to compile and run
it yourself (requires g++ with -fsanitize=address):

```bash
g++ -std=c++17 -g -fsanitize=address -o crash_demo crash_demo.cpp
./crash_demo
```
