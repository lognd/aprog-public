# Study Guide 34: Standard Containers p2

This module covers container adaptors (`std::stack`, `std::queue`,
`std::priority_queue`) -- narrow interfaces wrapping an underlying
container -- and the duplicate-allowing associative siblings
`std::multiset`/`std::multimap`.

## Know before you start

- The Stack/Queue/Deque ADTs and the adapter pattern [assumed: row 31 --
  Stack, Queue, Deque (ADT)]
- `std::set`/`std::map`'s balanced-tree sorted iteration and unique-key
  rejection [assumed: row 33 -- Map & Set ADT]
- `std::vector`/`std::deque` as underlying storage [assumed: row 32 --
  Standard Containers p1]

## Taught here

Concept: container adaptors
- Know that a container adaptor does not store elements itself or
  implement its own algorithms -- it wraps an underlying container and
  exposes a narrower, purpose-built interface on top of it.
- Know `std::stack` gives LIFO access only (`top()` reaches the most
  recently pushed element); `std::queue` gives FIFO access only (`front()`
  reaches the oldest still-waiting element); `std::priority_queue` always
  keeps the current highest-priority element reachable through `top()`,
  regardless of insertion order.
- Know that none of the three adaptors expose `begin()`/`end()` -- that
  narrow interface is the entire point of an adaptor, so "I need to walk
  every element" is a hard signal that no adaptor fits and a real
  container (usually `std::vector`) is needed instead.
- Know the heap property: a parent is never lower priority than either of
  its children -- a partial order maintained internally by
  `std::priority_queue`, not a full sort of all elements.
- Know the min-heap-for-top-k technique: keeping a bounded set of the k
  best-so-far elements needs fast access to the SMALLEST of the kept
  elements (to evict it when a better candidate arrives), which is exactly
  what a min-heap's `top()` gives.

Concept: multiset and multimap
- Know that `std::set`/`std::map` silently reject a second `insert()` with
  an already-present key; `std::multiset`/`std::multimap` never do --
  every `insert()` actually adds a new element, duplicates included, and
  `size()` grows every time.
- Know that `count(key)` on a multi- container can return any nonnegative
  number (not just 0 or 1), reporting exactly how many stored elements
  share that key.
- Know that multi- containers are still backed by the same balanced tree
  as their non-multi siblings, so iteration still visits elements in
  ascending sorted-key order, with duplicates sorting next to each other.
- Know that `erase(key)` on a multi- container removes EVERY matching
  element at once and returns the count removed (not just one).

Concept: priority_queue's deterministic pop order
- Know that `std::priority_queue` pops in a fully deterministic order
  driven by a max-heap by default (largest element first).
- Know that `std::pair`'s comparison is lexicographic (first element
  compared first, second element only breaks ties), and that this is
  exactly what drives ordering in a `priority_queue<pair<...>>`.

## Study checklist

- [ ] Given a workload, decide stack, queue, priority_queue, or "none of
      them, use a vector."
- [ ] Explain why none of the three adaptors can support iteration.
- [ ] Explain the min-heap-for-top-k technique.
- [ ] Predict size()/count() after a sequence of multiset/multimap
      insert() and erase(key) calls.
- [ ] Predict the pop order of a priority_queue<std::pair<...>>.

## Practiced in

`adaptor-roundup`, `multi-court`
