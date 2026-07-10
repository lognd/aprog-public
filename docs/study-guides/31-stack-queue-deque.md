# Study Guide 31: Stack, Queue, Deque (ADT)

This module builds the deque ADT twice -- as a circular-buffer array and as
a doubly linked list -- and then derives Stack and Queue as thin adapters
over it, the same way the C++ standard library does. The ring-buffer
activity rehearses the exact head/size/modulo arithmetic the array backend
needs, with a performance test enforcing O(1) `pop_front`.

## Know before you start

- The ADT/implementation distinction and the array-vs-list cost model
  [assumed: row 29 -- List ADT & Supporting DS]
- Doubly/singly linked node chains, the delete-order trap, and the Big 5
  on node-based structures [assumed: row 30 -- Linked List]
- Amortized O(1) growth by capacity doubling [assumed: row 28 --
  Complexity Theory]
- The adapter pattern (a wrapper exposing a smaller, renamed subset of
  another class's operations) [assumed: row 24 -- Design Patterns]
- Cache locality of contiguous storage [assumed: row 19 -- Structs (DOD &
  OOP intro)]

## Taught here

Concept: the deque ADT
- Know that a deque ("deck", double-ended queue) is an ADT supporting
  insertion and removal at BOTH ends in O(1): `push_front`/`push_back`,
  `pop_front`/`pop_back`, `front()`/`back()`, `size()`/`empty()` -- and
  that all six end operations being O(1) is the deque's defining promise.
- Know why the naive array (index 0 always the front) fails: `pop_front`
  must shift every remaining element left, an O(n) operation that a
  performance test can and does catch.

Concept: the circular buffer
- Know the three bookkeeping numbers: `capacity_` (physical slots),
  `head_` (physical index of the logical front), and `size_` (elements
  currently stored -- not the same as capacity).
- Know that logical front-to-back order is `head_`, `(head_ + 1) %
  capacity_`, `(head_ + 2) % capacity_`, ... for `size_` elements --
  independent of where physical index 0 is.
- Know that `a % b` folds any raw index into `[0, b)`, which is exactly
  the wraparound a fixed array needs: compute the raw sum first (`head_ +
  size_`), then take it `% capacity_` -- e.g. capacity 8, head 5, size 7
  puts the next `push_back` at (5+7) % 8 = 4.
- Know the two wrap directions: `push_back` wraps forward via `(head_ +
  size_) % capacity_`; `push_front` wraps backward via `(head_ +
  capacity_ - 1) % capacity_` -- adding `capacity_` first prevents
  unsigned underflow when `head_` is 0.
- Know that the next-write index and `head_` are different quantities:
  `head_` only moves on `pop_front`/`push_front`.
- Know grow-and-re-linearize: when a full buffer doubles, elements must be
  copied out in LOGICAL order (starting at the old `head_`, wrapping) into
  the new array starting at index 0, resetting `head_` to 0 -- a
  byte-for-byte physical copy of a wrapped buffer scrambles the order.

Concept: two backends, one contract
- Know that `ArrayDeque<T>` (contiguous, cache-friendly, occasional O(n)
  grow that amortizes to O(1) per push) and `ListDeque<T>` (doubly linked
  nodes, no bulk grow ever, but poor locality and per-node pointer
  overhead) satisfy the same deque ADT with the same asymptotic costs --
  the choice is an engineering trade-off, not a correctness question.
- Be able to implement the Big 5 for an owned raw array (a second kind of
  owned resource, different from a node chain) and for a doubly linked
  list backend.
- Know the bool-return, no-exceptions contract carried over from the
  linked-list assignment: pops on an empty container return `false` and
  do nothing; `front()`/`back()` are only called on non-empty containers.

Concept: Stack and Queue as adapters
- Know that `Stack<T>` (LIFO: push and pop at the SAME end) delegates
  `push` -> `push_back`, `pop` -> `pop_back`, `top` -> `back`; and
  `Queue<T>` (FIFO: push at one end, pop at the other) delegates `push` ->
  `push_back`, `pop` -> `pop_front`.
- Know that neither adapter is a new data structure: each holds a deque
  backend as a private member and exposes a restricted, renamed view --
  exactly how `std::stack` and `std::queue` wrap `std::deque` by default.
- Know the template shape `Stack<T, D = ArrayDeque<T>>`: the backend is a
  template parameter with a default, so swapping in `ListDeque<int>`
  requires no other code changes.

## Study checklist

- [ ] State the deque ADT's six end operations and its defining O(1)
      promise.
- [ ] Explain why the naive front-at-index-0 array makes `pop_front` O(n).
- [ ] Compute the next `push_back` index for capacity 8, head 5, size 7.
- [ ] Write the safe backward-wrap formula for `push_front` and explain
      the underflow it avoids.
- [ ] Explain why grow must re-linearize instead of copying physical
      slots.
- [ ] Map Stack and Queue operations onto their deque delegates.

## Practiced in

`ring-buffer-rehearsal`, `deque-two-ways`
