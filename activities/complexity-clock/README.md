# Complexity Clock

Seven programmers each wrote a function to compute the same value. Every
function returns the correct answer. They are not equally fast.

## Getting started

    python3 launch.py

A shell opens with `clock.cpp` and a `Makefile`. Build the benchmark and
run it. Study the timing output and the source code. When you are ready,
type `exit` and answer two questions.

## Your task

1. Build and run the benchmark.
2. Read the timing output.
3. Read every function in `clock.cpp`, including any helpers.
4. Exit the shell and answer the questions.

## You will know you are done when...

Both questions are correct and the launcher reveals the passphrase.

## Hints

<details>
<summary>Hint 1 -- reading the output</summary>

The `Time` column shows how long each function took in milliseconds. All
seven produce the same answer. Look for the one that is dramatically slower
than the others. Once you have identified it, read its source code
carefully -- all of it, including any functions it calls.

Do not be misled by code that looks complicated or has nested loops.
Read what the code actually does, not just what it looks like at a glance.

</details>

<details>
<summary>Hint 2 -- why the slow one is slow</summary>

A function that calls another function is not necessarily O(1) per call.
The cost of a function call depends on what that function does. If a
function contains a loop, every call to it runs that loop.

Ask yourself: if the outer loop in the slow function runs N times, and
each iteration calls a helper, how many total loop iterations happen?
What does the helper do for a call with argument k?

</details>

<details>
<summary>Hint 3 -- the doubling question</summary>

Work out the total number of operations for small N.
For N=4: tally(1) + tally(2) + tally(3) + tally(4) = 1+2+3+4 = 10
For N=8: tally(1)+...+tally(8) = 1+2+...+8 = 36
When N doubles from 4 to 8, the work goes from 10 to 36 -- roughly a
factor of 4, not 2. The general formula is N*(N+1)/2, which grows as N^2.

</details>
