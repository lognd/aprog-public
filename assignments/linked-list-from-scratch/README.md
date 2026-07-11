# Linked List From Scratch

You have already used `std::vector`, which stores its elements in one
contiguous block of memory. A **linked list** stores each element in its
own separately allocated **node**, and each node points to the next one.
This assignment asks you to build a singly linked list class template,
`LinkedList<T>`, from raw pointers and `new`/`delete` -- the same way
`std::vector` and `std::list` are built underneath, minus all their extra
machinery. By the end you will have implemented a full Big 5 (destructor,
copy constructor, copy assignment, move constructor, move assignment) for
a data structure made of many separately allocated pieces instead of one
contiguous buffer, which is a meaningfully different problem than the
single-pointer case you saw in the unique-pointer assignment.

---

## Learning goals

- Build the node/next-pointer mental model: a linked list is a chain of
  heap-allocated nodes, each holding a value and a pointer to the next node
- Implement a correct **deep copy** of a multi-node structure: copying a
  linked list means allocating a brand-new node for every element, not
  copying pointers
- Implement move construction/assignment that steals an entire chain of
  nodes in O(1) by reassigning three pointers (head, tail, size) instead of
  copying any nodes
- Practice the delete-order trap: freeing a node before reading its `next`
  pointer corrupts the rest of the traversal
- Maintain an O(1) `size()` by tracking a running count instead of walking
  the list, and an O(1) `push_back` by keeping a tail pointer instead of
  walking to the end
- Design a no-exceptions error contract: out-of-range operations return a
  `bool` success flag instead of throwing

## Background

### The node/next-pointer mental model

A `std::vector<int>` holding `{10, 20, 30}` looks like one block of memory:

```
index:   0    1    2
        +----+----+----+
        | 10 | 20 | 30 |
        +----+----+----+
```

A linked list holding the same three values looks completely different.
Each value lives in its own node, allocated separately with `new`, and each
node stores a pointer to the next node:

```
head_
  |
  v
+------+------+     +------+------+     +------+------+
|  10  | next-+---->|  20  | next-+---->|  30  | next-+---->  nullptr
+------+------+     +------+------+     +------+------+
                                            ^
                                            |
                                          tail_
```

`head_` points at the first node. The last node's `next` pointer is
`nullptr` -- that is how you know traversal has reached the end. This
assignment's `LinkedList<T>` also keeps a `tail_` pointer at the last node,
so that `push_back` does not have to walk the whole list every time (more
on that below).

There is no index-based random access here: to reach the node at position
4, you must follow `next` four times starting from `head_`. That cost --
O(n) to reach an arbitrary position, versus O(1) for `std::vector`'s
`operator[]` -- is the central tradeoff of linked lists, and it is explored
in the List ADT activities that come before this assignment.

### Why smart pointers are set aside here

Every other assignment in this course that manages heap memory uses
`std::unique_ptr` or a hand-built equivalent. This assignment uses a raw
`Node*` with manual `new`/`delete` instead, on purpose:

- If `Node::next` were a `std::unique_ptr<Node>`, destroying a long list
  would destroy `head_`, whose destructor destroys its `next`, whose
  destructor destroys its `next`, and so on -- one recursive call per node.
  A list of 100,000 nodes would blow the call stack. `LinkedList<T>`'s
  `clear()` avoids this by deleting nodes in an explicit loop.
- The point of this exercise is to see the pointer-chasing and manual
  memory management directly, the way `std::list` itself is implemented
  underneath. Wrapping every `next` pointer in a smart pointer here would
  hide exactly the mechanics you are here to learn. (You already built
  that muscle in the unique-pointer assignment -- this one is deliberately
  raw.)

Manual `new`/`delete` is correct and expected in this file. Just make sure
every `new` you write is matched by exactly one `delete`, on every code
path, including copies and self-assignment.

### Why copying must deep-copy node by node

If `LinkedList`'s copy constructor just copied the `head_` pointer field
(the way a compiler-generated copy constructor would), the copy and the
original would both point at the *same* chain of nodes. Destroying either
one would delete nodes the other still thinks it owns -- a double-delete,
the same disaster you saw with a shallow-copied unique pointer, just with
more nodes involved. A correct copy constructor walks the source list from
`head_` to `nullptr` and calls `push_back` for each value, allocating an
entirely new, independent chain:

```
original:  head_ -> [10] -> [20] -> [30] -> nullptr
copy:      head_ -> [10] -> [20] -> [30] -> nullptr   (different node addresses)
```

Mutating the copy (e.g. `copy.push_front(5)`) must never change what
`original` sees, and vice versa, because they now own completely separate
nodes.

### Why move steals head_/tail_/size_ instead of copying

Moving a `LinkedList` is the opposite situation: the source is about to be
discarded (or is being reused as an empty list), so there is no need to
preserve its nodes. A move constructor/assignment just copies the three
member variables -- `head_`, `tail_`, `size_` -- from the source into the
destination, then resets the source's members to the empty state
(`nullptr`, `nullptr`, `0`). No node is allocated, copied, or freed. This
is why moving a 10,000-node list is O(1) while copying it is O(n).

