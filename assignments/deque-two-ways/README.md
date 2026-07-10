# Deque, Two Ways

A **deque** (pronounced "deck", short for "double-ended queue") is an
**ADT** (Abstract Data Type -- a description of what operations a data
structure supports and what they mean, without saying how it is
implemented) that supports inserting and removing elements at BOTH ends in
O(1) time: `push_front`/`push_back` to insert, `pop_front`/`pop_back` to
remove, plus `front()`/`back()` to look at either end without removing it.
This assignment asks you to build a deque two different ways -- `ArrayDeque<T>`
on top of a circular array buffer, and `ListDeque<T>` on top of a doubly
linked list -- and then build `Stack<T>` and `Queue<T>` as thin **adapters**
(wrapper classes that expose a smaller, renamed subset of another class's
operations) on top of whichever deque backend you choose.

---

## Learning goals

- Understand why a plain (non-wrapping) array makes `pop_front` an O(n)
  operation, and how a circular buffer fixes that
- Build the circular-buffer mental model: a `head_` index, a `size_` count,
  and modulo arithmetic to "wrap" an index back to the start of the array
- Implement grow-on-full with re-linearization: doubling a wrapped array's
  capacity safely, without scrambling element order
- Practice the Big 5 (destructor, copy/move construct, copy/move assign)
  on a second, different kind of owned resource (a raw array instead of a
  chain of nodes)
- Recognize the **adapter pattern**: `Stack<T>` and `Queue<T>` are not new
  data structures, they are restricted views over a deque, the same way
  `std::stack` and `std::queue` are implemented over `std::deque` in the
  real C++ standard library

## Background

### The deque ADT and its operations

An ADT describes a contract -- what you can ask a data structure to do, and
what each operation means -- without dictating how the data is stored in
memory. The deque ADT's contract is:

| Operation | Meaning |
|-----------|---------|
| `push_back(v)` | Insert `v` as the new last element |
| `push_front(v)` | Insert `v` as the new first element |
| `pop_back()` | Remove the last element |
| `pop_front()` | Remove the first element |
| `back()` | Look at (do not remove) the last element |
| `front()` | Look at (do not remove) the first element |
| `size()` / `empty()` | How many elements, and whether there are zero |

The defining promise of a deque, as opposed to a plain array or a singly
linked list, is that ALL SIX of `push_back`, `push_front`, `pop_back`,
`pop_front`, `front`, and `back` are O(1). This assignment builds the same
ADT on top of two different underlying storage strategies, so you can see
exactly which parts of the implementation change and which parts of the
contract stay fixed regardless of storage choice.

### Why a plain array makes pop_front O(n)

Suppose you tried to build a deque the naive way: a dynamically allocated
array where element 0 is always the logical front. `push_back` is easy --
write into the next open slot at the end. But `pop_front` is not:

```
before pop_front():
index:   0    1    2    3
        +----+----+----+----+
        | 10 | 20 | 30 | 40 |
        +----+----+----+----+

after removing 10, EVERY remaining element must shift left one slot:
index:   0    1    2
        +----+----+----+
        | 20 | 30 | 40 |
        +----+----+----+
```

