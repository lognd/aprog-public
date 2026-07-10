# Study Guide 32: Standard Containers p1

`std::vector` and `std::array` were already covered at row 7 -- this
module's job is the two containers that are NEW here: `std::list` (doubly
linked, the standard-library sibling of the linked list you built by hand
at row 30) and `std::forward_list` (singly linked, one pointer per node).
It puts the container-cost intuition built by hand-rolling a dynamic array,
a circular buffer, and a linked list to work choosing between all five
standard sequence containers, weighted toward `std::list`'s splice and
iterator-stability strengths and `std::forward_list`'s frugal, forward-only
design -- with an honest recap of where `std::list` still loses.

## Know before you start

- The array-vs-linked-list cost profile (random access, front insertion,
  splicing) [assumed: row 29 -- List ADT & Supporting DS]
- Your own hand-rolled singly linked list and its `insert_after`-shaped
  positional operations [assumed: row 30 -- Linked List ADT]
- The deque ADT and the circular-buffer implementation backing
  `std::deque` [assumed: row 31 -- Stack, Queue, Deque (ADT)]
- `std::vector`'s heap growth versus `std::array`'s fixed compile-time
  size, and `std::vector`'s size-versus-capacity bookkeeping under the
  standard's actual guarantees [assumed: row 7 -- Standard Library Types]
- Amortized O(1) `push_back` via capacity doubling [assumed: row 28 --
  Complexity Theory]

## Taught here

Concept: std::list -- splice and iterator stability
- Know that `std::list::splice` moves a run of nodes from one list (or one
  position within a list) to another by relinking a small, fixed number of
  `next`/`prev` pointers, copying zero element data, in O(1) -- this is
  `std::list`'s headline advantage over every array-backed container,
  which must shift or copy O(n) element data to do the same job.
- Know that inserting or erasing ANYWHERE in a `std::list` never
  invalidates an iterator, pointer, or reference to any OTHER element --
  only an iterator to the element actually erased becomes invalid. This is
  a separate guarantee from splicing: it is about node stability under
  unrelated edits, not about moving nodes between containers. (A later
  unit on iterators formalizes exactly which operation invalidates which
  container's iterators, scenario by scenario -- this module states
  `std::list`'s piece of that picture in its own terms, ahead of that
  formal treatment.)
- Know the member functions that exist on `std::list` specifically because
  its node layout makes them cheap: `sort()` (a node-relinking merge sort
  -- the free `std::sort` cannot be used on `std::list` at all, because it
  needs random-access iterators that a linked list does not have),
  `remove(value)` (unlinks every matching node), and `unique()` (collapses
  runs of CONSECUTIVE equal elements, not global duplicates).

Concept: std::forward_list -- the frugal, forward-only option
- Know that `std::forward_list` stores only a `next` pointer per node
  (versus `std::list`'s `next` AND `prev`), trading away backward
  traversal for a smaller per-node footprint -- reach for it when a
  workload only ever walks forward and per-node memory actually matters.
- Know that `std::forward_list` has NO `size()` member at all, on purpose:
  it refuses to pay to maintain a running count that a forward-only
  workload might never ask for. Getting a count when you do need one costs
  an explicit O(n) walk, `std::distance(begin(), end())`.
- Know `std::forward_list`'s positional API, `before_begin()` +
  `insert_after(pos, value)` -- the same shape you already built by hand
  for your own singly linked list, and for the same underlying reason: a
  singly linked node has no way to reach the node before it, so every
  positional operation is phrased in terms of "after a position you
  already have," never "before" or "at."

Concept: choosing a sequence container (five now, not four)
- Know that `std::vector` remains the correct default sequence container
  -- reach for it first, and only move to another container when a
  scenario states a specific requirement it cannot meet. That has not
  changed since row 7; this module is about recognizing the cases that DO
  point elsewhere.
- Know that `std::array` fits only when the element count is a true
  compile-time constant (row 7 material, mentioned here for completeness).
- Know that `std::deque` fits workloads needing fast, stable O(1)
  insertion/removal at BOTH the front and the back, and that it is NOT one
  contiguous block of memory -- it is internally a map (index) of
  separately allocated fixed-size blocks, which is exactly what lets it
  grow at either end without moving existing elements.
- Know the honest case where `std::list` still loses despite a real
  splicing need: a hot loop that reads/mutates every element far more
  often than it splices pays `std::list`'s cache-locality cost (pointer-
  chasing, no contiguous storage) on every one of those far-more-frequent
  accesses -- weigh a rare convenience against an extreme cost by how
  often each actually happens, not by which sounds more sophisticated
  (callback to the list-tradeoff-tribunal activity's benchmark, row 29).
- Be able to reason through the decision in order: is the size a
  compile-time constant (`std::array`)? Does it need fast front-insertion
  plus index access (`std::deque`)? Does it need cheap splicing or
  survive-unrelated-edits iterator stability, with a hot loop that does
  NOT dominate (`std::list`)? Is it forward-only, no-`size()`-needed, and
  memory-constrained (`std::forward_list`)? Otherwise, `std::vector`.

## Study checklist

- [ ] Given a workload description, pick vector, deque, list,
      forward_list, or array and justify it by the one requirement that
      rules out the others.
- [ ] Explain what `splice` actually moves and why it is O(1) regardless
      of how many elements move.
- [ ] Explain why an iterator held into a `std::list` element survives a
      splice of that element into a different list.
- [ ] Explain why `std::sort` cannot be called on a `std::list`, and what
      `std::list::sort()` does instead.
- [ ] Explain the difference between `remove()` (every matching element)
      and `unique()` (only consecutive runs).
- [ ] Explain why `std::forward_list` has no `size()` member and how to
      get a count anyway.
- [ ] Explain what `before_begin()` is for and why `insert_after`, not
      `insert`, is `std::forward_list`'s positional operation.
- [ ] Explain what `std::deque` actually stores internally and why that
      design gives O(1) at both ends.
- [ ] Given a workload with both a real splicing need and a dominant hot
      loop, explain why `std::list` can still be the wrong answer.

## Practiced in

`container-casting-call`, `splice-circus`
