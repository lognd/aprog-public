# Activity: Adaptor Roundup

A **container adaptor** does not store elements itself and does not
implement its own algorithms -- it wraps an existing container (its
"underlying container") and exposes a narrower, purpose-built interface on
top of it. `std::stack`, `std::queue`, and `std::priority_queue` are the
three standard adaptors. This activity is a round of scenario trials: for
each workload, decide which adaptor fits -- or whether the honest answer
is "none of them, use a plain `std::vector`" -- and why.

## Background

`std::stack` gives last-in-first-out (LIFO) access: only the most recently
pushed element is reachable, through `top()`. `std::queue` gives
first-in-first-out (FIFO) access: only the oldest still-waiting element is
reachable, through `front()`. `std::priority_queue` always keeps the
current highest-priority element reachable through `top()`, regardless of
insertion order, by maintaining a **heap** internally.

None of the three expose `begin()`/`end()` -- that narrow interface is the
entire point of an adaptor. If a workload's core requirement is "walk
every element," none of the three adaptors can do that; you need a
container that actually supports iteration.

## Concepts covered

- What a container adaptor is, and why its interface is deliberately narrow
- `std::stack` (LIFO) vs `std::queue` (FIFO) vs `std::priority_queue`
  (highest-priority-first)
- The heap property: a parent is never lower priority than its children
  (a partial order, not a full sort)
- Recognizing the "need to iterate" trap: none of the three adaptors
  support it
- The min-heap-for-top-k technique, and why the smallest of the kept
  elements is the one you need fast access to
- What underlying container each adaptor defaults to, and why

## How it works

Each question describes a workload or asks a direct question about
adaptor behavior. Type the exact answer requested by the prompt (a
container name, or one of the listed phrases). Getting a question wrong
shows a detailed explanation of the tradeoff or mechanism you missed;
answer every question correctly to reveal the passphrase.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have answered every scenario correctly and the launcher prints the
passphrase.
