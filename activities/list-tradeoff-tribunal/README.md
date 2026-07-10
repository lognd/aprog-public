# Activity: List Tradeoff Tribunal

`std::vector` (a dynamic array) and a hand-built linked list can both hold
the same sequence of values, in the same order, and offer many of the same
operations by name. Yet in practice, choosing between them for a given job
can mean the difference between a program that scales fine and one that
grinds to a halt. This activity puts a series of concrete requirement
scenarios "on trial": for each one, you decide which backing structure --
dynamic array, linked list, or either works about equally well -- actually
fits the job, and why.

## Background

An ADT (Abstract Data Type) is a description of a data structure's
behavior: a set of operations and the contract each one honors, with no
mention of how those operations are actually carried out underneath. "A
List ADT supports insert(index, value), remove(index), get(index), and
size()" is a complete ADT description -- it says nothing about contiguous
memory or linked nodes. A dynamic array and a linked list are both
IMPLEMENTATIONS of a similar List ADT: they honor a similar contract, but
the mechanics underneath (one contiguous block of memory, versus a chain of
separately allocated nodes each pointing to the next) are completely
different, and that difference is exactly why the same abstract operation
can have wildly different real-world cost depending on which one backs it.

## Concepts covered

- The distinction between an ADT (the operations contract) and a concrete
  implementation (how those operations are carried out)
- Cache locality: why contiguous memory is faster to iterate over on real
  hardware than scattered, pointer-linked memory
- Front-insertion cost: O(n) shifting for a dynamic array vs. O(1)
  relinking for a linked list
- Random-access cost: O(1) address arithmetic for a dynamic array vs. O(n)
  pointer-chasing for a linked list
- Splicing: why rearranging pointers (linked list) can beat moving data
  (dynamic array) for cut-and-reinsert workloads
- The practical reality that dynamic arrays often beat linked lists even
  where a linked list's Big-O looks better on paper

## How it works

The activity presents nine questions, each describing a usage scenario (no
code -- pure reasoning). For each one you type your answer exactly as
prompted -- usually one of `dynamic array`, `linked list`, or `either
works`, though a couple of questions ask for a specific term or `true`/
`false`. Every question also carries an explanation, shown once you answer
correctly, that walks through the reasoning from first principles. Answer
every question correctly to reveal the activity's passphrase.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have answered all nine questions correctly and the launcher prints the
activity's passphrase.

## Hints

<details>
<summary>Hint 1 -- what actually moves versus what actually gets touched</summary>

For any "which structure wins" question, ask yourself concretely: what
physical work does each structure have to do for this specific operation?
Does it copy/shift existing element DATA, or does it just repoint a
pointer? Data movement scales with how many elements are affected; pointer
repointing does not.

</details>

<details>
<summary>Hint 2 -- Big-O is not the whole story</summary>

A couple of questions ask about real hardware performance, not just
asymptotic complexity. Two operations can both be "O(n)" and still differ
by a large constant factor in wall-clock time -- cache locality is exactly
that kind of constant-factor effect.

</details>

## Going further

- Write a small benchmark that pushes 100,000 integers into a
  `std::vector<int>` and into a hand-rolled linked list, then times a full
  forward iteration over each. How large is the gap, and does it match
  your intuition from this activity?
- Look up `std::deque` (double-ended queue) and figure out how it achieves
  fast insertion at both ends without either shifting a full array or
  paying a per-element heap allocation like a linked list does.
- Pick one "either works" scenario from this activity and change one
  detail of it (for example, make index-based reads frequent instead of
  rare) so that it clearly tips toward one structure. What did you change,
  and why does it matter?
