# Activity: C-String Predictor

C-style strings -- null-terminated character arrays -- and the functions
from `<cstring>` that operate on them. Unlike `std::string`, a C string has
no built-in length tracking; everything is defined by the `'\0'` terminator.

## Concepts covered

- Null-terminated character arrays and the `'\0'` sentinel
- `strlen`: counts characters before the null terminator, not including it
- `strcpy` and `strcat`: how they walk the destination pointer to append
- Pointer decay: how a `char[]` becomes a `const char*` when passed to a function

## How it works

You are shown six C++ programs that use char arrays, pointers, `strlen`,
`strcpy`, and `strcat`. Predict the output of each program. The activity
unlocks when all six answers are correct.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

All six answers are correct and the program prints the passphrase.

## Going further

- Implement `strcat` from scratch: walk to the end of `dst`, then copy `src`
  character by character. How does the final null terminator get placed?
- What does `strlen` return for an empty string (`""`)? Verify your answer
  by tracing the loop.
- Write a program that deliberately overflows a `char[8]` buffer and run it
  under ASan (`-fsanitize=address`) to see what the report looks like.
