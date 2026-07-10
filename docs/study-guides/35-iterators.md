# Study Guide 35: Iterators (traversals)

This module builds the iterator mental model from scratch -- a movable
cursor object, not a language special case -- traces which container
operations invalidate held iterators/pointers/references, and has
students implement a full custom `Iterator`/`ConstIterator` pair on their
own linked list so range-for works on it for free.

## Know before you start

- `std::vector` contiguous storage vs. `std::map`/`std::set` node-based
  storage vs. `std::deque` block-based storage [assumed: row 32 --
  Standard Containers p1; row 33 -- Map & Set ADT]
- The linked list's `Node*` chain, `head_`/`tail_`, and the Big 5 on
  node-owning classes [assumed: row 30 -- Linked List]
- Operator overloading mechanics (`operator*`, `operator++`, `operator==`)
  as ordinary member functions [assumed: row 21 -- OOP Implementation in
  C++]
- References vs. pointers [assumed: row 11 -- Pointers]

## Taught here

Concept: the cursor mental model
- Know that an iterator is a movable cursor object -- a small value that
  points at one element of a container and knows how to move to the next
  one -- and that a `std::vector<int>::iterator` is really just a wrapped
  `int*` under the hood; there is no compiler magic involved.
- Know the five operations: `begin()`/`end()` return cursors; `*it`
  dereferences (reads the pointed-at element); `++it` advances to the next
  element.
- Know `end()` as a fence post: a position one step past the last real
  element, never itself a real element, never safe to dereference, and
  used purely as a loop's stopping signal (`for (auto it = v.begin(); it
  != v.end(); ++it)`).
- Know `rbegin()`/`rend()` as the mirror image, walking backward from the
  last element to one-before-the-first.
- Know map iterators dereference to a pair, accessed via `it->first`
  (key) and `it->second` (value); string iterators walk characters the
  same cursor way.
- Know the safe-erase idiom: `it = container.erase(it);` -- `erase`
  returns a valid iterator to the element that followed the erased one,
  which must be captured back into `it` because the old `it` is now
  invalidated.
- Know `const_iterator` vs. `iterator` is a compile-time distinction (what
  mutation is allowed through it), never something that changes a
  program's printed output.

Concept: range-for's desugaring
- Know that `for (auto& x : container) { body }` is not special-cased by
  the compiler for each type -- it desugars into calling exactly five
  things on the iterator type: `begin()`, `end()`, `operator!=`, prefix
  `operator++`, and `operator*`; implementing those five correctly makes
  range-for work automatically.
- Know prefix `++it` advances the cursor then returns a reference to the
  now-advanced iterator; postfix `it++` must save a copy of the OLD state
  first, advance the real iterator, then return the saved copy -- getting
  this order backwards is a subtle bug invisible at the call site unless
  the return value is actually used.
- Know a singly linked list's node only stores a `next` pointer, so its
  iterator supports only `operator++` (forward), never `operator--`; a
  `prev` pointer (doubly linked) would be required for backward iteration.

Concept: iterator/pointer/reference invalidation
- Know that a held iterator, pointer, or reference into a container is
  only safe to use as long as the container has not moved, reallocated,
  or destroyed the memory it points into.
- Know `std::vector` reallocation (growing past capacity) invalidates
  EVERY iterator, pointer, and reference into the old block; `reserve()`
  up front avoids this up to the reserved capacity.
- Know `std::vector::erase` invalidates iterators at and after the erased
  position, never before it.
- Know `std::map`/`std::set` are node-based: `insert()` invalidates
  nothing; `erase()` invalidates only the erased element's own iterator,
  leaving every other iterator into the map untouched.
- Know `std::deque::push_back`/`push_front` invalidates iterators but NOT
  references or pointers to existing elements -- the one case where those
  two fates split, because of `std::deque`'s block-based internal layout.
- Know that mutating a container's size inside a range-for loop over that
  same container is undefined behavior.

Concept: implementing an iterator from scratch
- Be able to build `Iterator` as a thin wrapper around a single `Node*`,
  implementing `operator*`, `operator->`, prefix `operator++`, postfix
  `operator++(int)`, `operator==`, and `operator!=`.
- Be able to build a parallel `ConstIterator` whose `operator*`/
  `operator->` return `const T&`/`const T*`, exposed via `cbegin()`/
  `cend()`, with `const`-qualified `begin()`/`end()` overloads forwarding
  to them so range-for still works on a `const LinkedList<T>&`.
- Know `end()` for a singly linked list is naturally represented by a
  wrapped `nullptr`, because the last real node's `next` is already
  `nullptr` -- advancing off the end arrives at the same value with no
  special-case bookkeeping.
- Be able to implement `insert_after(pos, value)`/`erase_after(pos)`, the
  natural positional operations for a singly linked list, including their
  documented no-op contracts (`pos == end()`, or nothing after `pos` to
  erase) and correctly updating `tail_` when the affected node is the
  list's last node.

## Study checklist

- [ ] Explain why end() is never dereferenced and why it is a "fence
      post."
- [ ] List the five operations range-for's desugaring actually calls.
- [ ] Explain the order-of-operations difference between prefix and
      postfix ++.
- [ ] For vector/map/deque, name which operations invalidate iterators,
      pointers, and references, including the deque case where they
      split.
- [ ] Use the safe-erase idiom to erase while iterating.
- [ ] Explain why a singly linked list's iterator has no operator--.

## Practiced in

`iterator-walk`, `invalidation-minefield`, `linked-list-iterators`
