# Activity: ASan Autopsy

AddressSanitizer (usually shortened to **ASan**) is a tool built into g++
and clang++ that catches memory-safety bugs -- reading or writing memory
you should not be touching -- the moment they happen, instead of letting
them silently corrupt your program's memory or crash it somewhere
unrelated and confusing later. You turn it on with a single compiler flag,
`-fsanitize=address`, and when your program does something wrong, it
prints a detailed report explaining exactly what happened and where.

The reports look intimidating the first time you see one -- walls of hex
addresses and stack traces. This activity strips that intimidation away by
showing you real reports, generated from real compiled programs, and
teaching you to read their structure so you can extract the two things
that actually matter: what kind of bug this is, and which line caused it.

## Background

Every ASan report shares the same basic shape:

1. A headline naming the bug category, e.g.
   `ERROR: AddressSanitizer: heap-buffer-overflow`.
2. One or more STACK TRACES -- lists of function calls showing where
   something happened. The FIRST trace is always the CRASH SITE: where
   the bad access itself occurred. It usually starts with a line like
   `WRITE of size 4 at 0x... thread T0` or `READ of size 4 at 0x...`.
3. Depending on the bug, further traces showing where the memory involved
   was ALLOCATED (`allocated by thread T0 here`) and, for use-after-free
   and double-free bugs, where it was FREED (`freed by thread T0 here`).
4. A `SUMMARY:` line restating the bug category and crash location.

Each trace's `#0` frame -- the very first line under it -- names the exact
source file and line number responsible. Reading an ASan report is mostly
a matter of finding the crash-site trace first, then checking whether
there is a "freed by" trace (which points to a use-after-free or
double-free) or only an "allocated by" trace (which points to a bounds
overflow or, if the report appears at program exit with no crash-site
trace at all, a leak).

You will also see a lot of noise you can safely ignore: raw hex addresses
like `0xf9d2acc00b64`, `pc`, `bp`, and `sp` values, and `thread T0` (every
program in this activity runs on a single THREAD -- one independent
sequence of execution within the program -- so it is always thread
number 0). None of that noise changes from question to question; the
questions below can always be answered from the headline and the `#0`
frames alone.

## Concepts covered

- Reading the structure of an AddressSanitizer report: headline,
  crash-site trace, allocation trace, free trace, summary
- Distinguishing heap-buffer-overflow, heap-use-after-free, double-free,
  memory-leak, and stack-buffer-overflow from report structure alone
- The difference between HEAP memory (allocated with `new`/`new[]`,
  reported via `operator new`) and STACK memory (ordinary local
  variables, reported as "located in stack of thread T0")
- LeakSanitizer (LSan), which ships with ASan and reports leaks at
  program exit rather than at the moment of a bad access
- How ASan intercepts standard library functions like `strcpy` so that
  overflows happening INSIDE them are still caught

## How it works

Each question shows a short C++ program (compiled with
`g++ -fsanitize=address -g`) and a real, trimmed excerpt of the report it
actually produced. Most questions ask you to name the bug category; a
couple ask you to identify the exact source LINE NUMBER responsible,
based on reading the correct stack trace within the report.

## Getting started

```bash
python3 launch.py
```

For each question, read the program first, then the report. Try to
predict the category before reading the report closely, then use the
report to confirm or correct yourself.

## You will know you are done when...

All eight questions have been answered correctly and the launcher prints
the passphrase.

## Hints

<details>
<summary>Hint 1 -- heap or stack?</summary>

If the "allocated by" (or "is located in") section names `operator new`
or `operator new[]`, the memory is on the HEAP. If it instead says
"is located in stack of thread T0," the memory is an ordinary local
variable on the STACK -- no `new` involved at all.

</details>

<details>
<summary>Hint 2 -- does a "freed by" section exist?</summary>

If the report includes a `freed by thread T0 here` trace, the bug
involves memory that was already released: either a use-after-free (the
crash-site trace is a READ or WRITE) or a double-free (the crash-site
trace is itself another call to `delete`/`free`). If there is no "freed
by" section, the memory was never freed at all, which points toward a
leak or a bounds overflow instead.

</details>

<details>
<summary>Hint 3 -- no crash-site trace at all?</summary>

If the report has no `WRITE of size`/`READ of size` line and instead
starts with `LeakSanitizer: detected memory leaks`, it is not describing
a moment where the program did something wrong mid-execution -- it is a
summary produced AFTER the program exited, listing every allocation that
nothing ever freed.

</details>

## Going further

- Compile one of this activity's programs yourself with
  `g++ -fsanitize=address -g -O0` and run it. Does your local report look
  identical to the one shown here, or do the addresses and offsets
  differ? Which parts of the report stay the same across runs and
  machines, and which parts do not?
- Fix each buggy program (add the missing `delete`/`delete[]`, correct the
  off-by-one, guard the `strcpy` with a size check) and confirm ASan
  reports no errors on the fixed version.
- Try `-fsanitize=undefined` in addition to `-fsanitize=address` (you can
  combine them: `-fsanitize=address,undefined`). Write a small program
  with signed integer overflow and see what a different sanitizer's
  report looks like.
- Read about "shadow memory" -- the mechanism ASan uses internally to
  track which bytes are valid, freed, or red-zone padding around every
  allocation. Why does this make ASan catch bugs that a plain segfault
  would miss entirely?
