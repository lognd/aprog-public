# Activity: Index vs. Node

"O(n)" and "O(1)" describe how cost SCALES, but they can make two very
different structures look interchangeable at a glance. This activity makes
the cost of dynamic-array and linked-list operations concrete. A dynamic
array stores elements back to back in one block of memory and reaches any
element directly by index; a linked list stores each element in its own
**node** (a small block holding one value plus a pointer to the next node)
and can only be reached by starting at the first node (`head`) and
following those pointers one at a time. A **shift** is one element moving
to a different index inside the array (to open up or close a gap); a
**pointer hop** is one `->next` step taken while walking a linked list.
Given an exact sequence of elements and an exact operation, you compute
the exact number of shifts, hops, or resulting size/capacity -- numbers
you can count on your fingers, not just complexity classes.

## Concepts covered

- Counting exactly how many elements a dynamic array shifts on insert/erase
- Counting exactly how many pointer hops a linked-list traversal or
  insertion requires to reach a given index
- Contrasting O(1) index arithmetic (dynamic array) with O(n) sequential
  pointer-chasing (linked list) using real numbers instead of just symbols
- Amortized growth (a single expensive operation's cost spread out over
  many cheap ones that come after it): tracing a dynamic array's
  capacity-doubling sequence to compute its exact size and capacity after
  a run of `push_back` calls

## How it works

Each of the eight questions shows a short code comment illustrating a
concrete operation sequence -- for example, `insert(2, 99)` on a five-element
array, or reaching index 4 of a linked list from `head`. You answer with an
exact number (the prompt tells you the expected answer format each time).
Answering correctly reveals an explanation that walks through the count
step by step; answering incorrectly shows the reasoning behind the most
common miscounts. Answer every question correctly to reveal the passphrase.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have answered all eight questions correctly and the launcher prints
the activity's passphrase.

## Hints

<details>
<summary>Hint 1 -- draw the array or list on paper</summary>

For any shift-counting question, write out the array's indices before and
after the operation and circle which elements changed position. For any
hop-counting question, draw the chain of nodes and count arrows from head
to the target.

</details>

<details>
<summary>Hint 2 -- capacity growth is a separate trace from size</summary>

Size just counts how many elements have actually been pushed. Capacity
only changes on a push that happens while the array is already full --
track size and capacity as two separate running numbers, updating capacity
only when size would exceed it.

</details>

## Going further

- Generalize: write the formula for how many elements `insert(index, ...)`
  shifts in an array of size `n`, and the formula for how many hops
  `insert_at(index, ...)` costs in a linked list. When do the two formulas
  agree, and when do they diverge the most?
- Trace capacity growth starting from an empty array through 20
  `push_back` calls. How many reallocations happen in total, and how does
  that compare to 20 (the number of pushes)?
- Implement a tiny dynamic array yourself (a fixed-size heap buffer that
  doubles when full) and print its size and capacity after every push to
  confirm your traced numbers match.
