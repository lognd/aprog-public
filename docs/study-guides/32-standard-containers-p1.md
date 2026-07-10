# Study Guide 32: Standard Containers p1

This module puts the container-cost intuition built by hand-rolling a
dynamic array and a circular buffer to work choosing between the real
standard library sequence containers: `std::vector`, `std::deque`,
`std::list`, and `std::array`. It also nails down `std::vector`'s
size-versus-capacity bookkeeping under the standard's actual guarantees.

## Know before you start

- The array-vs-linked-list cost profile (random access, front insertion,
  splicing) [assumed: row 29 -- List ADT & Supporting DS]
- The deque ADT and the circular-buffer implementation backing
  `std::deque` [assumed: row 31 -- Stack, Queue, Deque (ADT)]
- `std::vector`'s heap growth versus `std::array`'s fixed compile-time size
  [assumed: row 7 -- Standard Library Types]
- Amortized O(1) `push_back` via capacity doubling [assumed: row 28 --
  Complexity Theory]

## Taught here

Concept: choosing a sequence container
- Know that `std::vector` is the correct default sequence container:
  reach for it first, and only move to another container when a scenario
  states a specific requirement it cannot meet.
- Know that `std::array` fits only when the element count is a true
  compile-time constant -- known while writing the code, never a runtime
  quantity, and never growing or shrinking afterward.
- Know that `std::deque` fits workloads needing fast, stable O(1)
  insertion/removal at BOTH the front and the back (`std::vector` is only
  O(1) at the back).
- Know that `std::deque` is NOT one contiguous block of memory -- it is
  internally a map (index) of separately allocated fixed-size blocks,
  which is exactly what lets it grow at the front without moving existing
  elements.
- Know the narrow, honest case where `std::list` wins: splice-heavy
  workloads (cutting a contiguous run out and reinserting it elsewhere)
  where iterators saved before the splice must remain valid afterward --
  `std::vector`/`std::deque` reallocation or shifting can invalidate saved
  iterators, but splicing a `std::list` never does.
- Be able to reason "is the size a compile-time constant?" first, then
  default to `std::vector`, and only reach past it for a stated
  front-insertion, splicing-with-iterator-stability, or fixed-size need.

Concept: size vs. capacity
- Know that `size()` counts elements actually stored; `capacity()` counts
  how much room is reserved before the next `push_back` would need to
  reallocate a bigger buffer -- the two numbers are tracked separately and
  move independently.
- Know that `reserve(n)` is standard-guaranteed to leave `capacity() >= n`,
  making a pre-`reserve`d capacity a portable, exactly-predictable number
  across compilers.
- Know that `std::vector`'s growth factor when it DOES reallocate (1.5x,
  2x, or another factor) is implementation-defined by the standard, so raw
  `capacity()` values after unpinned repeated `push_back` are not portable
  and should never be predicted as an exact number.
- Know which operations change only `size()`: `push_back`, `pop_back`,
  `clear()`, and `resize()` to a size within the current capacity.
- Know which operations can change `capacity()`: `reserve()`, and any
  `push_back`/`resize()` that outgrows the current capacity (triggering a
  reallocation).
- Know that `clear()` and `pop_back()` never release already-allocated
  capacity -- `size()` drops but `capacity()` stays exactly where it was.
- Know that `resize(n)` to a smaller `n` drops trailing elements
  (`size()` only shrinks); `resize(n)` to a larger `n` value-initializes
  the new slots (0 for `int`), never copying an existing element into
  them.

## Study checklist

- [ ] Given a workload description, pick vector, deque, list, or array and
      justify it by the one requirement that rules out the others.
- [ ] Explain what std::deque actually stores internally and why that
      design gives O(1) at both ends.
- [ ] Explain why unpinned push_back capacity values are not portable but
      reserve()-pinned ones are.
- [ ] List which operations move size() only vs. which can move
      capacity() too.
- [ ] Predict size()/capacity() after a reserve/push_back/pop_back/clear/
      resize sequence.

## Practiced in

`container-casting-call`, `capacity-chronicles`