The source must be left in a valid, empty state, not a dangling one: after
`b = std::move(a);`, `a` must be safe to destroy and safe to keep using
(e.g. `a.push_back(1)` should work normally and start a fresh list).

### The delete-order trap in clear()

A tempting but broken way to write `clear()`:

```cpp
Node* cur = head_;
while (cur != nullptr) {
    delete cur;         // WRONG: frees cur before reading cur->next
    cur = cur->next;    // use-after-free -- cur is a dangling pointer here
}
```

Once `delete cur;` runs, reading `cur->next` on the next line is a
**use-after-free**: the memory has been returned to the allocator and may
already be overwritten. The fix is to save `next` *before* deleting the
current node:

```cpp
Node* cur = head_;
while (cur != nullptr) {
    Node* next = cur->next;   // save it first
    delete cur;                // now safe to free cur
    cur = next;                 // advance using the saved pointer
}
```

This same trap applies inside `remove_at` and the destructor. AddressSanitizer
and Valgrind, both used in grading, will catch this class of bug directly.

---

## Task

Implement every member of `LinkedList<T>` declared in `linked_list.hpp`:

- Default constructor, destructor, copy constructor, copy assignment, move
  constructor, move assignment (the full Big 5)
- `push_front(value)` -- insert at the head, O(1)
- `push_back(value)` -- insert at the tail, O(1) (use the `tail_` pointer;
  do not walk the list from `head_`)
- `insert_at(index, value)` -- insert so the new element becomes position
  `index`. Valid range is `[0, size()]` inclusive (`index == size()` means
  "append"). Returns `true` on success, `false` and no-op if
  `index > size()`. No exceptions.
- `remove_at(index)` -- remove the element at position `index`. Valid range
  is `[0, size())`. Returns `true` on success, `false` and no-op if
  `index >= size()` (including on an empty list). No exceptions.
- `find(value)` -- returns the index of the first matching element, or
  `-1` if none matches
- `size()` -- O(1); track a running count as a member variable
- `empty()`
- `clear()` -- frees every node and resets to the empty state; safe to
  call more than once and safe to keep using the list afterward
- `front()` / `back()` -- reference to the first/last element (only called
  when the list is non-empty)

The full declarations, with the exact contract for each function, are
documented as comments in `linked_list.hpp`. Do not change any function
signature.

---

## Files

| File | Purpose |
|------|---------|
| `linked_list.hpp` | Declarations -- implement every member here (header-only, no matching .cpp) |

## Compilation and Testing

```bash
cd visible-tests
mkdir build && cd build
cmake .. -DSUBMISSION_DIR=<path-to-your-linked_list.hpp-directory>
cmake --build .
./linked-list-from-scratch_tests
```

Run under AddressSanitizer while developing to catch double-deletes and
use-after-frees early:

```bash
g++ -std=c++17 -fsanitize=address -g -I. your_test.cpp -o test && ./test
```

---

## Constraints

- Do not use `std::vector`, `std::list`, or `std::deque` anywhere in
  `linked_list.hpp`.
- Do not use exceptions (`throw`/`try`/`catch`) anywhere in `linked_list.hpp`.
- Do not modify the public interface (function signatures) declared in
  `linked_list.hpp`.
- `push_back` and `size()` must be O(1). A `push_back` that walks the list
  from `head_` to find the last node, or a `size()` that counts nodes on
  every call, does not meet the assignment's requirements even if it
  produces correct answers.

---

## Grading

| Component | Points |
|-----------|--------|
| Source constraints (no `std::vector`/`std::list`/`std::deque`) | 10 |
| Compilation | 0 |
| Visible correctness (Catch2) | 30 |
| Hidden correctness (Catch2) | 30 |
| Performance (O(1) `push_back` and `size`) | 10 |
| Memory safety (Valgrind, visible) | 5 |
| Memory safety (Valgrind, hidden) | 5 |
| Memory safety (ASan, visible) | 5 |
| Memory safety (ASan, hidden) | 5 |
| **Total** | **100** |

## Submission

Submit a single file named `linked_list.hpp`. Do not rename it.

## Going further

- Implement a `reverse()` member that reverses the list in place using
  three pointers (`prev`, `cur`, `next`) and O(1) extra space -- the same
  technique used in the `link-tracer` activity.
- Add a `[]`-style random-access helper and measure, with a stopwatch or
  `std::chrono`, how much slower it is than `std::vector::operator[]` for
  a list of 100,000 elements. This is the tradeoff explored in the
  `list-tradeoff-tribunal` and `index-vs-node` activities.
- Convert `LinkedList<T>` into a doubly linked list (`Node` gains a `prev`
  pointer) and implement `pop_back()` in O(1). What has to change in every
  function that currently touches `tail_`?
