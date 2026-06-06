# Complexity Clock

Four programmers each wrote a function to compute the sum 1 + 2 + ... + n.
Every function returns the correct answer.  But they are not equally fast.

Your job is not to run the code -- it is to *count*.  For each function, trace
through it by hand and determine exactly how many times the marked line
executes when n = 10.

## Getting started

    python3 launch.py

No shell drop, no compiling.  Four functions appear one at a time.  For each,
type the number of times the marked line runs.  Wrong answers are explained
and re-prompted.

## How to count

Pick a small concrete value of n and trace manually:

1. Find the marked line  `// <--`
2. Identify which loop (or loops) contain it
3. For each loop, determine how many times its body runs
4. Multiply nested loop counts together; add them up when loops are sequential

A good strategy: build a table.  For a nested loop, list the outer variable
down one side and count inner iterations across.

## Rules

- Do NOT run the code or use a compiler.
- Trace by hand.  The whole point is the process, not the answer.
- Wrong answers are explained and re-prompted.
- All four must be correct to receive the passphrase.
