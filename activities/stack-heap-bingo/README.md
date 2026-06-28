# Activity: Stack/Heap Bingo

Where a variable lives (stack vs. heap vs. static storage) and how long it
lives (block, function, program, or manually managed) are two of the most
important things to understand about C++ memory. This activity builds
intuition for both by having you classify 25 real C++ variable declarations.

## Background

A typical process memory layout (low address at bottom):

```
  High address  +----------------------------+
                |  Stack                     |  grows downward
                |  (local vars, call frames) |
                +----------------------------+
                |  (unmapped gap)            |
                +----------------------------+
                |  Heap                      |  grows upward
                |  (new / malloc)            |
                +----------------------------+
                |  BSS segment               |  zero-initialized globals
                |  (uninit. static storage)  |
                +----------------------------+
                |  Data segment              |  initialized globals
                |  (init. static storage)    |
                +----------------------------+
                |  Text / Code segment       |  executable instructions
  Low address   +----------------------------+
```

**Stack** -- function call frames live here. Each call pushes a frame; each
return pops one. Local variables and parameters live in the current frame.
Block-scoped variables are within a frame but released when the block ends.

**Heap** -- dynamic allocation (`new`/`delete`, `malloc`/`free`) comes from
here. The heap can grow as long as the OS allows. The programmer controls
the lifetime explicitly.

**BSS segment** -- global and static variables that are not explicitly
initialized go here. The OS zero-initializes them before `main()` runs.

**Data segment** -- global and static variables that are explicitly
initialized with a non-zero value go here. Initialized before `main()` runs.

**Text segment** -- the compiled machine code. Read-only on most platforms.

The "static / program-duration" category in this activity covers both BSS
and Data segments. The exact segment depends on whether the variable has an
initializer and what value it has, but the lifetime is the same: the entire
program run.

## Concepts covered

- Stack allocation: local variables live in the current call frame
- Block scope vs. function scope for stack variables
- Heap allocation: `new` / `delete` give manual lifetime control
- Static storage duration: globals and `static` locals live for the entire program
- The four categories and how to classify any declaration by reading its syntax

## How it works

You are shown a 5x5 bingo grid. Each cell contains a short C++ snippet and
names one variable to classify. You pick a cell, read the code, and choose
the correct category:

1. stack / block-scoped
2. stack / function-scoped
3. static / program-duration
4. heap / manually-managed

When you complete an entire row, column, or diagonal (5 correct cells in a
line), you receive the passphrase. You do not need to answer every cell --
just find one winning line.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You complete a full row, column, or diagonal and the program prints the
passphrase.

## Going further

- Look up `alloca`. It allocates on the stack at runtime -- why is it
  dangerous and why does the C++ standard not include it?
- Write a program that allocates a very large array on the stack and run it.
  What error do you get? Look up `ulimit -s` to see your stack size limit.
- Look up `thread_local` storage duration. How does it differ from `static`
  in a multi-threaded program?
