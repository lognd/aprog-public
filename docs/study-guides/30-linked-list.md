# Study Guide 30: Linked List (operations, build your own)

This module works with raw `Node*` chains directly: tracing splices,
reversals, and broken relinks by hand, then implementing a full templated
singly linked list with the complete Big 5, O(1) `push_back` and `size()`,
graded under both ASan and Valgrind.

## Know before you start

- Array-vs-list cost model and pointer-hop counting [assumed: row 29 --
  List ADT & Supporting DS]
- The Big Five, deep vs. shallow copy, move semantics, and self-assignment
  guards [assumed: row 25 -- Dynamic Memory]
- Use-after-free and double-delete as bug classes, and reading ASan/
  Valgrind reports [assumed: row 26 -- Memory & Profiling Tools]
- `new`/`delete` pairing on heap nodes [assumed: row 10 -- Memory Model]
- Class templates as used in generic containers [assumed: row 23 --
  Polymorphism]

## Taught here

Concept: the node/next-pointer chain
- Know that a singly linked list is a chain of separately heap-allocated
  nodes (`T data; Node* next;`), where `head_` points at the first node
  and the last node's `next` is `nullptr` -- the traversal terminator.
- Know that reaching position k requires following `next` k times from
  `head_` (no index arithmetic exists), and that keeping a `tail_`
  pointer is what makes `push_back` O(1) instead of a full walk.
- Be able to trace the classic manipulations by drawing the chain and
  redrawing arrows after every pointer-touching line: `push_front`,
  `insert_after` (link the new node in without losing the rest of the
  chain), and relinking around a removed node without leaking it or
  reading freed memory.
- Be able to reverse a list in place with three pointers (`prev`, `cur`,
  `next`) in O(1) extra space.
- Know the slow/fast pointer ("tortoise and hare") technique for finding
  the middle of a list in one pass, and that the same technique detects
  cycles.
- Be able to diagnose a broken relink: overwriting or deleting a pointer
  before something downstream has read its old value makes a node
  unreachable (a leak) or the traversal read freed memory.

Concept: why this module uses raw pointers deliberately
- Know that wrapping `next` in a smart pointer would make destruction
  recursive -- destroying the head destroys its next, which destroys its
  next, one call-stack frame per node -- risking stack overflow on long
  lists; an explicit delete loop avoids this.
- Know that manual `new`/`delete` here is intentional pedagogy (this is
  how `std::list` is built underneath), with the obligation that every
  `new` is matched by exactly one `delete` on every code path.

Concept: the Big 5 for a multi-node structure
- Know that a compiler-generated (shallow) copy of a list copies only the
  `head_` pointer, leaving two lists sharing one chain -- destroying
  either double-deletes the other's nodes; a correct copy constructor
  walks the source and allocates a brand-new node per element so the two
  lists are fully independent.
- Know that move construction/assignment steals the entire chain in O(1)
  by transferring three members (`head_`, `tail_`, `size_`) and resetting
  the source to a valid empty state (`nullptr`, `nullptr`, 0) that is
  both safe to destroy and safe to keep using.
- Know the delete-order trap in `clear()`/destructor/`remove_at`: `delete
  cur; cur = cur->next;` is a use-after-free -- the fix is saving `next`
  before deleting, then advancing via the saved pointer.
- Know the no-exceptions error contract used here: out-of-range
  `insert_at`/`remove_at` return `false` and do nothing instead of
  throwing, with `insert_at` valid on `[0, size()]` (appending at
  `size()`) and `remove_at` valid on `[0, size())`.
- Know the performance contract: `size()` must be O(1) by maintaining a
  running count, and `push_back` must be O(1) via `tail_` -- a walking
  implementation is wrong even when its answers are right.
- Know that memory-safety grading runs the same tests under both Valgrind
  and ASan, because correctness assertions alone cannot catch leaks,
  double-deletes, or use-after-free.

## Study checklist

- [ ] Trace a `delete_middle` relink and state which pointer must be read
      before which delete.
- [ ] Write the three-pointer reverse loop from memory.
- [ ] Explain why `Node::next` as a `unique_ptr` risks stack overflow.
- [ ] Explain what a shallow-copied list does when both copies are
      destroyed.
- [ ] State what move assignment transfers and what state the source must
      be left in.
- [ ] Spot the use-after-free in the naive `clear()` loop and fix it.

## Practiced in

`link-tracer`, `linked-list-from-scratch`
