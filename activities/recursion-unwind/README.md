# Recursion Unwind

**Type:** Shell drop (debug a broken program)
**Topic:** Recursion -- base cases, recursive steps, call stack

## Overview

You are handed a C++ program with two broken recursive functions. Your job is
to find and fix both bugs so the program produces the correct output.

The program contains:

- `digit_sum(int n)` -- should return the sum of digits of n, e.g. 493 -> 16
- `reverse_str(string, int i, int j)` -- should reverse the string between
  indices i and j, e.g. "hello" -> "olleh"

Both functions are implemented recursively but have bugs. When fixed, the
program should print:

```
16
olleh
```

## How to run

```
python3 launch.py
```

The launcher copies the broken program into a temporary directory and drops
you into a shell. Edit `main.cpp`, then use `make run` to build and run.
When the output matches, type `exit` to validate and receive the passphrase.

## What to fix

**Bug 1 (digit_sum):** The function is missing its base case. Without a base
case, the recursion never stops and the program crashes (stack overflow).
Think: what is the simplest input where you can return the answer directly
without a recursive call?

**Bug 2 (reverse_str):** The swap statement has an off-by-one error. The
function is supposed to swap characters at positions i and j, but it is
swapping the wrong characters. Read the swap line carefully.

## Build commands

```bash
make        # compile main.cpp -> ./prog
make run    # compile and run
make clean  # remove the binary
```

## Tips

- A recursive function needs a base case (stops recursion) and a recursive
  step (reduces the problem toward the base case).
- If your program hangs or crashes immediately, the base case is still missing
  or unreachable.
- Use small test values to trace the logic manually before running.
