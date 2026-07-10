# Study Guide 26: Memory & Profiling Tools (valgrind, asan, perf, gprof)

This module teaches the two workhorse memory-error tools: AddressSanitizer
(compiled in with `-fsanitize=address`, reporting bad accesses the moment
they happen) and valgrind (running the unmodified binary in a simulator,
reporting leaks at exit). Students learn to read both tools' reports well
enough to name the bug class and find the responsible line.

## Know before you start

- Heap allocation and the `new`/`delete`, `new[]`/`delete[]` pairing rules
  [assumed: row 10 -- Memory Model]
- The resource-management bug vocabulary: double free, leak, dangling
  pointer, use-after-free [assumed: row 25 -- Dynamic Memory]
- Stack traces and frame numbering [assumed: row 10 -- Memory Model]
- Buffer overflows on fixed-size char arrays [assumed: row 12 -- C-Style
  Strings & Arrays]

## Taught here

Concept: reading an ASan report
- Know that AddressSanitizer (ASan) is built into g++/clang++, enabled
  with `-fsanitize=address`, and catches memory-safety bugs the moment
  they happen instead of letting them corrupt memory and crash somewhere
  unrelated later.
- Know the fixed report structure: a headline naming the bug category, a
  crash-site stack trace first (starting `READ of size N` / `WRITE of size
  N`), then traces for where the memory was allocated (`allocated by`) and
  -- for freed-memory bugs -- where it was freed (`freed by`), ending with
  a `SUMMARY:` line.
- Know that each trace's `#0` frame names the exact source file and line
  responsible.
- Be able to classify the bug from report structure alone: a `freed by`
  trace present means use-after-free (crash site is a READ/WRITE) or
  double-free (crash site is itself another `delete`/`free`); no `freed
  by` trace points to a bounds overflow; no crash-site trace at all, with
  a `LeakSanitizer: detected memory leaks` header at exit, means a leak.
- Know the heap-vs-stack tell: `operator new`/`operator new[]` in the
  allocation section means heap memory; "is located in stack of thread
  T0" means an ordinary local variable.
- Know that LeakSanitizer (LSan) ships with ASan and reports leaks at
  program exit rather than at the moment of a bad access, and that ASan
  intercepts library functions like `strcpy` so overflows inside them are
  still caught.

Concept: valgrind leak checking
- Know that valgrind runs the compiled program inside a simulator and
  watches every memory access from the outside -- no recompilation or
  special flag needed, just `valgrind --leak-check=full ./program`.
- Know that "definitely lost" means valgrind can prove no pointer anywhere
  in the program still referred to that block at exit -- it could never
  have been freed even if the program kept running (distinct from "still
  reachable" and other categories).
- Be able to read an individual leak record: a byte count plus a call
  stack listed innermost-first; the responsible line is the innermost
  frame in YOUR code, not `operator new` itself.
- Know the three classic leak shapes exercised here: replacing an owned
  allocation without freeing the old one first; freeing a container node
  but forgetting the heap-allocated data it owns; and an early-return path
  that exits a function after allocating but before the free.
- Know that `new` pairs with `delete` and `new[]` pairs with `delete[]`,
  and that mixing them is undefined behavior distinct from a missing-free
  leak.
- Know that leaks do not usually crash a program or change its output --
  the program looks fine while quietly wasting memory, which is why a tool
  is needed at all.
- Know the target end state of a leak-fixing session: `definitely lost: 0
  bytes in 0 blocks` with the program's normal output unchanged.

## Study checklist

- [ ] Given an ASan report excerpt, name the bug category and the
      responsible source line.
- [ ] State the report feature that distinguishes use-after-free from
      double-free from heap-buffer-overflow from leak.
- [ ] Explain the difference between how ASan and valgrind attach to a
      program.
- [ ] Define "definitely lost" precisely.
- [ ] Given a valgrind leak record, identify which of your functions
      allocated the lost memory.
- [ ] Describe the early-return leak shape and its fix.

## Practiced in

`asan-autopsy`, `valgrind-leak-lab`
