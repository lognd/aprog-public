# Activity: Stack/Heap Bingo

## What you will practice

Where a variable lives (stack vs. heap vs. static storage) and how long it
lives (block, function, program, or manually managed) are two of the most
important things to understand about C++ memory.  This activity builds
intuition for both by having you classify 25 real C++ variable declarations.

## How it works

You are shown a 5x5 bingo grid.  Each cell contains a short C++ snippet and
names one variable to classify.  You pick a cell, read the code, and choose
the correct category:

1. stack / block-scoped
2. stack / function-scoped
3. static / program-duration
4. heap / manually-managed

When you complete an entire row, column, or diagonal (5 correct cells in a
line), you receive the passphrase.

You do not need to answer every cell -- just find one winning line.

## Requirements

- Python 3.8 or later
- No external libraries required

## Running the activity

```
python3 launch.py
```

---

## Going Deeper: Memory Segments (optional)

This activity focuses on the four categories above.  If you are curious about
how this maps to the actual layout of a running process, here is a brief
overview.  This is background knowledge -- it is not needed to complete the
activity or answer any questions.

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

**Stack** -- function call frames live here.  Each call pushes a frame; each
return pops one.  Local variables and parameters live in the current frame.
Block-scoped variables are within a frame but released when the block ends.

**Heap** -- dynamic allocation (new/delete, malloc/free) comes from here.  The
heap can grow as long as the OS allows.  The programmer controls the lifetime
explicitly.

**BSS segment** -- global and static variables that are not explicitly
initialized go here.  The OS zero-initializes them before main() runs.

**Data segment** -- global and static variables that are explicitly initialized
with a non-zero value go here.  Initialized before main() runs.

**Text segment** -- the compiled machine code.  Read-only on most platforms.

The "static / program-duration" category in this activity covers both BSS and
Data segments.  The exact segment depends on whether the variable has an
initializer and what value it has, but the lifetime is the same: the entire
program run.
