# Activity: Big-O Lineup

Big-O notation is a way of describing how an algorithm's running time grows
as its input gets bigger, while deliberately ignoring details that do not
matter for that question -- exactly how fast your specific computer is, or
small constant amounts of extra work. "O(n)" means the running time grows
roughly in direct proportion to the input size n; "O(n^2)" means it grows
roughly in proportion to n squared; and so on. It is the vocabulary
programmers use to talk about *how well an algorithm scales*, independent of
any one machine or measurement.

This activity shows you ten short C++ functions. For each one, you identify
its time complexity -- its Big-O growth rate -- as a function of the size of
its input, called n. There is no code to run: this is about reading code and
reasoning about how many times each line of it executes as n grows.

---

## Background

### What "n" means

In every question here, n refers to the SIZE of the relevant input -- the
number of elements in a vector, the value of an integer parameter, and so
on. Each question tells you explicitly what n represents for that function.

### The five growth rates in this activity

- **O(1) -- constant time.** The running time does not depend on the input
  size at all. Doubling, or even multiplying the input by a million, changes
  nothing about how much work is done.
- **O(log n) -- logarithmic time.** The running time grows very slowly: only
  by discarding a large fraction of the remaining work at each step (the
  classic example is repeatedly cutting a range in half). Doubling the input
  size only ever adds ONE more step.
- **O(n) -- linear time.** The running time grows in direct proportion to
  the input size: doubling the input roughly doubles the work.
- **O(n log n) -- "linearithmic" time.** Roughly n steps, each doing O(log n)
  work (or vice versa). The signature shape of efficient sorting algorithms.
- **O(n^2) -- quadratic time.** The running time grows in proportion to the
  SQUARE of the input size, typically from one loop nested inside another.
  Doubling the input roughly quadruples the work.

### Worst case, best case, and why "the complexity" usually means worst case

Some functions can finish early -- for example, a loop that returns the
moment it finds what it is looking for. Such a function's running time
depends on the specific input, not just its size: a lucky input finishes
fast (the BEST case), while an unlucky one forces the function to do the
maximum possible amount of work (the WORST case). When a complexity is
stated without saying which case it means, it conventionally refers to the
worst case -- the one guarantee that holds no matter what input you are
given. This activity asks about the worst case explicitly whenever it
matters.

### Amortized complexity

Some operations are usually cheap but occasionally expensive -- the
`push_back` question in this activity is the classic example: appending to a
`std::vector` is usually O(1) (there is spare room), but occasionally
triggers a full resize that copies every existing element, an O(n)
operation. AMORTIZED complexity answers a different, more useful question:
"what is the true average cost per operation, over a long sequence, provably
-- not just by luck?" It works by spreading the (rare) expensive operations'
total cost evenly across the (common) cheap ones. `push_back`'s amortized
cost is O(1), even though any single call might occasionally be O(n).

---

## Concepts covered

- Reading loops (single, sequential, and nested) to determine growth rate
- Triangular nested loops (`for j < i`) -- still O(n^2), with the constant
  factor explained
- Calling an O(n) helper function from inside a loop -- multiplies, not adds
- Sequential loops -- add their costs, do not multiply
- Halving loops and binary search -- the O(log n) shape
- Early-exit functions -- distinguishing best case from worst case
- Amortized analysis, using `std::vector::push_back` as the motivating case
- Contiguous-array random access (`operator[]`) as a true O(1) operation

---

## How it works

Each question shows one short C++ function (plus, for the amortized
question, a code comment describing `push_back`'s behavior instead of a full
function). Read the code, then type the function's time complexity exactly
as one of the five listed options (for example, `O(n log n)`, with that
exact spacing and capitalization). Wrong answers are explained in detail
before you try again; correct answers unlock a full explanation and move you
to the next question. All ten questions must be answered correctly to
receive the passphrase.

---

## Getting started

```bash
python3 launch.py
```

---

## You will know you are done when...

The launcher prints the passphrase after all ten functions have been
correctly classified.

---

## Hints

<details>
<summary>Hint 1 -- count how many times the innermost line of code actually runs</summary>

For any loop-based question, the most reliable method is to literally count:
as a function of n, how many times does the single "unit of work" deepest
inside the function actually execute? That count's growth rate, as a
function of n, is the function's Big-O.

</details>

<details>
<summary>Hint 2 -- nested loops multiply, sequential loops add</summary>

If one loop runs INSIDE another, their costs multiply (an O(n) outer loop
around an O(n) inner loop gives O(n^2)). If one loop finishes completely
before the next one begins, their costs add (O(n) then O(n) gives O(2n),
which simplifies to O(n), since Big-O drops constant multipliers).

</details>

<details>
<summary>Hint 3 -- a loop that halves its remaining range each step is O(log n)</summary>

Whenever you see an index or a range shrinking by roughly half on each
iteration (rather than moving by a fixed amount, like +1), that is the
signature of O(log n) -- ask "how many times can this be halved before it
reaches 1?"

</details>

---

## Going further

- Take the `countPairs` (triangular loop) function from this activity and
  actually run it for a few values of n, counting the real number of
  `count++` calls. Confirm it matches `n(n-1)/2`.
- Time `sumAll` on vectors of size 1,000,000 and 10,000,000 using
  `std::chrono`. Does the measured ratio roughly match what O(n) predicts?
- Write your own version of `hasDuplicate` that instead sorts the vector
  first (an O(n log n) operation) and then does a single linear scan looking
  for adjacent equal elements. What is the overall complexity of that
  version, and why is it better than the O(n^2) nested-loop version for
  large inputs?
- Look up why `std::vector` doubles its capacity on resize instead of
  growing by a fixed amount (like +10) each time. Work out, using the same
  reasoning as the `push_back` question, what the amortized cost per
  `push_back` would become if it grew by a fixed amount instead.
