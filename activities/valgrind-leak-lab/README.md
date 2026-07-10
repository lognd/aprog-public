# Activity: Valgrind Leak Lab

**valgrind** is a tool that runs your compiled program inside a simulator
and watches every single memory access it makes. Unlike AddressSanitizer
(covered in the ASan Autopsy activity), you do not need to recompile your
program with a special flag -- you just run `valgrind ./your_program`
and it does the watching from the outside. One of its most useful modes,
`--leak-check=full`, tracks every block of HEAP memory (memory obtained
with `new` or `new[]`, which must be released by hand with a matching
`delete` or `delete[]`) and reports, when the program exits, exactly which
blocks were never freed.

You are given a small inventory-list program with THREE separate memory
leaks hidden in it. Your job is to find and fix all three using valgrind's
own output as your guide.

## Concepts covered

- Reading a valgrind `LEAK SUMMARY` and individual leak records
- The specific meaning of "definitely lost": memory that valgrind can
  prove is unreachable -- no pointer anywhere in the program still points
  at it -- when the program exits
- Reading a leak record's call stack to find the exact function and line
  that allocated the lost memory
- `new` / `delete` and `new[]` / `delete[]` pairing -- and the bug of
  pairing the wrong one, or forgetting one entirely
- Early-return leak paths: a function that allocates memory and then
  returns before reaching the code that would have freed it

## How it works

`inventory.cpp` builds a small singly-linked list of `Item` records, each
holding a heap-allocated name string. The program compiles and runs
without crashing and produces perfectly reasonable-looking output -- but
three separate code paths leak memory:

1. Renaming an item allocates a new name string but never frees the old
   one first.
2. The function that frees the whole list frees each node but forgets to
   free that node's name string first.
3. A validation function allocates an item, then, on an early-return path
   for invalid input, returns without freeing the item it just allocated.

You will use valgrind to find each one, fix it in the source, and rebuild.
When you exit the shell, the launcher rebuilds your code itself and reruns
valgrind on the result -- it does not trust anything you typed, only what
your program and valgrind actually report.

## Getting started

```bash
python3 launch.py
```

A shell opens inside a fresh copy of the workspace.

### Step 1 -- build and run the program normally

```bash
make
./inventory
```

It prints a small inventory report. Nothing looks wrong from this output
alone -- leaks do not usually crash a program or change its output; they
just quietly waste memory.

### Step 2 -- run it under valgrind

```bash
valgrind --leak-check=full ./inventory
```

Read the `HEAP SUMMARY` and the `LEAK SUMMARY` at the end, then scroll up
to the individual leak records above them. Each record shows a byte
count and a call stack: the stack tells you exactly which function
allocated the memory that was never freed, one frame per function call,
innermost first.

### Step 3 -- fix each leak

Open `inventory.cpp` in your editor. Using the call stacks from valgrind's
output, find and fix all three leaks with the correct `delete` or
`delete[]` call, in the correct place.

### Step 4 -- rebuild and recheck

```bash
make
valgrind --leak-check=full ./inventory
```

Keep fixing and rechecking until the summary reads:

```
definitely lost: 0 bytes in 0 blocks
```

### Step 5 -- exit

```bash
exit
```

The launcher rebuilds your code and reruns valgrind itself to confirm.

## You will know you are done when...

After you exit the shell, the launcher's own valgrind run reports zero
bytes definitely lost and the program's output is unchanged, and it
prints the passphrase. If leaks remain, it shows you the relevant part of
its own valgrind output and offers to let you try again.

## Hints

<details>
<summary>Hint 1 -- what does "definitely lost" actually mean?</summary>

"Definitely lost" means valgrind can prove that, at the moment the
program exited, NOTHING in the program -- no variable, no pointer stored
inside another object -- still referred to that block of memory. It is
gone for good and could never have been freed even if the program kept
running. (Valgrind has other categories too, like "still reachable" for
memory that is still pointed to by something when the program exits, but
this activity only concerns "definitely lost.")

</details>

<details>
<summary>Hint 2 -- reading a leak record's call stack</summary>

A leak record's call stack lists function calls from the innermost
(where `new` or `new[]` was actually called) outward to `main`. Find the
INNERMOST function in YOUR code (not `operator new` itself, which is just
the allocator) -- that tells you which of your functions is responsible
for the allocation that was never freed.

</details>

<details>
<summary>Hint 3 -- new vs. new[]</summary>

`new` allocates a single object and must be freed with plain `delete`.
`new[]` allocates an array and must be freed with `delete[]`. Mixing them
up (`delete`-ing something allocated with `new[]`, or vice versa) is
undefined behavior, separate from the missing-delete leaks in this
activity -- but worth knowing about for your own code.

</details>

## Going further

- Deliberately reintroduce one of the three leaks after fixing all of
  them, and confirm valgrind catches it again with a `--leak-check=full`
  rerun.
- Try `valgrind --leak-check=full --show-leak-kinds=all ./inventory` and
  read about the difference between "definitely lost," "indirectly
  lost," and "possibly lost."
- Compile `inventory.cpp` with `-fsanitize=address` instead (see the ASan
  Autopsy activity) and run it directly (no valgrind needed). Does ASan's
  leak report at program exit point at the same lines valgrind did?
- Research `valgrind --tool=memcheck` vs. other valgrind tools like
  `--tool=callgrind` (used for profiling, covered elsewhere in this
  course). What does the word "tool" mean in valgrind's own terminology?
