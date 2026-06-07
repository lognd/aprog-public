# Control Gauntlet

Four programs, four things to know: short-circuit evaluation, `break`,
`continue`, and De Morgan's law.

## Getting started

    python3 launch.py

A shell opens with four source files. One is a demo -- compile and run it
to see short-circuit evaluation in action. The other three have bugs.
Fix all three to earn the passphrase.

## short_circuit.cpp -- exploration demo

Compile and run it:

    g++ -std=c++17 -Wall -o short_circuit short_circuit.cpp && ./short_circuit

Read the output carefully. With `&&`, if the left operand is `false`, the
right operand is never evaluated. With `||`, if the left operand is `true`,
the right operand is never evaluated. Notice which function calls are
skipped entirely for each element. Nothing to fix here.

## The three broken programs

Each has exactly one bug. Read each program, understand what it is supposed
to compute, compile it, check whether the output is correct, and fix the bug.

When all three produce the correct output, type `exit`. The launcher
compiles and runs each one automatically and reveals the passphrase only
if all three are correct.

## You will know you are done when...

The launcher prints the passphrase.

## Hints

<details>
<summary>search.cpp hint</summary>

The program searches through a range and records a match each time it finds
one. Consider what happens when there is more than one match: does the
program stop at the right one? What keyword exits a loop immediately when
the desired result has been found?

</details>

<details>
<summary>filter.cpp hint</summary>

The program is supposed to add only certain numbers to a running total.
Some numbers should be excluded. The exclusion check runs, but something
is missing that would prevent the rest of the loop body from executing when
the check succeeds. What keyword skips the remainder of a loop iteration?

</details>

<details>
<summary>leap.cpp hint</summary>

The leap year rule is: divisible by 4, EXCEPT centuries (divisible by 100),
which only count if also divisible by 400. The comment in the source states
the correct logic. Compare the comment carefully to the code. The bug is
a single wrong logical operator (`&&` vs `||`) somewhere in the condition.
Think about what each version of the condition actually accepts.

</details>

<details>
<summary>leap.cpp deeper hint -- De Morgan's law</summary>

De Morgan's law:
  `!(A && B)` is equivalent to `!A || !B`
  `!(A || B)` is equivalent to `!A && !B`

The leap year condition has two parts joined by a logical operator. The
correct rule requires the first part to use `&&` (both conditions must hold).
The buggy version uses `||` (either condition suffices, which is far too
permissive or too restrictive depending on what surrounds it). Write out
what each version accepts before changing the code.

</details>
