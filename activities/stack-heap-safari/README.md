# Activity: Stack & Heap Safari

Six short C++ programs that illustrate how memory is managed at runtime.
You will predict the output of each snippet before running it, then see
whether your mental model is correct.

## Concepts covered

- The call stack: each function call creates a new frame with its own local variables
- Stack unwinding: code after a recursive call runs on the way back out, not the way in
- Heap allocation: objects created with `new` outlive the function that created them
- Recursion tracing: following a recursive function call-by-call through its full execution

## How it works

The program compiles each snippet, shows you the code, and asks for the
output. Type the exact output the snippet would produce (use Enter for
newlines). You will receive the activity passphrase when all answers are
correct.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

All answers are correct and the program prints the passphrase.

## Hints

<details>
<summary>Hint 1 -- tracing recursive functions</summary>

Trace recursive functions step by step. Draw a call tree if it helps.
Code AFTER a recursive call runs on the way back out (unwinding), not on
the way in.

</details>

<details>
<summary>Hint 2 -- variable lifetimes</summary>

Stack-allocated locals live only as long as their function is on the stack.
Heap objects (created with `new`) live until `delete` is called.

</details>

## Going further

- Take one of the recursive snippets and add a print statement both before
  and after the recursive call. Verify that the "after" print runs on the
  way back up the call stack.
- Write a function that returns a pointer to a local variable and run it
  under ASan. Read the report and find the exact line flagged.
- Look up what "stack unwinding" means in the context of C++ exceptions
  (`throw`/`catch`) and how destructors are called during unwinding.
