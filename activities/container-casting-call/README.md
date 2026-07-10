# Activity: Container Casting Call

`std::vector` and `std::array` were the two containers of row 7 (Standard
Library Types) -- you already know their storage model cold. This row adds
two new ones, `std::list` and `std::forward_list`, and this activity is
about the decision that comes next: given a workload description, which
standard library sequence container -- `std::vector`, `std::deque`,
`std::list`, `std::forward_list`, or `std::array` -- actually fits? No code
to trace here, just eight scenarios and the reasoning behind each right
answer, weighted toward the two containers that are new to you.

## Concepts covered

- `std::list`'s two real superpowers: O(1) `splice` between positions or
  containers, and iterators/references to OTHER elements that survive an
  insertion or erasure anywhere else in the list
- `std::forward_list` as the frugal, forward-only option -- one pointer per
  node instead of two, no `size()` member, `insert_after`/`before_begin()`
  as its positional API
- The honest case where `std::list` still loses: a hot loop that touches
  every element far more often than it splices, where cache locality wins
  (a callback to the list-tradeoff-tribunal activity)
- `std::vector` and `std::array` as the row-7 defaults, mentioned here to
  keep the full container picture in view -- `std::vector` remains the
  correct default sequence container
- `std::deque` for fast, stable growth at both the front and the back, and
  what it actually stores internally (a map of fixed-size blocks, not one
  contiguous array)

## How it works

Each question describes a workload -- what gets inserted, how often, where,
and how the data is read back -- and asks which container fits best. Type
the exact container name (or exact phrase, for the internal-structure
question) requested by the prompt. Getting a question wrong shows you a
detailed explanation of why your answer doesn't fit and what does; answer
every question correctly to reveal the passphrase.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly answered all eight scenarios and the launcher prints
the activity's passphrase.

## Hints

<details>
<summary>Hint 1 -- ask "is this size fixed at compile time?" first</summary>

If the answer is yes -- a truly fixed count, known while you are writing
the code, that never grows or shrinks -- the container is almost always
`std::array`. If the count is a runtime quantity (even if it happens to
stay small), keep reading the other requirements.

</details>

<details>
<summary>Hint 2 -- default to std::vector unless a specific requirement says otherwise</summary>

`std::vector` remains the right default outside a specific requirement --
that has not changed since row 7. Only reach past it when the scenario
specifically needs fast front-insertion (`std::deque`), a fixed
compile-time count (`std::array`), or, this row's new territory, cheap
splicing / iterator stability across unrelated edits (`std::list`), or a
forward-only, no-`size()`, minimal-per-node-overhead walk
(`std::forward_list`).

</details>

<details>
<summary>Hint 3 -- std::list and std::forward_list are not interchangeable</summary>

Both give you node stability (an element, once inserted, keeps its address
and its iterators stay valid until that specific element is erased). The
difference is which direction you can walk and what each node costs:
`std::list` stores `next` AND `prev` per node and can splice from an
arbitrary position on its own; `std::forward_list` stores only `next`,
saving memory, but can only insert/erase relative to a position it is
already holding (`insert_after`/`erase_after`), and has no `size()` at all.

</details>

## Going further

- Write a tiny benchmark comparing `std::vector::insert(begin(), value)`
  (front insertion) against `std::deque::push_front` for a few hundred
  thousand elements. How much does the gap widen as the count grows?
- Look up how `std::deque`'s block size is typically chosen by real
  standard library implementations (libstdc++, libc++). Why might a very
  small element type change that choice?
- Modify one of the "either works" style scenarios from the
  `list-tradeoff-tribunal` activity into a fourth-container decision: does
  adding `std::deque` or `std::array` as an option change the answer?
