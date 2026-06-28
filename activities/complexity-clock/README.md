# Activity: Complexity Clock

Seven programmers each wrote a function to compute the same value. Every
function returns the correct answer. They are not equally fast.

## Concepts covered

- Reading wall-clock benchmark output to identify the slow function
- Analyzing nested loops where the inner loop's cost scales with the input
- Why O(N^2) behavior emerges when a helper function is called N times and the helper itself does O(N) work
- The difference between how code looks and what it actually costs to execute

## How it works

A shell opens with `clock.cpp` and a `Makefile`. Build the benchmark and
run it. Study the timing output and the source code. When you are ready,
type `exit` and answer two questions.

## Getting started

```bash
python3 launch.py
```

A shell opens with `clock.cpp` and a `Makefile`.

### Step 1 -- build and run the benchmark

```bash
make && ./clock
```

Read every line of the timing output before continuing.

### Step 2 -- read the source code

Open `clock.cpp` and read every function, including any helpers. Note
which function is dramatically slower than the others.

### Step 3 -- exit and answer the questions

```
exit
```

The launcher will ask two questions. Answer both correctly to receive the
passphrase.

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

## Going further

- Rewrite the slow function to be O(N) and verify the speedup in the benchmark.
- Profile the original `clock.cpp` with `gprof` or `perf record` and read
  the output. Which line shows up hottest?
- Look up what a flame graph is and how to generate one with `perf` on Linux.
  Identify the slow function in the flame graph.
