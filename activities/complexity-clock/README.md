# Activity: Complexity Clock

Seven functions all compute the same sum, sum(1 + 2 + ... + N). All seven
give the right answer. They are not equally fast. Build the benchmark, watch
the clock, then trace four short functions by hand to see exactly why some
functions do far more work than others.

## Concepts covered

- Reading a wall-clock benchmark table (a printed list of measured running
  times) to spot which implementation is unexpectedly slow
- Counting, by hand, how many times a specific line inside a loop actually
  runs for a given input
- Nested loops whose inner loop length depends on the outer loop's current
  position, not a fixed number
- The taste of it: two functions can both be "correct" and still take wildly
  different amounts of time as the input grows. Some do work roughly
  proportional to the input size; others do work that grows like the input
  size multiplied by itself -- double the input, and that second kind takes
  roughly four times as long, not twice.
- Why code that "looks like one loop" can secretly cost as much as two
  nested loops, and vice versa

(Later in the course, in Complexity Theory, you will learn the formal
notation for describing this precisely.)

## How it works

This activity has two parts. First, a shell opens inside a copy of
`clock.cpp` and a `Makefile`. Build and run the benchmark to see seven
functions -- alice, bob, carol, dave, eve, frank, and grace -- all compute
the same sum, timed side by side. You cannot leave this shell until the
program has been built at least once.

After you exit the shell, the launcher asks four questions. Each question
shows you a short function (again named alice, bob, carol, and dave, but
with new code written out directly in the question -- these are not the
same function bodies as the ones in `clock.cpp`). One line in each function
is marked with `// <--`. Your job is to trace the function by hand for an
input of 10 and say exactly how many times that marked line executes.
Answer all four correctly to receive the passphrase.

## Getting started

```bash
python3 launch.py
```

A shell opens inside a fresh copy of the project.

### Step 1 -- build and run the benchmark

```bash
make && ./clock
```

You must build `clock` before the launcher will let you continue.

### Step 2 -- read the output carefully

All seven functions print the same answer. Note which ones are fast and
which ones are slow. Open `clock.cpp` and read every function while the
numbers are still fresh.

### Step 3 -- exit and start the quiz

```
exit
```

The launcher asks four short questions about counting loop executions.

## You will know you are done when...

All four questions are answered correctly and the launcher reveals the
passphrase.

## Hints

<details>
<summary>Hint 1 -- reading the benchmark output</summary>

The `Time` column shows how long each function took in milliseconds. All
seven produce the same answer, so the differences you see are purely about
how much work each one does, not about correctness. Find the slowest one
and reread its source with fresh eyes -- including any helper function it
calls.

</details>

<details>
<summary>Hint 2 -- a loop body only counts the line it wraps</summary>

The marked line in each quiz question is inside a loop (or nested loops).
It runs once for every time control reaches that exact spot -- not once per
call to the function, and not once per outer-loop pass if there is an inner
loop underneath. Write out the values the loop variable takes, one by one,
if you are not sure.

</details>

<details>
<summary>Hint 3 -- nested loops and the doubling question</summary>

When one loop is nested inside another, and the inner loop's length depends
on where the outer loop currently is, add up the inner-loop lengths across
every outer step rather than multiplying by a fixed number. Try it for a
small input by hand first, then see if you can spot the pattern before
plugging in 10.

</details>

## Going further

- Rewrite the slowest function in `clock.cpp` to do work roughly
  proportional to N instead of N multiplied by itself, and confirm the
  speedup in the benchmark.
- Profile the original `clock.cpp` with `gprof` or `perf record` and read
  the output. Which line shows up hottest?
- Look up what a flame graph is and how to generate one with `perf` on
  Linux. Identify the slow function in the flame graph.
