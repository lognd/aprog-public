# Activity: Ring Buffer Rehearsal

A **circular buffer** (also called a **ring buffer**) is the trick that
lets a fixed-size array support O(1) insertion and removal at BOTH ends,
which is exactly what the `ArrayDeque<T>` in the `deque-two-ways`
assignment is built on. Instead of always treating index 0 as "the front"
(which would force every removal from the front to shift every remaining
element left by one slot -- an O(n) operation), a circular buffer lets the
logical front live at any index, tracked by a `head_` variable, and treats
the array as wrapping around: the slot "after" the last physical index is
index 0 again, the same way a clock face wraps from 12 back to 1.

This activity has no code to write and nothing to compile. You trace, by
hand, a single capacity-8 circular buffer through a sequence of
`push_back`/`pop_front` operations, computing exactly what a correct
`ArrayDeque<T>` implementation would compute at each step: which physical
index a push writes to, where `head_` ends up after a run of pops, how
many elements are stored, and what happens to the buffer's contents when
it fills up and has to grow. If you can answer every question in this
activity correctly, you understand the exact mental model you need to
implement `ArrayDeque<T>` in `deque-two-ways`.

---

## Background

### head_, size_, and capacity_

A circular buffer tracks three numbers alongside its underlying array:

- `capacity_` -- the total number of physical slots in the array (fixed
  until a grow happens).
- `head_` -- the physical array index of the current LOGICAL front
  element.
- `size_` -- how many elements are currently stored (not the same thing as
  `capacity_` -- most of the array can be empty).

The logical front-to-back order of elements is: the element at `head_`,
then the element at `(head_ + 1) % capacity_`, then
`(head_ + 2) % capacity_`, and so on for `size_` elements total. Note that
none of these depend on where index 0 physically is -- `head_` can be any
valid index, and the buffer's logical front-to-back order still makes
sense by walking forward from `head_` and wrapping via modulo.

### The modulo operator as "wraparound"

`a % b` (read "a modulo b" or "a mod b") gives the remainder when `a` is
divided by `b`. For any non-negative `a`, `a % b` always lands in the
range `[0, b)` -- it never returns `b` or anything larger. That is exactly
the property a circular buffer needs: no matter how large a raw index
computation gets (`head_ + size_`, or `head_ - 1`, computed as if the
array went on forever), taking the result `% capacity_` folds it back into
a valid physical slot.

Worked example: `capacity_ = 8`, `head_ = 5`, `size_ = 7`. Where does the
NEXT `push_back` write? Compute `head_ + size_ = 5 + 7 = 12`. There is no
physical index 12 in an 8-slot array. `12 % 8 = 4` (12 divided by 8 is 1
remainder 4) -- so the write lands at physical index 4, having wrapped
around past index 7 and back through index 0, 1, 2, 3.

### Two directions of wraparound

Growing the occupied region past the end of the array (via `push_back`)
wraps FORWARD: `(head_ + size_) % capacity_`. Growing it past the
BEGINNING of the array (via `push_front`, which has to place a new element
immediately before the current `head_`) wraps BACKWARD, and needs a small
trick because `head_` is an unsigned index: instead of computing
`head_ - 1` directly (which underflows to a huge number if `head_` is
already 0), the safe computation is `(head_ + capacity_ - 1) % capacity_`
-- adding `capacity_` first guarantees the subtraction never goes negative
before the modulo folds it back into range.

---

## Concepts covered

- The `head_`/`size_`/`capacity_` circular-buffer mental model
- Modulo arithmetic as the mechanism behind array "wraparound"
- Computing the next write index for `push_back` and `push_front`
- Tracking `head_` through a sequence of `pop_front` calls
- Recognizing when a buffer is full versus over capacity
- Grow-and-re-linearize: why growth must preserve logical order even
  when the buffer was wrapped at the moment it grew

---

## How it works

This activity shows nine questions, each continuing the same rehearsal
from where the previous one left off: a capacity-8 circular buffer starts
empty, and a sequence of `push_back`/`pop_front` calls (plus one grow) runs
against it. Each question's code block shows the buffer's state and the
operations that just ran, using the exact same `(head_ + size_) %
capacity_` and `(head_ + 1) % capacity_` formulas a correct `ArrayDeque<T>`
implementation uses. You answer with a single integer for most questions
(an index or a count), and with a comma-separated list of letters for the
final question, exactly as each prompt specifies. Wrong answers are
explained in detail before you try again; correct answers unlock a full
explanation and move you to the next question. All nine questions must be
answered correctly to receive the passphrase.

---

## Getting started

```bash
python3 launch.py
```

---

## You will know you are done when...

The launcher prints the passphrase after all nine questions in the
rehearsal have been answered correctly.

---

## Hints

<details>
<summary>Hint 1 -- write index versus head_ are different formulas</summary>

The next `push_back` write index is `(head_ + size_) % capacity_`. `head_`
itself only changes when a `pop_front` or `push_front` runs. Do not
confuse "where the next element goes" with "where the front element
currently is" -- they are two different quantities that happen to use the
same modulo trick.

</details>

<details>
<summary>Hint 2 -- always compute the raw sum first, then take modulo</summary>

For every index computation in this activity, first add up the raw
numbers as if the array had no size limit at all (`head_ + size_`, or
`head_ + capacity_ - 1`), and only THEN take that result `% capacity_`.
Trying to reason about wraparound in your head without doing this two-step
process is the most common source of off-by-one mistakes.

</details>

<details>
<summary>Hint 3 -- re-linearization preserves logical order, not physical position</summary>

When a grow happens, the elements are copied out in their LOGICAL
front-to-back order (starting from the old `head_`, wrapping as needed)
and written into the new array starting fresh at index 0. Physical
positions from before the grow do not matter afterward -- only the
front-to-back sequence of surviving elements does.

</details>

---

## Going further

- Work through the same rehearsal again, but this time also trace what a
  `push_front` (instead of `push_back`) does to `head_` at each wrap point,
  using `(head_ + capacity_ - 1) % capacity_`.
- Once you have implemented `ArrayDeque<T>` in the `deque-two-ways`
  assignment, add a temporary debug `print` inside `push_back` and
  `pop_front` that prints `head_`, `size_`, and the computed write/read
  index on every call, then re-run this activity's exact operation
  sequence against your real implementation and confirm every number
  matches what you traced by hand here.
- Look up how `std::deque`'s real block-map implementation avoids ever
  needing a full re-linearizing grow at all. What does it do instead when
  it runs out of room at one end?
