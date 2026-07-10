# Activity: Iterator Walk

An **iterator** is a movable cursor object -- a small value that points at
one element of a container and knows how to move to the next one, without
exposing the container's internal layout. This activity builds the core
iterator mental model from scratch, one snippet at a time:
`begin()`/`end()`, dereferencing with `*it`, advancing with `++it`, the
"fence post" picture of `end()` as one-past-the-last-element, reverse
iteration, map iterators, string iterators, and the safe-erase idiom.

## Background

`v.begin()` returns a cursor pointing at a container's first element.
`*it` dereferences that cursor, reading the element it currently points
at. `++it` advances the cursor to the next element. `v.end()` is a
**fence post**: a position one step past the last real element, never
itself a real element and never meant to be dereferenced -- it exists
purely as a stopping signal for loops like `for (auto it = v.begin(); it
!= v.end(); ++it)`. `rbegin()`/`rend()` are the mirror image, walking
backward from the last element to one-before-the-first.

## Concepts covered

- The cursor mental model: `begin()`/`end()`, `*it`, `++it`
- `end()` as a one-past-the-last fence post, never dereferenced
- Random-access iterators (`it + n`, `std::distance`) vs. one-step-at-a-time
  iterators
- Reverse iteration with `rbegin()`/`rend()`
- Map iterators (`it->first`, `it->second`) and string iterators
- The safe-erase idiom: `it = container.erase(it);`
- `const_iterator` vs. `iterator` (a compile-time distinction, not an
  output-observable one)

## How it works

Each snippet shows a short C++ program. Predict its exact output, then the
launcher compiles and runs it with g++ to check your answer. Getting a
snippet wrong shows a detailed explanation of the iterator mechanics you
missed; predict every snippet correctly to reveal the passphrase.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly predicted the output of every snippet and the launcher
prints the passphrase.
