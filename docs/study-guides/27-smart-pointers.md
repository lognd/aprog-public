# Study Guide 27: Smart Pointers (std + build your own)

This module turns heap ownership into an explicit design decision:
choosing among `unique_ptr`, `shared_ptr`, `weak_ptr`, and plain raw
pointers/references per scenario; tracing `shared_ptr` reference counts
exactly, including the cycle leak; and implementing a `unique_ptr`-like
class from scratch with correct move semantics, `release`, and `reset`.

## Know before you start

- The Big Five, move semantics, and `std::move` as a cast [assumed: row 25
  -- Dynamic Memory]
- RAII and why an owning type deletes its copy operations [assumed: row 21
  -- OOP Implementation in C++]
- Operator overloading, the member-vs-free decision rule, and
  `explicit operator bool` [assumed: row 21 -- OOP Implementation in
  C++]
- Double-delete, leaks, and dangling pointers as bug classes [assumed:
  row 25 -- Dynamic Memory]
- Valgrind and ASan leak checking [assumed: row 26 -- Memory & Profiling
  Tools]
- Abstract base classes and factories over `Shape`-style hierarchies
  [assumed: row 22 -- Inheritance]

## Taught here

Concept: ownership as a design question
- Know that ownership means responsibility for eventually freeing a heap
  object, and that exactly one decision procedure applies to every heap
  object: who destroys it, and when.
- Know the four verdicts: `unique_ptr` (exactly one owner at a time;
  copying is a compile error; ownership transfers by move; destruction
  deletes the object), `shared_ptr` (multiple simultaneous owners via a
  reference count in a heap-allocated control block; object destroyed when
  the count hits zero), `weak_ptr` (a non-owning observer of a
  `shared_ptr`-managed object; never keeps it alive; `.lock()` returns a
  live `shared_ptr` or an empty one), and a plain raw pointer or reference
  (pure borrow: look at or use an object briefly without ever managing its
  lifetime).
- Be able to pick the verdict by asking: how many owners, and do they
  overlap in time with no identifiable "last one standing"? Does the code
  only need to check on the object without keeping it alive? Or does it
  merely borrow?
- Know the "`shared_ptr` everywhere" overuse trap: every copy does an
  atomic reference-count update and every `shared_ptr` needs a control
  block, so defaulting to it when `unique_ptr` or a raw borrow would do
  has real cost.

Concept: shared_ptr mechanics and the cycle leak
- Know that copying a `shared_ptr` increments `use_count()` and destroying
  one (or `.reset()`) decrements it; moving one transfers ownership
  without changing the count and leaves the source null.
- Know that passing a `shared_ptr` by value bumps the count for the
  duration of the call.
- Be able to trace `use_count()` as a running total through copies, moves,
  function calls, and scope exits, remembering locals destroy in reverse
  declaration order at their closing brace.
- Know the reference-cycle leak: two objects holding `shared_ptr`s to each
  other keep each other's counts above zero forever, so neither destructor
  ever runs even when nothing else can reach them -- a genuine silent
  leak.
- Know the fix: make one direction (usually the back-reference, e.g. child
  to parent) a `weak_ptr`, since ownership usually has one natural
  direction.

Concept: building a unique owner from scratch
- Know why a unique-owner copy constructor cannot exist: copying the raw
  pointer means two destructors delete the same address (double-delete,
  undefined behavior); "copying by stealing" is a move, not a copy -- so
  the copy operations are `= delete`d, turning the mistake into a compile
  error.
- Be able to implement a move constructor that steals the source's pointer
  and nulls the source (without the nulling, the source's destructor
  double-deletes), marked `noexcept` so containers move instead of copy.
- Know move assignment's extra duties: delete whatever `*this` already
  owned first (or leak it), and guard against self-move so `p =
  std::move(p)` does not delete the object out from under itself.
- Know the three lookalike operations precisely: `get()` returns the raw
  pointer for inspection while the smart pointer keeps ownership (never
  delete what `get()` returns); `release()` returns the pointer AND
  forgets it, transferring ownership to the caller; `reset(p)` deletes the
  currently owned pointer then takes ownership of `p`.
- Know the self-reset trap: `p.reset(p.get())` must not delete
  unconditionally before storing, or it re-stores a just-deleted (dangling)
  address -- compare the incoming pointer against the owned one first.
- Be able to implement the supporting members: member `swap`, `operator*`
  and `operator->` (undefined on null, same as `std::unique_ptr`), and
  `explicit operator bool`.

Concept: using std::unique_ptr as a caller
- Be able to write a factory function that constructs with
  `std::make_unique` and returns a `std::unique_ptr<Base>` (empty on
  unknown input) so callers never write `new`.
- Know the parameter conventions: take a `const
  std::vector<std::unique_ptr<T>>&` by reference to inspect without taking
  ownership; return a `std::unique_ptr` by value when transferring
  ownership out.
- Know that a `unique_ptr` can only be moved out of a container element,
  never copied -- `std::move` is required, and the vacated slot becomes an
  empty `unique_ptr`.
- Know that assertion-passing tests can still leak or double-free, which
  is why unique-owner code is verified under Valgrind and ASan in addition
  to unit tests.

## Study checklist

- [ ] For a scenario (tree children, observer list, cache, read-only
      function parameter), name the correct pointer kind and justify it.
- [ ] Trace `use_count()` through a copy, a move, a by-value call, and a
      scope exit.
- [ ] Explain the reference-cycle leak and which direction becomes
      `weak_ptr`.
- [ ] State what `get()`, `release()`, and `reset()` each do to ownership.
- [ ] Explain the self-move and self-reset traps and their guards.
- [ ] Explain why the move constructor must null the source's pointer.

## Practiced in

`ownership-court`, `shared-ptr-tracer`, `unique-ptr-from-scratch`
