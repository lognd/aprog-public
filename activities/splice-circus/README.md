# Activity: Splice Circus

Back in `linked-list-from-scratch` you built a singly linked list by hand,
with raw `Node*` pointers and manual `new`/`delete`. `std::list` is the
standard library's version of that idea, doubly linked (each node knows
both its `next` AND its `prev`), and `std::forward_list` is the standard
library's version of the singly linked list you actually built -- one
pointer per node, forward-only. This activity is the "meet std" half of
that arc: seven programs that show off what those two containers can do
that no array-backed container (`std::vector`, `std::deque`, `std::array`)
can, by predicting their exact printed output.

---

## Concepts covered

- `std::list::splice` -- moving a run of nodes from one list (or one
  position) to another in O(1), without copying a single element
- Iterators held across a `splice` staying valid: the NODE moves, not a
  copy, so a saved iterator keeps dereferencing to the same value even
  after its node has changed containers
- `std::list::sort()` as a member function, and why: `std::list` has no
  random access, so the free `std::sort` (which needs it) cannot be used
  on one at all -- the member version is a node-relinking merge sort
  instead
- `std::list::remove()` and `std::list::unique()` -- member functions that
  erase by relinking, no shifting
- `std::forward_list::before_begin()` and `insert_after()` -- the exact
  positional API you already built by hand for your own singly linked list
- `std::forward_list` having no `size()` member at all, and using
  `std::distance(begin(), end())` (an O(n) walk) as the honest way to
  count elements when you actually need to

## How it works

Each snippet is a complete, compilable C++ program. Read the code, trace
through it by hand, and type the exact output it produces -- for
multi-line output you will be prompted to enter one line at a time. The
launcher compiles and runs each program itself (with `g++ -std=c++17`) and
checks your prediction against the real, measured output. Predict every
snippet correctly to reveal the passphrase.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly predicted the output of all seven snippets and the
launcher prints the activity's passphrase.

## Hints

<details>
<summary>Hint 1 -- splice() takes a half-open range, [first, last)</summary>

Like every other standard-library range in this course, `splice(pos,
other, first, last)` moves everything from `first` up to but NOT including
`last`. If `first` is one element in and `last` is four elements in, three
elements move -- the one `first` points at, and the two after it, but not
the one `last` points at.

</details>

<details>
<summary>Hint 2 -- unique() only removes CONSECUTIVE duplicates</summary>

`unique()` is not "keep one copy of every distinct value in the whole
list" -- it only collapses a RUN of equal elements sitting next to each
other. If the same value appears again later, separated by other values in
between, that later occurrence survives as its own run. Pair `sort()` with
`unique()` first if you want full deduplication.

</details>

<details>
<summary>Hint 3 -- before_begin() is a fence post, not a real element</summary>

Just like `end()` is one position PAST the last real element and is never
itself dereferenceable, `before_begin()` is one position BEFORE the first
real element, and it is also never dereferenceable. It exists purely so
`insert_after(before_begin(), value)` can prepend to a `forward_list`
without a special case -- the same reason `end()` exists in every other
standard container's iterator interface.

</details>

## Going further

- Time (with `std::chrono`) 100,000 elements' worth of `splice` between two
  `std::list`s versus manually erasing and re-inserting the same elements
  one at a time. How much does relinking-instead-of-copying actually save?
- Implement `splice` yourself on the `LinkedList<T>` you built in
  `linked-list-from-scratch`/`linked-list-iterators`: given two lists and
  an iterator range in one of them, cut that range out and relink it into
  the other, touching only the boundary `Node*` pointers.
- Look up why `std::list::sort()` is documented as a **stable** sort
  (elements that compare equal keep their original relative order) while
  `std::sort` (used on `std::vector`) makes no such promise. What does that
  cost `std::sort` in exchange for not needing that guarantee?
