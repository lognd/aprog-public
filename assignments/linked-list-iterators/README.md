# Linked List Iterators

Last assignment you built `LinkedList<T>` from raw `Node*` pointers and
manual `new`/`delete`. That class works, but you can only walk it with a
hand-written loop that reaches into its internals (there is no such
internal access from outside the class -- `head_`/`tail_` are private).
This assignment adds an **iterator**: a small, movable cursor object that
walks the list one node at a time, without exposing a single pointer to
the outside world. By the end, your `LinkedList<T>` will support
`for (auto& x : list) { ... }` directly, the same way `std::vector` and
`std::map` do, plus two classic singly-linked positional operations,
`insert_after` and `erase_after`.

---

## Learning goals

- Understand what an iterator actually is: a cursor object, not a magic
  language feature -- build one yourself from a single wrapped `Node*`
- Implement `operator*`, `operator->`, prefix `++`, postfix `++`, and
  `==`/`!=` on a custom class, and see exactly how range-for uses them
- Internalize the `begin()`/`end()` fence-post picture: `end()` is one
  position PAST the last real element, never itself a real element
- Practice the difference between prefix `++it` (advance, then return the
  new state) and postfix `it++` (save the old state, advance, then return
  the saved copy)
- Design and implement `const`-correct iteration (`ConstIterator`,
  `cbegin()`/`cend()`) so read-only code can promise, at compile time,
  that it will never mutate the list
- Implement `insert_after`/`erase_after`, the natural positional
  operations for a singly linked list (as opposed to `insert_at`/
  `remove_at`'s index-based operations from last assignment), including
  the no-op contract when there is nothing after the given position

---

## Background

### An iterator is a cursor, not magic

Every iterator-based loop you have used so far -- `for (auto it =
v.begin(); it != v.end(); ++it)`, or even a plain range-for -- has been
using an **iterator**: an object that knows two things, how to read the
element it currently points at, and how to move to the next one. A
`std::vector<int>::iterator` internally is really just a wrapped
`int*`. `LinkedList<T>::Iterator`, which you are about to build, is really
just a wrapped `Node*`:

```cpp
class Iterator {
public:
    explicit Iterator(Node* node);
    T& operator*() const;    // read the element this cursor points at
    Iterator& operator++();  // move the cursor to the next node
    // ...
private:
    Node* node_;
};
```

There is no special compiler magic involved -- an iterator is an ordinary
class with a few operators overloaded so it can be used with `*`, `++`,
`==`, and `!=` syntax. That is the entire trick.

### The begin()/end() fence-post picture

For a list holding `10 -> 20 -> 30 -> nullptr`:

```
begin()
  |
  v
+------+     +------+     +------+
|  10  | --> |  20  | --> |  30  | --> nullptr
+------+     +------+     +------+
                                  ^
                                  |
                            end() (one PAST 30 -- not a real node)
```

`begin()` returns an `Iterator` wrapping the list's `head_` pointer.
`end()` returns an `Iterator` wrapping `nullptr` -- and this is exactly
why `nullptr` is a perfect choice for it: the last real node's `next` is
already `nullptr`, so advancing an iterator off the end of the list
naturally arrives at the same `nullptr` that `end()` represents, with no
special-case bookkeeping needed. `end()` is a **fence post**: a position
one step past the last real element, never itself a real element, and
never safe to dereference.

### Why range-for needs exactly these five operations

`for (auto& x : list) { body }` is not a special case the compiler
hard-codes for every type -- it **desugars** into an ordinary loop that
calls exactly five things on your iterator type:

```cpp
{
    auto __it = list.begin();
    auto __end = list.end();
    for (; __it != __end; ++__it) {
        auto& x = *__it;
        body
    }
}
```

`begin()`, `end()`, `operator!=`, `operator++` (prefix), and `operator*`
-- implement those five correctly on `Iterator`, and range-for works on
`LinkedList<T>` for free, with no other changes needed anywhere.

### Prefix vs. postfix: which one saves the old value?

```cpp
Iterator& operator++();      // prefix:  ++it
Iterator operator++(int);    // postfix: it++   (the `int` parameter is a
                              // dummy -- it exists only to give the
                              // compiler two DIFFERENT signatures to
                              // overload on; you never use its value)
```

Prefix `++it` advances the cursor, then returns a reference to the
now-advanced iterator itself. Postfix `it++` must do the OPPOSITE order:
save a copy of the iterator as it was BEFORE advancing, advance the real
iterator, then return the saved copy -- so that `auto old = it++;` leaves
`old` pointing at the ORIGINAL position and `it` pointing at the new one.
Getting this order backwards (advancing first, then copying) is a subtle
bug that looks identical to prefix `++` at the call site but breaks any
code that actually uses postfix's return value -- one of the wrong-answer
fixtures used to build this assignment's grader makes exactly this
mistake.

### Why a singly linked list gives forward-only iterators

Each `Node` only stores a pointer to the NEXT node, not the previous one
-- there is no way to walk backward from a given node without re-scanning
the whole list from `head_`. That is why `LinkedList<T>::Iterator` only
supports `operator++` (forward), never `operator--` (backward): a doubly
linked list (with a `prev` pointer on every node, an extension suggested
at the end of this README) would be needed to support that.

### `const`-correctness: `ConstIterator` and `cbegin()`/`cend()`

This assignment uses the simpler of two common designs: a completely
separate `ConstIterator` class (rather than making `Iterator` itself
`const`-parameterized with a template flag), exposed through `cbegin()`/
`cend()`, plus `const`-qualified overloads of `begin()`/`end()` that
forward to `cbegin()`/`cend()` so range-for still works automatically on
a `const LinkedList<T>&`. `ConstIterator`'s `operator*`/`operator->`
return `const T&`/`const T*`, so code holding only a `ConstIterator` has
no way to mutate the list through it, even though it walks the exact same
chain of nodes the same way `Iterator` does.

### `insert_after` / `erase_after`

These are the natural positional operations for a singly linked list,
building directly on the iterator you just wrote:

- `insert_after(pos, value)` inserts `value` immediately after the node
  `pos` points at. `pos` must not be `end()` -- there is nothing to
  insert "after" the fence post. If `pos == end()`, this is a documented
  no-op: it does nothing and returns `false`.
- `erase_after(pos)` removes the node immediately after the one `pos`
  points at. `pos` must not be `end()`, and there must actually be a node
  after it (if `pos` points at the last node, there is nothing after it
  to erase). Both conditions are documented no-ops: return `false` and
  change nothing.

Both must correctly update `tail_` when the affected node happens to be
the list's last node -- forgetting this breaks a later `push_back` (it
would silently corrupt the chain rather than actually appending), which
is exactly what the hidden tests check for.

