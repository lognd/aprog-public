# Activity: Invalidation Minefield

An iterator, pointer, or reference into a container is only safe to use as
long as the container has not done something that moves, reallocates, or
destroys the memory it points into. This activity puts eight scenarios on
trial: given code that holds an iterator/pointer/reference into a
container and then performs some operation, decide whether it is still
valid afterward, or has been invalidated -- meaning using it afterward is
undefined behavior. Every explanation teaches WHY, starting from the
container's actual memory layout.

## Background

`std::vector` stores its elements in one contiguous block of heap memory.
Growing past capacity forces a brand-new, larger block, with every element
copied or moved into it and the old block freed -- invalidating every
iterator, pointer, and reference into the old block. `std::map` (and
`std::set`) are node-based: every key-value pair lives in its own
separately heap-allocated node, connected by pointers into a balanced
tree. Inserting or erasing one key only touches that one node's memory,
leaving every other iterator into the map completely unaffected.
`std::deque` splits the difference: it is a sequence of separately
allocated fixed-size blocks, so `push_back`/`push_front` never invalidates
references or pointers to existing elements, but it can still invalidate
iterators.

## Concepts covered

- `std::vector` reallocation invalidates everything into it; `reserve()`
  avoids it up to the reserved capacity
- `std::vector::erase` invalidates iterators at and after the erased
  position, never before it
- `std::map`/`std::set` are node-based: `insert()` invalidates nothing;
  `erase()` invalidates only the erased element's iterator
- `std::deque::push_back` invalidates iterators but not references or
  pointers -- the one case where those two fates split
- Why mutating a container's size inside a range-for loop over that same
  container is undefined behavior

## How it works

Each question shows a short code snippet holding an iterator, pointer, or
reference into a container, followed by an operation on that container.
Decide the verdict: still valid, or invalidated. Getting a question wrong
shows a detailed explanation of the memory layout that determines the
answer; answer every question correctly to reveal the passphrase.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have answered every scenario correctly and the launcher prints the
passphrase.
