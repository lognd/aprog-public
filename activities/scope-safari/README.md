# Scope Safari

Every name in C++ has a scope -- the region of the program where it is
visible. Scope is determined by curly braces `{ }`. A variable lives from
the line where it is declared to the `}` that closes the block containing it.
This rule has some consequences that are easy to miss the first time.

## Getting started

    python3 launch.py

A shell opens inside a fresh copy of the project.

## Your task

`main.cpp` has bugs. The program should print:

    Multiples of 3 in [1..30]: 10
    Above 7 in [1..10]: 3
    Above 14 in [1..20]: 6

Fix `main.cpp` until the output matches, then type `exit`. The launcher
checks your work automatically.

## Resources in the repo

`explore.cpp` demonstrates several scope concepts in isolation. Build and
run it any time:

    make explore && ./explore

You are not required to use it, but it may help you understand what is
happening in `main.cpp`.

## You will know you are done when...

The launcher prints the passphrase.

## Hints

<details>
<summary>Hint 1 -- reading compiler output</summary>

Compile `main.cpp` with `make` and read every line of output, including
warnings. Compilers flag certain scope problems as warnings even when the
code is technically legal. A warning on a specific line is a signal worth
investigating.

</details>

<details>
<summary>Hint 2 -- the first wrong value</summary>

The first line of output is wrong. There is a loop in `main` that is
supposed to accumulate a counter, but the counter never changes. Ask
yourself: how many variables named `count` exist inside the loop body, and
which one does `count++` actually modify?

</details>

<details>
<summary>Hint 3 -- the second wrong value</summary>

The third line of output is wrong even though the program compiles cleanly
and produces no warnings for that code path. `count_above` is called twice.
The second call gives a different kind of wrong answer than the first call.
Read `count_above` carefully. Consider the lifetime of `result` across
multiple calls: does it behave the way you expect?

</details>

<details>
<summary>Hint 4 -- static local variables</summary>

A local variable declared with `static` has a lifetime that extends beyond
the call that created it. It is initialized once (the first time the
function runs) and keeps its value between subsequent calls. This can be
intentional (see `next_id` in `explore.cpp`) or accidental. If `result`
should start at zero for each call, `static` is wrong.

</details>
