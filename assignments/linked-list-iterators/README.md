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

## Examples at a glance

To make every operation concrete, here is **one** list, built with three
`push_back` calls, and what each iterator operation does to it or returns
from it. Read this table first -- it is the whole assignment in miniature.

```
list.push_back(10);
list.push_back(20);
list.push_back(30);

+------+     +------+     +------+
|  10  | --> |  20  | --> |  30  | --> nullptr
+------+     +------+     +------+
   ^                          ^
   |                          |
begin()                 end() is one past this node (wraps nullptr)
```

| Call | Returns / Result | Why |
|------|-------------------|-----|
| `list.begin()` | `Iterator` wrapping the node holding `10` | `begin()` always wraps `head_`, the first real node |
| `list.end()` | `Iterator` wrapping `nullptr` | `end()` is the fence post -- one position PAST `30`, never itself a real node |
| `*list.begin()` | `10` | dereferencing reads the data stored in the node the cursor currently points at |
| `auto it = list.begin(); ++it; *it` | `20` | prefix `++` moves the cursor to `head_->next` (the node holding `20`), then `*it` reads it |
| `auto it = list.begin(); auto old = it++; *old` then `*it` | `*old == 10`, `*it == 20` | postfix `it++` saves the position BEFORE moving (`old` stays at `10`), then advances the real iterator (`it` moves to `20`) |
| `list.find_it(20)` | `Iterator` at the node holding `20` | scans from `head_` until `cur->data == 20` |
| `list.find_it(99)` | `list.end()` | `99` never appears, so the scan falls off the end and returns the fence post |
| `list.insert_after(list.find_it(20), 25)` | `true`; list becomes `10 -> 20 -> 25 -> 30` | a new node holding `25` is spliced in right after the node holding `20` |
| `list.insert_after(list.end(), 99)` | `false`, list unchanged | `end()` is not a real node -- there is nothing to insert "after" a fence post, so this is a documented no-op |
| `list.erase_after(list.find_it(20))` (on the 4-node list above) | `true`; list becomes `10 -> 20 -> 30` again | the node right after `20` (holding `25`) is unlinked and `delete`d |
| `list.erase_after(list.find_it(30))` | `false`, list unchanged | `30` is the last node -- there is nothing after it to erase |
| `LinkedList<int>{}.begin() == LinkedList<int>{}.end()` | `true` | an empty list has `head_ == nullptr`, so `begin()` (wraps `head_`) and `end()` (wraps `nullptr`) wrap the same pointer |
| `list.cbegin()` | `ConstIterator` at the node holding `10` | walks the exact same chain as `begin()`, but `*` returns `const T&`, so the list cannot be mutated through it |

## Worked example: watch a sequence of iterator operations run, step by step

This is the single most important thing to understand in the assignment, so
here is every step spelled out. Start from the same list as above,
`10 -> 20 -> 30 -> nullptr`, and run this sequence:

```cpp
auto it = list.begin();   // step 1
int a = *it;              // step 2
++it;                     // step 3
int b = *it;              // step 4
auto old = it++;          // step 5
int c = *old;              // step 6
int d = *it;                // step 7
++it;                     // step 8
bool done = (it == list.end()); // step 9
```

| Step | Code | Cursor position after this step | What happened and why |
|------|------|----------------------------------|------------------------|
| 1 | `auto it = list.begin();` | `it` wraps the node holding `10` | `begin()` always starts at `head_`, the first real node |
| 2 | `int a = *it;` | unchanged, still at `10` | `operator*` only READS the current node's data; it never moves the cursor. `a == 10` |
| 3 | `++it;` | `it` wraps the node holding `20` | prefix `++` follows `node_->next`: the node holding `10`'s `next` pointer leads to the node holding `20` |
| 4 | `int b = *it;` | unchanged, still at `20` | reading again without moving. `b == 20` |
| 5 | `auto old = it++;` | `it` now wraps `30`; `old` wraps `20` | postfix `it++` must save the CURRENT position first (`old` gets a copy pointing at `20`), THEN advance the real `it` to `30`. Getting this order backwards is the classic postfix bug. |
| 6 | `int c = *old;` | (reading `old`, not `it`) | `old` was saved at step 5 pointing at `20`, so `c == 20` |
| 7 | `int d = *it;` | (reading `it`) | `it` was advanced to `30` at step 5, so `d == 30` |
| 8 | `++it;` | `it` wraps `nullptr` | `30` is the last node, so `30`'s `next` is `nullptr` -- advancing off the last real node naturally lands on the same `nullptr` that `end()` wraps. No special-case code is needed for this to work. |
| 9 | `bool done = (it == list.end());` | -- | `list.end()` also wraps `nullptr`, and `operator==` compares the wrapped pointers, so `it == list.end()` compares `nullptr == nullptr`. `done == true`. |

