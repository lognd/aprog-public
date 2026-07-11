# Activity: Stale Build

You have inherited a prime-counting utility. The CI (continuous integration) pipeline -- the automated system that builds and tests every change -- always runs
`make clean && make` before testing, and it always passes. Your colleague
reports that when they edit `limits.h` and run `make` locally (without
cleaning first), the binary still prints the old result. They have gone on
vacation.

Your job: figure out why incremental builds produce stale output, and fix
the Makefile -- the plain-text file that tells the `make` tool which
commands to run to build the project, organized into named rules. Each
rule lists a target (the file to produce), its prerequisites (the files
it depends on), and a recipe (the commands to run if the target is out of
date).

## Background

`sieve.cpp` implements a trial-division primality test. For each candidate
`n` in `[2, SIEVE_LIMIT]`, it checks every integer `d` from 2 up to the
square root of `n`. If no `d` divides `n` evenly, `n` is prime. The limit
is defined in `limits.h` as a compile-time constant -- a value baked into
the compiled machine code rather than read while the program runs. `main.cpp`
calls `prime_count()` and prints the result.

Because `SIEVE_LIMIT` is a compile-time constant, changing it in `limits.h`
only takes effect if the files that include it are recompiled. That is the
key to this problem.

## Concepts covered

- How `make` uses file timestamps to decide what to rebuild
- The prerequisite list in a Makefile rule and what happens when a file is omitted
- Why a header file that defines a compile-time constant must be a listed dependency
- The difference between a clean build (always correct) and an incremental build (correct only with complete prerequisites)

## How it works

A shell opens inside a fresh copy of the repository. Read the source files,
build the program, and investigate. The fix must make incremental builds
reliable -- do not delete object files by hand as a workaround. Fix the
build system, not the source code: `limits.h`, `sieve.cpp`, and `main.cpp`
are correct; the Makefile is the problem.

The launcher considers the problem fixed when both of the following are
true:

1. `make clean && make && ./count_primes` prints the expected output.
2. If you modify `limits.h` and run `make` again (without cleaning),
   the binary is rebuilt and reflects the change.

Check 2 is the real test. A clean build has always worked. The question is
whether `make` knows that changing `limits.h` means the compiled object
files are out of date.

## Getting started

```bash
python3 launch.py
```

A shell opens inside a fresh copy of the repository. Type `exit` when you
believe you have fixed the problem.

### Step 1 -- build and run the program

```bash
make && ./count_primes
```

Note the output.

### Step 2 -- reproduce the bug

Edit `limits.h` and change `SIEVE_LIMIT` to a different value. Run `make`
without cleaning. Does the output change? If not, you have reproduced the
bug.

### Step 3 -- fix the Makefile

Open the Makefile. Find the rules for each `.o` file and add the missing
header dependencies.

### Step 4 -- verify the fix

Edit `limits.h` again and run `make`. Confirm the binary is rebuilt and the
output reflects your change.

### Step 5 -- exit

```
exit
```

The launcher runs both checks automatically.

## You will know you are done when...

Both checks pass and the launcher reveals the passphrase.

## Hints

<details>
<summary>Hint 1 -- where to start</summary>

Build the program and run it. Then edit `limits.h` and change `SIEVE_LIMIT`
to a different value. Run `make` (without cleaning) and run the binary
again. Did the output change? If not, `make` did not rebuild what it should
have. Think about what has to happen for a change to a header file to take
effect.

</details>

<details>
<summary>Hint 2 -- what make uses to decide whether to rebuild</summary>

`make` compares timestamps. A target is rebuilt if any of its listed
prerequisites are newer than the target itself. If a file that a source
file depends on is not listed as a prerequisite, `make` never knows that
file changed.

</details>

<details>
<summary>Hint 3 -- what is missing from the Makefile</summary>

Open the Makefile. Look at the rule for `sieve.o`. It lists `sieve.cpp`
as a prerequisite. Now open `sieve.cpp`. What other file does it
`#include`? That file also affects the compiled output -- but it is not
listed. Repeat for `main.o`.

</details>

<details>
<summary>Hint 4 -- how to fix it</summary>

A prerequisite line lists all files that, if changed, should cause the
target to be rebuilt. If `sieve.o` depends on both `sieve.cpp` and
`limits.h`, the rule should read:

```makefile
sieve.o: sieve.cpp limits.h
```

Add the missing header to each object-file rule. Then verify by editing
`limits.h`, running `make`, and confirming the binary reflects your change.

</details>

## Going further

- Look up `gcc -MMD -MP`. These flags auto-generate dependency files (`.d`)
  so the Makefile never needs manual header lists. Add them to the build and
  see how the generated `.d` files look.
- Try the same exercise with CMake: does `cmake --build` correctly detect
  header changes without you listing them manually? Why?
- Read about `ninja` as an alternative to `make`. How does it handle
  dependency tracking differently?
