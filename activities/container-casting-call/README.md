# Activity: Container Casting Call

You have already built your own dynamic array and your own circular buffer
by hand, so you know exactly what `std::vector` and `std::deque` are doing
underneath. This activity is about the decision that comes next: given a
workload description, which standard library sequence container --
`std::vector`, `std::deque`, `std::list`, or `std::array` -- actually fits?
No code to trace here, just eleven scenarios and the reasoning behind each
right answer.

## Concepts covered

- `std::vector` as the correct default sequence container, and recognizing
  when a scenario has no requirement that points elsewhere
- `std::array` for a size that is a compile-time constant, never a runtime
  quantity
- `std::deque` for fast, stable growth at both the front and the back
- The rare, honest case where `std::list` wins: splice-heavy workloads with
  saved iterators that must survive unrelated insertions
- What `std::deque` actually stores internally (a map of fixed-size blocks,
  not one contiguous array) and why that design gives O(1) operations at
  both ends without ever moving existing elements

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

You have correctly answered all eleven scenarios and the launcher prints
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

`std::vector` is the right answer more often than any other container in
this activity, on purpose -- it mirrors real-world usage. Only reach past
it when the scenario specifically needs fast front-insertion (`std::deque`),
cheap splicing with iterator stability (`std::list`), or a fixed compile-time
count (`std::array`).

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
