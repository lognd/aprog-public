# Activity: Multi-Court

`std::multiset`, `std::multimap`, and `std::priority_queue` are on trial.
`std::multiset` and `std::multimap` are the duplicate-allowing siblings of
`std::set` and `std::map`: they never reject a key just because it is
already present. `std::priority_queue` always pops in a fully
deterministic order, driven by a max-heap by default. Every snippet here
traces exactly how duplicates are counted, sized, iterated, and popped --
compile and run each one to check your prediction.

## Background

`std::set`/`std::map` silently reject a second `insert()` with an
already-present key. `std::multiset`/`std::multimap` never do -- every
`insert()` call actually adds a new element, duplicates included, so
`size()` grows every time. `count(key)` on a multi- container can return
any nonnegative number (not just 0 or 1), reporting exactly how many
stored elements share that key. Both are still backed by the same balanced
tree as their non-multi siblings, so iteration still visits elements in
ascending sorted-key order -- duplicates just sort next to each other.

## Concepts covered

- `std::multiset`/`std::multimap` allow duplicate keys; `std::set`/`std::map` do not
- `count()` on a multi- container reports how many elements share a key,
  not just presence
- Multi- containers still iterate in sorted key order
- `erase(key)` on a multi- container removes every matching element at
  once and returns the count removed
- `std::priority_queue`'s deterministic max-heap pop order
- `std::pair`'s lexicographic comparison, and how it drives
  `priority_queue<pair<...>>` ordering

## How it works

Each snippet shows a short C++ program. Predict its exact output, then the
launcher compiles and runs it with g++ to check your answer. Getting a
snippet wrong shows a detailed explanation of the container behavior you
missed; predict every snippet correctly to reveal the passphrase.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly predicted the output of every snippet and the launcher
prints the passphrase.
