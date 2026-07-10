# Activity: Termination Tribunal

A loop **terminates** if it is guaranteed to eventually stop running, no
matter what input it is given. Proving termination, informally, means
finding a **variant** (also called a **measure**) -- some quantity
computed from the loop's own variables that is bounded below by a fixed
value the loop cannot go past, and strictly decreases by at least a
fixed amount every single iteration. A strictly decreasing quantity that
is bounded below cannot decrease forever, so a loop with a valid variant
is guaranteed to stop. This activity puts seven loops on trial: does
each one always terminate, can it loop forever, does it terminate only
for some inputs -- or, for exactly one famously stubborn case, is the
honest answer that nobody has ever proven it either way?

## Concepts covered

- Naming a decreasing, bounded-below **variant/measure** as the informal
  proof technique behind loop termination
- The parity trap: exit tests built on exact equality (`!=`) instead of
  an inequality (`<`, `>=`)
- Unsigned integer underflow: why `i >= 0` can never be false for an
  unsigned loop counter
- Floating-point rounding error breaking an exact-equality exit test
- The Collatz conjecture as a genuine example of a loop whose
  termination is mathematically unproven, not just hard to figure out

## How it works

Each question shows a short loop and asks for the honest verdict: always
terminates, can loop forever, terminates only for some inputs, or (for
one specific question) no one knows -- unproven. Getting a question
wrong shows a detailed explanation that names the decreasing-measure
argument (or explains precisely why no such measure has ever been
found). Answer every question correctly to reveal the passphrase.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly diagnosed the termination behavior of every loop and
the launcher prints the passphrase.

## Going further

- Look up the actual computational verification record for the Collatz
  conjecture -- how large a starting value has been checked so far
  without finding a counterexample? Does a huge verified range change
  how confident mathematicians are that the conjecture is true, even
  without a proof?
- Take the unsigned-countdown bug from this activity and compile it with
  warnings enabled (`-Wall -Wextra` for g++). Does your compiler warn you
  about the always-true `i >= 0` comparison on an unsigned type?
- Write a loop of your own that multiplies a float by 0.5 repeatedly and
  compares it against 0.0 with `!=`. Does it ever actually reach exactly
  0.0, or does it behave differently from the 0.1-accumulation trap in
  this activity? Why might that be different from the addition case?
