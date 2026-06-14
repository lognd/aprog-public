# Stack & Heap Safari

**Type:** Snippet prediction
**Topic:** Memory model -- stack vs. heap, function call frames, recursion

## Overview

This activity walks you through six short C++ programs that illustrate how
memory is managed at runtime. You will predict the output of each snippet
before running it, then see whether your mental model is correct.

The concepts covered:

- The call stack: each function call creates a new frame with its own locals
- Stack unwinding: what happens after a recursive call returns
- Heap allocation: objects created with `new` outlive the function that created them
- Recursion tracing: following a recursive function call-by-call

## How to run

```
python3 launch.py
```

The program compiles each snippet, shows you the code, and asks for the
output. Type the exact output the snippet would produce (use Enter for
newlines). You will receive the activity passphrase when all answers are
correct.

## Tips

- Trace recursive functions step by step. Draw a call tree if it helps.
- Remember that code AFTER a recursive call runs on the way back out
  (unwinding), not on the way in.
- Stack-allocated locals live only as long as their function is on the stack.
  Heap objects (created with `new`) live until `delete` is called.
- Read error messages carefully. The compiler and runtime are your friends.
