# Activity: Paradigm Refactor Detector

Knowing that a loop is "imperative" (a step-by-step sequence of statements
that overwrite variables) and a pipeline is "functional" (a chain of small
transformations that produce new values instead of changing old ones) is
labeling. Knowing what you actually gain or lose when you rewrite one as
the other is understanding. This activity is about the second thing. If the
words imperative, functional, and declarative are new to you, do the
paradigm-lineup activity first -- this one builds directly on it.

Each question shows the same tiny problem solved two different ways, side by
side in one code block, and asks a pointed comparison question: which version
can run without any variable mutating? Which one depends on statement order?
Which one is guaranteed to return the same output for the same input? The
paradigm labels never appear in the answers -- only their consequences do.

---

## Background

### Why the style of code has consequences

Two programs can compute identical results and still behave very differently
as software: one may be safe to run from two places at once while the other
corrupts shared data; one may be trivial to unit-test (a unit test is a
small automated check that one piece of code works correctly on its own)
while the other needs elaborate setup. These differences come from
structural properties that each paradigm either guarantees or gives up. The
big ones:

**Mutation.** Mutation means overwriting a variable's stored value with a
new one. Imperative code works this way constantly -- an accumulator (a
variable that collects a running result, like a sum) updated on every loop
pass, or an object's field overwritten by a setter method.
Functional-style code produces new values instead of changing old ones. Why
care? A value that never changes cannot be changed by surprise. If two
parts of a program share one changeable object, either part can yank the
rug out from under the other. That whole category of bug is called an
**aliasing bug** ("aliasing" means two names referring to the same object),
and values that never change make it impossible.

```cpp
// mutating: every += reassigns total
int total = 0;
for (int x : nums) { total += x * x; }

// non-mutating pipeline (pseudocode): new values only
return nums.map(x => x * x).reduce((a, b) => a + b, 0);
```

**Order-dependence.** A sequence of imperative statements is fragile:
reorder two lines and the meaning changes. A single composed expression has
no statement sequence to get wrong. This matters for reading code (you must
mentally replay imperative steps in order), for refactoring (restructuring
code without changing what it does -- moving lines around is risky when
order matters), and for parallelism (running pieces of work at the same
time -- steps with no required order can safely run simultaneously).

**Referential transparency.** A function is referentially transparent when
the same input always produces the same output, with no hidden state
involved. `average_of({1,2,3})` returning 2 today, tomorrow, and in every
test run is a guarantee an object with an internal running total simply
cannot make -- its answer depends on its entire call history. Pure functions
are the easiest code in the world to test for exactly this reason.

**Hidden state vs values.** Compare a lookup function that returns a raw
pointer and, on failure, sets a global error flag (a variable living
outside every function, which any code can read or forget to read) against
one that returns an `optional<User>`. `std::optional` is a C++ type that
holds either a value or nothing at all, and forces you to check which
before using it. The first design hides the failure signal in a side
channel the caller can forget to check. The second makes "this might not
exist" part of the returned value itself, so the caller must confront it.
Encoding outcomes in values instead of side effects is the same shift in
spirit as the move from imperative to functional style.

None of this makes one paradigm "better." Imperative loops can compute
three statistics in a single pass where a composed pipeline needs three;
in-place mutation is often the fastest option and sometimes the only
practical one. The point is that each style buys you specific guarantees and
costs you specific things -- and a good engineer picks per situation, with
eyes open.

---

## Concepts covered

- Mutation vs producing new values, and why immutability prevents aliasing
  bugs
- Order-dependence of imperative statement sequences vs composed expressions
- Referential transparency: same input, same output, no hidden state
- Pure functions vs objects with accumulating internal state
- Testability and reuse consequences of decomposing one loop into composable
  functions (and the performance cost of extra passes)
- Encoding failure in return values (`optional`) vs side channels (global
  error flags)

---

## How it works

The launcher shows you eight questions. Each displays one code block
containing two labeled versions -- `version a` and `version b` -- of the
same tiny problem. C++ is used where possible; a few pipeline examples are
in clearly-marked pseudocode (a code-like sketch meant to be read by
humans, not compiled) that you only need to read.

Each prompt asks a pointed comparison question and ends with an explicit
option list, for example:

```
Type exactly one of: version a / version b / both / neither
```

Type your answer exactly as one of the listed options. Wrong answers get
feedback aimed at the specific property you misjudged; correct answers
unlock a full explanation of the consequence being illustrated. Answer all
eight correctly and the launcher decrypts and prints the passphrase.

---

## Getting started

```bash
python3 launch.py
```

For each question, do not just identify which version "looks functional."
Actually check the claimed property against each version: scan version a
line by line for reassignments, ask whether version b's steps could be
reordered, trace what happens on a second identical call.

---

## You will know you are done when...

The launcher prints `All correct.` followed by the passphrase between two
horizontal rules. Record the passphrase -- it is your proof of completion.

---

## Hints

<details>
<summary>Hint 1 -- how to check for mutation mechanically</summary>

Look for any of: `=` applied to a name that already has a value, `+=` and
friends, `++`/`--`, or a method whose job is to modify the object it is
called on (`push_back`, `setWidth`). If none of those appear, nothing
mutates. Declaring and initializing a fresh variable once is not mutation.

</details>

<details>
<summary>Hint 2 -- the second-call test</summary>

For any question about "same input, same output," imagine calling the thing
twice in a row with identical arguments and write down what each call
returns. An object with internal counters gives a different answer the
second time because its state grew. A pure function cannot -- it has no
memory of the first call.

</details>

<details>
<summary>Hint 3 -- read the option list before deciding</summary>

The options include `both` and `neither`, and a couple of questions use
them as serious candidates. After picking your favorite version, explicitly
check the other one against the question too -- the point of several
questions is that a property you expect only one version to have (or lack)
is shared, or absent, in a way that surprises.

</details>

---

## Going further

- Take the three-statistics question (max, sum, count in one loop vs three
  library calls) and benchmark both versions -- that is, measure and
  compare their running time -- in real C++ over a 10-million-element
  `std::vector<int>` compiled with `-O2`. How large is the single-pass
  advantage really?
- Rewrite the mutating `Widget` setter example as a real C++ class with
  `with_*` methods that return new objects by value. What does the copy cost
  you, and when would that matter?
- The `optional<User>` question previews a bigger idea: encoding all
  outcomes in return types. Look up `std::expected` (C++23), which carries
  either a value or an error. How would `find_user` look with it?
- Find a loop you wrote earlier this semester that both filters and
  transforms data. Rewrite it with `std::copy_if` / `std::transform` (or
  C++20 ranges) and compare: which version would be easier to unit-test, and
  which was easier to write?
