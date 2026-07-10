# Study Guide 36: Proofs & Invariance

This module teaches an informal, engineering-flavored version of two
proof techniques for reasoning about loops: the loop invariant (what stays
true every time through) and the termination variant (what strictly
decreases every time through, bounded below). Both activities are pure
reasoning about existing loops -- no code to write.

## Know before you start

- Loop syntax, exit conditions, and control flow [assumed: row 6 --
  Control & Functions]
- Unsigned integer types and overflow/underflow wraparound [assumed: row 5
  -- Variables & Type]
- Floating point representation and why exact equality comparisons are
  unreliable [assumed: row 5 -- Variables & Type]

## Taught here

Concept: the loop invariant
- Know a loop invariant is a statement about a program's variables that is
  true right before a loop starts, stays true after every single time the
  loop body runs, and combines with the loop's exit condition to give the
  postcondition (what is true once the loop is done).
- Know an invariant is not the same as the postcondition: the invariant
  holds at EVERY pass through the loop's checkpoint, while the
  postcondition is only what is true once the loop has exited.
- Know the exit condition itself (the test deciding whether to keep
  looping) is not a fact about the data and is not the invariant -- it is
  the separate ingredient that, combined with the invariant, yields the
  postcondition.
- Be able to spot off-by-one traps in invariant statements, such as
  whether a claimed sorted/summed prefix is `v[0..i-1]` or `v[0..i]`.
- Be able to trace the invariant chain across a shrinking-range algorithm
  (binary search's lo/hi range), a three-region algorithm (a partition
  step), and a mathematical algorithm (Euclid's GCD) that leans on an
  outside number-theory fact rather than pure array bookkeeping.

Concept: the termination variant
- Know a loop terminates if it is guaranteed to eventually stop running
  for any input, and that this is proven informally by naming a variant
  (measure): a quantity computed from the loop's own variables that is
  bounded below by a fixed value the loop cannot go past, and that
  strictly decreases by at least a fixed amount every iteration.
- Know that a strictly decreasing, bounded-below quantity cannot decrease
  forever, which is why finding a valid variant proves termination.
- Know the parity trap: an exit test built on exact equality (`!=`)
  instead of an inequality (`<`, `>=`) can skip past the exact stopping
  value and loop forever (e.g. stepping by 2 toward an odd target).
- Know the unsigned-underflow trap: `i >= 0` on an unsigned loop counter
  can never be false, because decrementing past 0 wraps around to a huge
  positive value instead of going negative -- the loop never terminates
  by that test.
- Know that floating-point rounding error can break an exact-equality
  exit test (e.g. repeatedly adding 0.1 and comparing `== 1.0`), because
  the accumulated value may never land on the exact bit pattern compared
  against.
- Know the Collatz conjecture as a genuine, real example of a loop whose
  termination is mathematically UNPROVEN for all inputs, not merely hard
  to figure out -- the honest verdict for it is "unproven," a legitimate
  fourth answer alongside "always terminates," "can loop forever," and
  "terminates only for some inputs."

## Study checklist

- [ ] State the three-part definition of a loop invariant.
- [ ] Distinguish an invariant from a postcondition and from the exit
      condition itself.
- [ ] Name the invariant for binary search's shrinking range.
- [ ] Define "variant/measure" and explain why decreasing + bounded-below
      proves termination.
- [ ] Explain the unsigned-underflow trap on `i >= 0`.
- [ ] Explain why the Collatz conjecture's termination is unproven, not
      just unsolved by this course.

## Practiced in

`invariant-inspector`, `termination-tribunal`