Final values: `a == 10`, `b == 20`, `c == 20`, `d == 30`, `done == true`.
Dereferencing `it` after step 8 (i.e. `*it`) would be undefined behavior --
`it` now wraps `nullptr`, and `end()` is a fence post that is never safe to
read from. This is exactly why every loop in this assignment checks
`it != list.end()` BEFORE dereferencing `it`, never after.

---

## Task

Implement everything under `// YOUR TASK: forward iterators` in
`linked_list.hpp`:

**`Iterator`: constructor, `operator*`, `operator->`, prefix `operator++`,
postfix `operator++(int)`, `operator==`, `operator!=`.**
(list is `10 -> 20 -> 30`, `it = list.begin()`)

- **Example (dereference):** `*it == 10`.
- **Example (prefix advance):** after `++it`, `*it == 20`.
- **Example (postfix advance):** `auto old = it++` (from `20`) leaves
  `*old == 20` and **`*it == 30`**.
- **Example (fence-post comparison):** `it == list.end()` is `false`
  while `it` is at any real node, and becomes `true` only once `it`
  has been advanced past `30`.
- **Error case (undefined behavior):** dereferencing `list.end()`
  (i.e. `*list.end()`) is **undefined behavior** and must never be done.

**`ConstIterator`: the same six operations, `const`-qualified.**

- **Example (empty-list comparison):** `list.cbegin() == list.cend()`
  is `true` **only for an empty list**.
- **Example (const read):** `*list.cbegin()` on `10 -> 20 -> 30` is
  `const int&` bound to `10`.
- **Error case (no mutation):** assigning through it, e.g.
  `*list.cbegin() = 5;`, **must not compile**.
- **Example (converting constructor):** a `ConstIterator` constructed
  from an `Iterator` (via the implicit converting constructor) points
  at the same node, so `ConstIterator(list.begin()) == list.cbegin()`
  is **`true`**.

**`begin()` / `end()` (mutable), `cbegin()` / `cend()`, and the
`const`-qualified `begin()` / `end()` overloads that forward to them.**

- **Empty-list case:** for `LinkedList<int> empty;` (nothing pushed),
  `empty.begin() == empty.end()` is **`true`** (both wrap `nullptr`).
- **Example (non-empty list):** for `10 -> 20 -> 30`,
  `list.begin() == list.end()` is `false`.
- **Example (const overload):** given
  `const LinkedList<int>& clist = list;`, `clist.begin()` returns a
  `ConstIterator` (the `const`-qualified overload), so
  `for (int x : clist)` compiles and **reads every element without
  being able to modify any of them**.

**`find_it(value)` -- returns an `Iterator` to the first matching
element, or `end()` if none matches.**

- **Example (found):** on `10 -> 20 -> 30`, `*list.find_it(20) == 20`.
- **Example (not found):** `list.find_it(99) == list.end()`.
- **Empty-list case:** on an empty list, `empty.find_it(0) ==
  empty.end()` -- nothing to find, so it falls straight through to
  `end()`.

**`insert_after(pos, value)` -- see the contract above and in the header.**

- **Example (middle insert):** on `10 -> 20 -> 30`,
  `list.insert_after(list.find_it(20), 25)` returns `true` and the
  list becomes `10 -> 20 -> 25 -> 30`.
- **Tricky case (insert after last node):**
  `list.insert_after(list.find_it(30), 40)` returns `true`, the list
  becomes `... -> 30 -> 40`, and **`list.back() == 40`** afterward
  (`tail_` was correctly updated).
- **Edge case (`end()`):** `list.insert_after(list.end(), 99)`
  returns **`false`** and changes nothing, since `end()` is a fence
  post with no node to insert after.

**`erase_after(pos)` -- see the contract above and in the header.**

- **Example (middle erase):** on `10 -> 20 -> 30`,
  `list.erase_after(list.find_it(10))` returns `true` and the list
  becomes `10 -> 30`.
- **Tricky case (erase after last node):**
  `list.erase_after(list.find_it(30))` (`30` is the last node,
  nothing after it) returns **`false`** and leaves the list unchanged.
- **Edge case (`end()`):** `list.erase_after(list.end())` also
  returns `false` for the same reason `insert_after(list.end(), ...)`
  does -- `end()` is not a real node to erase "after".

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