---

## Task

Implement everything under `// YOUR TASK: forward iterators` in
`linked_list.hpp`:

- `Iterator`: constructor, `operator*`, `operator->`, prefix `operator++`,
  postfix `operator++(int)`, `operator==`, `operator!=`
- `ConstIterator`: the same six operations, `const`-qualified
- `begin()` / `end()` (mutable), `cbegin()` / `cend()`, and the
  `const`-qualified `begin()` / `end()` overloads that forward to them
- `find_it(value)` -- returns an `Iterator` to the first matching
  element, or `end()` if none matches
- `insert_after(pos, value)` -- see the contract above and in the header
- `erase_after(pos)` -- see the contract above and in the header

The Big-5 and the basic push/insert/remove/find/size operations are
already implemented for you at the top of the file -- do not modify them.
Fill in every declaration marked with a comment describing its contract;
do not change any function signature.

---

## Files

| File | Purpose |
|------|---------|
| `linked_list.hpp` | Big-5 and basic operations provided; implement the iterator classes and iterator-based operations here (header-only, no matching .cpp) |

## Compilation and Testing

```bash
cd visible-tests
mkdir build && cd build
cmake .. -DSUBMISSION_DIR=<path-to-your-linked_list.hpp-directory>
cmake --build .
./linked-list-iterators_tests
```

Run under AddressSanitizer while developing to catch double-deletes and
use-after-frees early (in particular from `erase_after`):

```bash
g++ -std=c++17 -fsanitize=address -g -I. your_test.cpp -o test && ./test
```

---

## Constraints

- Do not use `std::vector`, `std::list`, or `std::deque` anywhere in
  `linked_list.hpp`.
- Do not use exceptions (`throw`/`try`/`catch`) anywhere in
  `linked_list.hpp`.
- Do not modify the public interface (function signatures) already
  declared in `linked_list.hpp`, and do not modify the provided Big-5 or
  basic operations.
- `erase_after` must actually `delete` the node it removes -- an
  `erase_after` that only re-links pointers without freeing the old
  node's memory leaks, and is caught directly by Valgrind.

---

## Grading

| Component | Points |
|-----------|--------|
| Source constraints (no `std::vector`/`std::list`/`std::deque`, no exceptions) | 10 |
| Compilation | 0 |
| Visible correctness (Catch2) | 30 |
| Hidden correctness (Catch2) | 40 |
| Memory safety (Valgrind, visible) | 5 |
| Memory safety (Valgrind, hidden) | 5 |
| Memory safety (ASan, visible) | 5 |
| Memory safety (ASan, hidden) | 5 |
| **Total** | **100** |

## Submission

Submit a single file named `linked_list.hpp`. Do not rename it.

## Going further

- Convert `LinkedList<T>` into a doubly linked list (`Node` gains a
  `prev` pointer) and add `operator--` to `Iterator`, making it a
  **bidirectional** iterator -- the same category `std::list`'s iterator
  belongs to.
- Implement `insert_before(pos, value)` for the doubly linked version from
  the previous idea. Why is `insert_before` easy for a doubly linked list
  but awkward for a singly linked one (hint: think about what a singly
  linked `insert_after` needs versus what `insert_before` would need)?
- Add a `reverse_iterator` that walks the list backward, the way
  `std::vector::rbegin()`/`rend()` do in `iterator-walk` -- what does a
  singly linked list need in order to support this at all?
