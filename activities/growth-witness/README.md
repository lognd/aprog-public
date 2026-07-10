# Activity: Growth Witness

Knowing an algorithm's Big-O growth rate (covered in the companion activity,
Big-O Lineup) is only useful if you can actually reason with it -- predicting
how much slower something gets as its input grows, or comparing two
different growth rates to see which one wins in the long run. This activity
is pure numeric reasoning, no code: given a growth rate and one measurement,
you estimate what happens at a different input size, or compare two growth
rates directly.

---

## Background

### What "growth rate" means, in numbers

Big-O describes how running time SCALES as the input size n grows -- it does
not predict an exact running time by itself (that also depends on the speed
of the specific computer, compiler, and so on). But if you already know one
measurement (say, "2 milliseconds at n=1000") and you know the growth rate
(say, O(n^2), meaning QUADRATIC -- proportional to n squared), you can
predict the running time at a different input size, because the *ratio*
between running times at two different sizes is determined by the growth
rate alone.

For an algorithm with growth rate O(n^2): if the input size is multiplied by
a factor of k, the running time is multiplied by k^2 (k squared), because
(k * n)^2 = k^2 * n^2. For O(n) (LINEAR): multiplying the input by k
multiplies the time by that same factor k. For O(1) (CONSTANT): multiplying
the input by any factor at all does not change the time.

### Why constants only delay the crossover, never change the winner

A growth rate like O(n) or O(n^2) hides an unwritten constant factor -- the
real running time might be `1000 * n` or `0.001 * n`, but Big-O calls both
of these simply O(n), because that constant does not change how the
function SCALES. This means a large constant can make a "worse" growth rate
temporarily faster than a "better" one, for SMALL n -- `1000n` is bigger than
`n^2` for any n below 1000. But once n is allowed to grow without bound, the
function with the better growth rate always eventually wins, and stays
ahead forever after that. This activity asks you to reason about this
"eventually" behavior directly, more than once.

### `log2`, and a shortcut worth memorizing

`log2(x)` (LOGARITHM base 2) answers "how many times do you have to double,
starting from 1, to reach x?" -- equivalently, "2 raised to what power gives
x?" A genuinely useful shortcut: `2^10 = 1024`, which is very close to
1,000. So `log2(1000)` is approximately 10. Since multiplying two numbers
corresponds to ADDING their logarithms (`log2(a*b) = log2(a) + log2(b)`),
you can estimate `log2` of any power-of-a-thousand-ish number quickly: for
example, `log2(1,000,000) = log2(1000 * 1000)`, approximately `10 + 10 =
20`. This shows up directly in estimating how many steps a binary search or
similar O(log n) algorithm needs on a realistic input size.

---

## Concepts covered

- Scaling a measured running time using a known Big-O growth rate
- The difference between "faster for small n" and "grows faster eventually"
- Why constant factors delay a crossover point but never change the
  long-run winner between two different growth-rate classes
- Estimating `log2(x)` using the `2^10 is approximately 1000` shortcut
- Recognizing the "doubling the input adds one step" signature of O(log n)
- Amortized O(1) as a fixed cost that does not scale with input size at all

---

## How it works

You will be shown seven to nine questions, one at a time. Each states a
required answer FORMAT explicitly in its own prompt -- some want a single
number (in milliseconds, or a plain count), and others want you to choose
from a short list of enumerated options (like `n^2 grows faster`). Read the
prompt carefully for the exact expected format before answering. Wrong
answers are explained before you try again; correct answers unlock a full
explanation. All questions must be answered correctly to receive the
passphrase.

---

## Getting started

```bash
python3 launch.py
```

---

## You will know you are done when...

The launcher prints the passphrase after every question has been answered
correctly.

---

## Hints

<details>
<summary>Hint 1 -- for a scaling question, find the input-size multiplier k first</summary>

Work out how many times bigger the new input size is compared to the
measured one (that ratio is k), then apply the rule for the stated growth
rate: multiply the time by k for O(n), by k^2 for O(n^2), not at all for
O(1), and so on.

</details>

<details>
<summary>Hint 2 -- "eventually" means ignore small n entirely</summary>

For any "which grows faster eventually" question, do not reason about any
one specific small value of n. Instead, compare the two functions' shapes
directly (for example, `n^2 = n * n` versus `1000n = 1000 * n`) and ask what
happens to their ratio as n keeps growing without any limit.

</details>

<details>
<summary>Hint 3 -- for `log2` estimates, anchor on `2^10 is approximately 1000`</summary>

Break the number you are taking `log2` of into a product of numbers you can
estimate `log2` for individually (especially factors of 1000, or exact
powers of two like 16 or 32), then add those estimates together.

</details>

---

## Going further

- Pick a real O(n log n) sorting algorithm (like `std::sort`, which is
  typically introsort, a hybrid that is O(n log n) in the worst case) and
  time it on vectors of size 100,000 and 1,000,000 using `std::chrono`.
  Does the ratio roughly match what O(n log n) predicts (a bit more than a
  10x increase, since log n also grows a little)?
- Compute the exact crossover point between `1000n` and `n^2` algebraically
  (solve `1000n = n^2` for n), and confirm it matches the n=1000 value used
  as an example in this activity's reasoning.
- Using the `2^10 is approximately 1000` shortcut, estimate `log2` of the
  number of atoms in the observable universe (roughly 10^80). How many
  "halvings" is that? Compare it to how few steps a binary search needs on
  even the largest realistic datasets.
- Write a small C++ program that calls `std::vector::push_back` in a loop
  1,000,000 times, and prints `v.capacity()` every time it changes. Confirm
  the capacity roughly doubles each time it grows, matching the amortized
  O(1) analysis from Big-O Lineup.
