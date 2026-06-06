# Control Gauntlet

Three C++ programs, three concepts.  One is a demo -- just run it and watch.
The other two have bugs.  Fix both to earn the passphrase.

## Getting started

    python3 launch.py

The launcher drops you into a shell with the three source files.  Follow the
steps below, then type `exit`.

## Step 1 -- short-circuit evaluation (exploration only)

Compile and run `short_circuit.cpp`:

    g++ -std=c++17 -o short_circuit short_circuit.cpp && ./short_circuit

The program calls two functions -- `is_large(x)` and `is_even(x)` -- and
prints which ones actually execute for each element in the array.

- With `&&`: if the left side is `false`, the right side is **never called**.
- With `||`: if the left side is `true`, the right side is **never called**.

This matters whenever the right-side expression has a side effect (printing,
modifying state, causing a crash).  Nothing to fix here; understand the
pattern and move on.

## Step 2 -- De Morgan's law (`demorgan.cpp`)

The function `keep(n)` is supposed to keep a number if it is **not** (negative
**and** odd at the same time) -- equivalently, keep it if it is non-negative
**or** even (or both).

The condition uses the wrong logical operator.  Read the De Morgan's law
reminder at the top of the file and change exactly one character.

Compile and run to check your fix:

    g++ -std=c++17 -o demorgan demorgan.cpp && ./demorgan

Expected output: `Kept: 5`

## Step 3 -- break and continue (`break_continue.cpp`)

The program has two loops, each missing one keyword.

**Loop 1** searches for the first multiple of 7 in `[1..50]`.  Read the loop
carefully: what does it do when it finds a match?  What should it do?

**Loop 2** sums only the odd numbers in `[1..10]`.  Read the `if` block for
even numbers: what should happen to those numbers?

Add one keyword to each loop.  Compile and run:

    g++ -std=c++17 -o break_continue break_continue.cpp && ./break_continue

Expected output: `First: 7 Sum: 25`

## Step 4 -- exit

Once both programs produce the correct output, type `exit`.  The launcher
compiles and runs `demorgan.cpp` and `break_continue.cpp`, verifies both
outputs, and reveals the passphrase.

## Hints

<details>
<summary>De Morgan's hint</summary>

Apply De Morgan's law to `!(n < 0 || n % 2 != 0)`:

    !(A || B)  ==  !A && !B

So the current condition is equivalent to `n >= 0 && n % 2 == 0` -- which
keeps only non-negative AND even numbers.  The goal is non-negative OR even.
One character needs to change inside the `!( )`.

</details>

<details>
<summary>break hint</summary>

Once the loop records `first`, there is no reason to keep iterating.  A
`break;` statement exits the innermost loop immediately.

</details>

<details>
<summary>continue hint</summary>

`continue` skips the rest of the current loop body and jumps straight to the
next iteration.  Place it where you want the loop to stop processing the
current element.

</details>

## Bonus -- do-while and switch-case

Two constructs you may not have seen yet:

`do { ... } while (cond)` -- the body always runs at least once because the
condition is checked *after* the body, not before.

`switch (expr) { case v: ... break; }` -- dispatches to the matching `case`
label.  Without a `break`, execution falls through to the next case.  All
`case` labels share one scope (see Scope Safari for why that can surprise you).