Removing the front element and then shifting every other element left by
one slot is O(n) -- the cost grows with however many elements are currently
in the deque. Do that inside a loop that alternates `push_back`/`pop_front`
many times (the exact pattern this assignment's hidden tests use), and the
total cost becomes O(n) per operation, over and over -- exactly the kind of
hidden quadratic blowup that a correct deque implementation must avoid.
Note that this shifting approach still produces the RIGHT ANSWER every
time -- `front()`, `back()`, and every element's value would all be
correct. The bug is purely a performance bug, invisible to ordinary
correctness tests, which is why this assignment also grades `pop_front`'s
running time directly (see Grading below).

### The circular buffer idea

A **circular buffer** (also called a **ring buffer**) solves this by
letting the logical front live at ANY index in the array, not just index 0.
Instead of shifting elements when the front is removed, you just move a
`head_` index forward by one. The array is treated as if it wraps around --
after the last physical index, the "next" slot is index 0 again, like a
clock face wrapping from 12 back to 1:

```
capacity_ = 8, head_ = 5, size_ = 4
logical order: [physical 5], [physical 6], [physical 7], [physical 0]

physical index:  0    1    2    3    4    5    6    7
                +----+----+----+----+----+----+----+----+
                | 40 |    |    |    |    | 10 | 20 | 30 |
                +----+----+----+----+----+----+----+----+
                  ^                        ^
             (wrapped back            head_ = 5
              around to 0)         (logical front,
                                       value 10)
```

Here the deque logically holds `10, 20, 30, 40` in that order, even though
physically `40` sits at index 0 -- BEFORE `head_` in raw array terms. The
element after physical index 7 (the last slot) is physical index 0, not
"off the end of the array." That wraparound is what "circular" means.

### Modulo arithmetic and wraparound, concretely

The tool that makes an index "wrap around" is the **modulo operator** (`%`
in C++): `a % b` gives the remainder of `a` divided by `b`, and for a
non-negative `a` that remainder is always in the range `[0, b)`. Applied to
an array index, `index % capacity_` takes any raw index -- even one that
has walked past the end of the array -- and folds it back into the valid
range of physical slots.

Worked example, continuing the diagram above (`capacity_ = 8`, `head_ = 5`,
`size_ = 4`): to find where `push_back` should write the fifth element, you
compute `(head_ + size_) % capacity_`:

```
head_ + size_ = 5 + 4 = 9
9 % 8 = 1     (9 divided by 8 is 1 remainder 1)
```

So the new element goes at physical index 1, NOT physical index 9 (which
does not exist -- the array only has 8 slots, indices 0 through 7). Every
index calculation in `ArrayDeque<T>` -- the write position for `push_back`,
the write position for `push_front`, the read position for `back()` --
follows this same pattern: compute the "raw" index as if the array went on
forever, then take it `% capacity_` to fold it back into range.

`push_front` uses the same idea in the other direction. To move `head_`
backward by one slot (wrapping past index 0 back to the last index),
compute `(head_ + capacity_ - 1) % capacity_` rather than `head_ - 1`
directly -- subtracting 1 from an unsigned index of 0 would underflow to a
huge number instead of wrapping to `capacity_ - 1`, which is exactly the
kind of bug this assignment's memory-safety grading is designed to catch.

### Why growth must re-linearize

Eventually a full circular buffer needs more room. The natural fix is the
same one `std::vector` uses: allocate a new, larger array (this assignment
doubles the capacity) and copy the existing elements into it. But you
cannot just copy the old array byte-for-byte into a bigger one -- if the
deque was wrapped (`head_ != 0`, elements split across the end of the
array), a byte-for-byte copy would put the elements in the new array in the
WRONG order (physical order, not logical front-to-back order):

```
before grow (wrapped): capacity_ = 8, head_ = 5, size_ = 4
physical: [40, _, _, _, _, 10, 20, 30]     logical order: 10, 20, 30, 40

WRONG grow (copies physical slots as-is):
new array: [40, _, _, _, _, 10, 20, 30, _, _, _, _, _, _, _, _]
  -- head_ would need to stay 5, and the deque is now scrambled across a
     bigger array for no reason, or worse, treated as starting at index 0
     with 40 first -- the wrong logical order entirely.

CORRECT grow (re-linearizes: copies starting at head_, wrapping,
into new array starting at index 0):
new array: [10, 20, 30, 40, _, _, _, _, _, _, _, _, _, _, _, _]
  -- head_ is reset to 0. Logical order (10, 20, 30, 40) is preserved.
```

"Re-linearize" means: read the elements out in their correct logical
order (starting at `head_`, wrapping via `% capacity_` as you go) and
write them into the new array starting fresh at index 0. This is also why
growing is a good time to reset `head_` back to 0 -- the new array does not
need to preserve the old wraparound point at all, only the element order.

### The adapter pattern connection

You have already seen the adapter pattern in this course under Design
Patterns: a class that does not implement its own core logic, but instead
wraps another class and exposes a smaller, renamed subset of that class's
operations. `Stack<T>` and `Queue<T>` in this assignment are exactly that:

- `Stack<T>` is LIFO (last-in, first-out): `push` and `pop` both happen at
  the SAME end. It is implemented by delegating `push` to `push_back`,
  `pop` to `pop_back`, and `top` to `back` on an underlying deque.
- `Queue<T>` is FIFO (first-in, first-out): `push` happens at one end,
  `pop` happens at the OTHER end. It is implemented by delegating `push` to
  `push_back`, `pop` to `pop_front`, `front` to `front`, and `back` to
  `back` on an underlying deque.

This mirrors how the real C++ standard library builds `std::stack` and
`std::queue`: neither is a standalone data structure with its own storage.
Both are templates parameterized on an underlying container (`std::deque`
by default) that they hold as a private member and delegate to. This
assignment's `Stack<T, D = ArrayDeque<T>>` and `Queue<T, D = ArrayDeque<T>>`
use the same shape -- `D` is a template parameter with a default, so
`Stack<int>` uses `ArrayDeque<int>` automatically, but `Stack<int,
ListDeque<int>>` swaps in the linked-list backend with no other code
changes. This is a deliberately simpler form than the real
`std::stack<T, Container = std::deque<T>>` (which also lets you swap
containers), chosen because at this point in the course you have seen
templates and container types but have not yet seen iterators, which
`std::deque`'s real interface leans on.

### Array vs. list tradeoffs, recap

You have already seen this tradeoff in the List ADT activities before the
linked-list-from-scratch assignment, and it applies here too:

- `ArrayDeque<T>` stores every element **contiguously** (back to back in
  one block of memory), which is cache-friendly -- visiting nearby elements
  tends to be fast because they are physically close together in memory
  (this property is called **locality**). Its cost is the occasional O(n)
  grow (amortized O(1) per push, the same argument used for
  `std::vector::push_back` in the `big-o-lineup` activity).
- `ListDeque<T>` stores every element in its own separately allocated node,
  so there is never a bulk grow/copy step -- but each node can live
  anywhere in memory, so traversal has poor locality, and each node carries
  extra memory overhead for its `prev`/`next` pointers.

Both backends satisfy the exact same deque ADT contract with the exact
same asymptotic complexity for every operation -- this is the point of
separating an ADT's contract from its implementation. The choice between
them is a real engineering tradeoff, not a correctness question.

---

## Task

Implement every member declared in three header files:

- `array_deque.hpp` -- `ArrayDeque<T>`, a circular-buffer array backend.
  Full Big 5, `push_front`/`push_back`/`pop_front`/`pop_back` (all O(1)),
  `front()`/`back()`, `size()`/`empty()`/`capacity()`, and a private
  `ensure_capacity()` that doubles and re-linearizes on grow.
- `list_deque.hpp` -- `ListDeque<T>`, a doubly linked list backend. Full
  Big 5, the same six deque operations, `size()`/`empty()`, and `clear()`.
- `stack_queue.hpp` -- `Stack<T, D>` and `Queue<T, D>`, container adapters
  over a deque backend `D` (defaulting to `ArrayDeque<T>`). Every member
  delegates to a private `D deque_` member.

`pop_front()` and `pop_back()` on both backends, and `push()`/`pop()` on
both adapters, return `true` on success or `false` and no-op on an empty
deque/stack/queue -- the same bool-return, no-exceptions contract style
used in `linked-list-from-scratch`. `front()` and `back()` are only ever
called when the container is non-empty, also matching that assignment's
contract.

The full declarations, with the exact contract for each function, are
documented as comments in each header. Do not change any function
signature.

---

## Files

| File | Purpose |
|------|---------|
| `array_deque.hpp` | Declarations for `ArrayDeque<T>` -- implement every member here |
| `list_deque.hpp` | Declarations for `ListDeque<T>` -- implement every member here |
| `stack_queue.hpp` | Declarations for `Stack<T, D>` and `Queue<T, D>` -- implement every member here |

## Compilation and Testing

```bash
cd visible-tests
mkdir build && cd build
cmake .. -DSUBMISSION_DIR=<path-to-your-submission-directory>
cmake --build .
./deque-two-ways_tests
```

Run under AddressSanitizer while developing to catch out-of-bounds writes
and double-frees early:

```bash
g++ -std=c++17 -fsanitize=address -g -I. your_test.cpp -o test && ./test
```

---

## Constraints

- Do not use `std::vector`, `std::deque`, or `std::list` anywhere in
  `array_deque.hpp` or `list_deque.hpp`. Build the storage yourself.
- Do not use exceptions (`throw`/`try`/`catch`) anywhere in any of the
  three files.
- Do not modify the public interface (function signatures) declared in any
  of the three files.
- `pop_front()` and `pop_back()` on `ArrayDeque<T>` must be O(1). A
  `pop_front()` that shifts every remaining element left does not meet the
  assignment's requirements even though it produces correct answers -- see
  Background above, and see Grading below for how this is checked.
- Every member of `Stack<T, D>` and `Queue<T, D>` must delegate to the
  private `deque_` member. Do not add any other storage or reimplement
  push/pop logic independently of `deque_`.

---

## Grading

| Component | Points |
|-----------|--------|
| Source constraints (no `std::vector`/`std::deque`/`std::list`) | 10 |
| Compilation | 0 |
| Visible correctness (Catch2) | 25 |
| Hidden correctness (Catch2) | 35 |
| `pop_front` performance (O(1), not O(n)) | 10 |
| Memory safety (Valgrind, visible) | 5 |
| Memory safety (Valgrind, hidden) | 5 |
| Memory safety (ASan, visible) | 5 |
| Memory safety (ASan, hidden) | 5 |
| **Total** | **100** |

The performance component runs a long sequence of interleaved
`push_back`/`pop_front` calls that keep the deque at a fixed, non-trivial
size and checks that the whole sequence finishes inside a generous time
budget. A correct O(1) circular-buffer `pop_front` finishes in a small
fraction of that budget; an O(n) shifting `pop_front` does not, even though
it would pass every correctness test above it.

## Submission

Submit three files: `array_deque.hpp`, `list_deque.hpp`, and
`stack_queue.hpp`. Do not rename them.

## Going further

- Read about how `std::deque`'s real implementation works: it is not one
  contiguous array or one linked list, but a "block map" -- an array of
  pointers to fixed-size chunks of elements. Why might the standard library
  prefer that over a single circular array like this assignment's
  `ArrayDeque<T>`? (Hint: think about what happens to existing element
  addresses when a `std::vector`-style circular array grows, versus what
  happens to a `std::deque`'s block map.)
- Benchmark `ArrayDeque<int>` against `ListDeque<int>` for a simple
  operation like "push one million elements, then pop them all" using
  `std::chrono`. Both are the same Big-O complexity for this workload --
  does one still run meaningfully faster in practice? What does that tell
  you about the locality tradeoff discussed above?
- Extend `Stack<T, D>` or `Queue<T, D>` with a `swap` member that exchanges
  two adapters' contents. Can you implement it in O(1) by delegating to a
  `swap` on the underlying deque, rather than copying elements?
