# Activity: Recursion Unwind

Recursion -- a function calling itself, either directly or by calling
another function that calls it back -- is not magic: every call has a cost
in time (how many calls happen) and space (how many stack frames, the block
of memory holding one call's local variables and return address, are alive
at once). Every recursive function needs a base case: the condition (such
as `n <= 1` in the code below) that stops the recursion and returns
directly instead of calling itself again. Without one, the calls never
stop and the program crashes when it runs out of stack space. This
activity builds
intuition for both by comparing three implementations of the same function:
naive recursive Fibonacci, memoized recursive Fibonacci (a version that
caches each result the first time it is computed so later calls with the
same input can look it up instead of recomputing it), and iterative
Fibonacci.

## Concepts covered

- Counting recursive calls by tracing a call tree
- Maximum stack depth: how many frames are alive simultaneously at the deepest point
- Exponential call growth in naive recursion vs linear growth with memoization
- How iterative Fibonacci avoids both the call-count explosion and the stack depth problem

## How it works

You are shown code for three implementations of `fib(n)` and asked nine
questions grouped into three sets of three:

- How many times is the function called when computing `fib(5)`?
- What is the maximum number of stack frames alive at once?
- If the input doubles to `fib(10)`, how does the call count change?

Each question asks you to reason from the code, not just recall a fact.
The passphrase is revealed when all nine answers are correct.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

All nine answers are correct and the program prints the passphrase.

## Going further

- Implement memoized Fibonacci using a `std::unordered_map` and verify that
  the call count matches your answer for `fib(5)`.
- Use a debugger (`gdb` or `lldb`) to pause execution inside naive `fib` and
  print the call stack with `bt`. Count the frames at the deepest call.
- Look up tail-call optimization (rewriting a recursive call that is the
  very last action in a function into a plain loop, reusing the same stack
  frame instead of pushing a new one). Can the compiler optimize naive `fib`
  into a loop? Try compiling with `-O2` and inspecting the assembly.
