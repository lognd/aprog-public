# Recursion Unwind

## What you will practice

Recursion is not magic -- every call has a cost in time (how many calls happen)
and space (how many frames are alive at once).  This activity builds intuition
for both by comparing three implementations of the same function: naive
recursive Fibonacci, memoized recursive Fibonacci, and iterative Fibonacci.

## How it works

You are shown code for three implementations of fib(n) and asked nine
questions grouped into three sets of three:

- How many times is the function called when computing fib(5)?
- What is the maximum number of stack frames alive at once?
- If the input doubles to fib(10), how does the call count change?

Each question asks you to reason from the code, not just recall a fact.  The
passphrase is revealed when all nine answers are correct.

## Requirements

- Python 3.8 or later
- No external libraries required

## Running the activity

```
python3 launch.py
```
