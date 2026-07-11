# Sort With Anything

In sort-suite, `merge_sort` only ever sorted `int`s in ascending order --
the comparison (`<`) was baked directly into the algorithm. This
assignment removes that restriction: you will generalize your merge sort
into a **template** that accepts a **comparator** as an argument, so the
exact same algorithm works with ANY of the three species of callable you
learned about in callable-lineup and capture-court: a **free function**, a
**functor**, or a **lambda**. This is the entire payoff of learning what a
callable is -- one algorithm, written once, that works with any comparison
rule a caller wants to plug in.

---

## The three callable species, side by side

All three of these call the exact same `sort_by` template. `sort_by`
itself never knows or cares which one it was handed:

```cpp
// 1. FREE FUNCTION
bool by_length_asc(const std::string& a, const std::string& b) {
    return a.size() < b.size();
}
sort_by(words, by_length_asc);

// 2. FUNCTOR -- a struct with operator()
struct ByAbsoluteValue {
    bool operator()(int a, int b) const { /* ... */ }
};
sort_by(numbers, ByAbsoluteValue{});

// 3. LAMBDA -- written inline, right where it is used
sort_by(numbers, [](int a, int b) { return a > b; });   // descending
```

`sort_by`'s own code is written exactly once. It works with all three
calls above because C++ templates do not require the comparator to be any
particular named TYPE -- they only require that the expression `cmp(a, b)`
compiles and returns something usable as a `bool`. A free function, a
functor object, and a lambda's closure object are three completely
different C++ types, and `sort_by` does not care: this is sometimes called
**duck typing** at compile time ("if it can be called like `cmp(a, b)`, it
works here").

---

## Background

### Callable, defined

A **callable** is anything that can be invoked with `(...)`, the way a
function can: a plain function, a function pointer, a functor (an object
with `operator()`), or a lambda. `sort_by`'s `Compare` template parameter
can be any callable with the shape `bool cmp(const T&, const T&)`.

### The comparator contract: strict weak ordering, in beginner terms

`cmp(a, b)` must return `true` exactly when `a` belongs STRICTLY before
`b`. For `sort_by` to work correctly, `cmp` has to follow a small set of
honest rules (together called a **strict weak ordering**):

- **Consistent**: `cmp(a, b)` and `cmp(b, a)` are never both `true` at the
  same time -- `a` cannot belong both before AND after `b`.
- **Irreflexive**: `cmp(a, a)` is always `false` -- an element never
  belongs strictly before itself.
- **Never return `true` for two elements you consider equal.** If `a` and
  `b` tie on whatever key you are sorting by, `cmp(a, b)` and `cmp(b, a)`
  must BOTH be `false`. This is the rule students break most often --
  writing `<=` instead of `<` inside a comparator, for example, makes
  `cmp(a, a)` return `true`, which violates irreflexivity and can make
  `sort_by` behave incorrectly (or even loop forever, depending on how an
  algorithm uses the comparator).

If two elements tie under `cmp` (neither is "strictly before" the other),
it is `sort_by`'s job -- not the comparator's -- to decide their relative
order, and it must do so by preserving whichever order they started in.
That is exactly what **stability** means, and it is why `sort_by` is
required to be stable.

---

## Examples at a glance

Several concrete `call -> result` pairs, covering every function in this
assignment:

| Call | Result | Why |
|------|--------|-----|
| `sort_by(v = {5, 3, 8, 1, 4}, [](int a, int b) { return a < b; })` | `v` becomes `{1, 3, 4, 5, 8}` | a plain ascending lambda comparator |
| `sort_by(v = {"ccc", "a", "bb", "dddd"}, by_length_asc)` | `v` becomes `{"a", "bb", "ccc", "dddd"}` | the FREE FUNCTION comparator orders by string length |
| `sort_by(v = {3, -1, -5, 2, -2}, ByAbsoluteValue{})` | `v` becomes `{-1, -2, 2, 3, -5}` | ordered by absolute value (`1, 2, 2, 3, 5`); on the `2`/`-2` tie in absolute value, the smaller ACTUAL value (`-2`) goes first, per `ByAbsoluteValue`'s own tie rule |
| `sort_by(v = {"z", "yy", "a", "bb"}, by_length_asc)` | `v` becomes `{"z", "a", "yy", "bb"}` | two ties in length (`"z"`/`"a"` both length 1, `"yy"`/`"bb"` both length 2); STABILITY keeps each tied pair in its original relative order (`"z"` before `"a"`, `"yy"` before `"bb"`) |
| `filter(v = {1, 2, 3, 4, 5, 6}, [](int x) { return x % 2 == 0; })` | `{2, 4, 6}` | keeps only the elements the predicate accepts, in original order; `v` itself is untouched |
| `for_each_apply(v = {1, 2, 3}, [](int& x) { x *= 10; })` | `v` becomes `{10, 20, 30}` | mutates every element IN PLACE through a `T&` parameter |
| `count_matching(v = {1, 2, 3, 4, 5, 6}, [](int x) { return x > 3; })` | `3` | three elements (`4, 5, 6`) satisfy the predicate; `v` is not modified |

---

## Worked example: watch `sort_by({5, 3, 8, 1, 4}, cmp)` run, step by step

This traces exactly what the reference algorithm does for a small vector.
`sort_by` recurses with merge sort, but any range of `kSmallRunThreshold`
(16) elements or fewer is sorted directly with **insertion sort** instead
of splitting further -- a common real-world optimization, since insertion
sort beats merge sort's overhead on small ranges. Because `v` here has
only 5 elements, the whole sort is a single insertion-sort pass; no
merging happens at all. `cmp(a, b)` is `a < b` (plain ascending).

Insertion sort's idea: walk `i` from index 1 to the end, treating
everything before `i` as already-sorted, and slide the "key" (`v[i]`)
leftward past every element `cmp(key, v[j])` says the key belongs before,
until it finds its resting spot.

| `i` | `key` | Shifts (comparisons via `cmp`) | `v` after this `i` |
|-----|-------|-------------------------------|---------------------|
| start | -- | -- | `{5, 3, 8, 1, 4}` |
| 1 | `3` | `cmp(3, 5)` is true (3 < 5) -> shift `5` right; nothing left of it -> place `3` at index 0 | `{3, 5, 8, 1, 4}` |
| 2 | `8` | `cmp(8, 5)` is false (8 < 5 is false) -> stop immediately, `8` stays put | `{3, 5, 8, 1, 4}` |
| 3 | `1` | `cmp(1, 8)` true -> shift `8` right; `cmp(1, 5)` true -> shift `5` right; `cmp(1, 3)` true -> shift `3` right; nothing left -> place `1` at index 0 | `{1, 3, 5, 8, 4}` |
| 4 | `4` | `cmp(4, 8)` true -> shift `8` right; `cmp(4, 5)` true -> shift `5` right; `cmp(4, 3)` false -> stop, place `4` right after `3` | `{1, 3, 4, 5, 8}` |
| end | -- | every `i` from 1 to 4 processed | `{1, 3, 4, 5, 8}` |

The final array is `{1, 3, 4, 5, 8}` -- confirmed sorted ascending. Notice
that each shift is decided purely by calling `cmp`, never by a hardcoded
`<`: swap `cmp` for `ByAbsoluteValue{}` or any other comparator and the
exact same shifting logic sorts by a completely different rule. On a
larger vector (more than 16 elements), `sort_by` would instead split `v`
into two halves, sort each half recursively (by this same process, or
further splitting), and `_merge_by` those two already-sorted halves back
together -- taking from the left half on every tie, which is what makes
the whole algorithm stable.

### Closure and capture, recapped

If you have completed capture-court, you already know this: a **closure**
is the object a lambda expression builds at the point it is written,
bundling its compiled body together with whatever it **captured** from
the surrounding scope. `[x]` captures `x` by value (a frozen copy);
`[&x]` captures `x` by reference (a live link to the original). None of
`sort_by`'s test lambdas need to capture anything at all -- they only use
their own parameters -- but you are free to write comparators that do
capture, e.g. a lambda that captures a target value and sorts by distance
from it.

### Why templates, not function pointers

You could build something like `sort_by` using a raw function pointer
parameter instead of a template (exactly the pattern `countMatching` used
in callable-lineup). The reason `sort_by` uses a template `Compare`
parameter instead: a template lets the compiler generate a specialized,
fully inlined version of `sort_by` for each different comparator type it
is called with, so a call like `sort_by(v, [](int a, int b){ return a <
b; })` can run exactly as fast as if you had hand-written that comparison
directly into the sort -- something a function pointer (an indirect call
through an address, opaque to the optimizer) generally cannot match.

---

## Task

Implement every function/template declared in `sort_with_anything.hpp`,
inside the `swa` namespace.

- **`sort_by(v, cmp)` -> `void`** -- sorts `v` in place using merge sort,
  ordering elements according to `cmp` (see the comparator contract
  above). Must be **stable**. Must run in O(n log n) time. `Compare` may
  be a free function, a functor, or a lambda.
  - **Example (lambda):** `sort_by(v = {5, 3, 8, 1, 4}, [](int a, int b) { return a < b; })` leaves `v == {1, 3, 4, 5, 8}`.
  - **Edge case (empty):** `sort_by(v = {}, cmp)` leaves **`v == {}`** (nothing to sort).
  - **Tricky case (stability):** `sort_by(v = {"z", "yy", "a", "bb"}, by_length_asc)` leaves `v == {"z", "a", "yy", "bb"}` (**length ties broken by original order**, since `sort_by` must be stable).
- **`by_length_asc(a, b)` -> `bool`** -- a FREE FUNCTION comparator: orders
  `std::string`s by ascending length.
  - **Example:** `by_length_asc("a", "bbb") == true`.
  - **Example (reversed args):** `by_length_asc("bbb", "a") == false`.
  - **Tricky case (tie):** `by_length_asc("cat", "dog") == false` (equal length 3, so **neither is "strictly before" the other** -- a tie).
- **`ByAbsoluteValue`** -- a FUNCTOR: `operator()(int a, int b)` orders ints
  by ascending absolute value. On a tie in absolute value, the smaller
  ACTUAL value comes first (e.g. `-3` belongs before `3`, since `-3 < 3`,
  even though both have absolute value `3`).
  - **Example (tie):** `ByAbsoluteValue{}(-3, 3) == true` (tied absolute values, **`-3 < 3`**).
  - **Example (reversed tie):** `ByAbsoluteValue{}(3, -3) == false` (same tie, checked the other direction).
  - **Example (no tie):** `ByAbsoluteValue{}(-5, 2) == false` (absolute value 5 is **not less than** absolute value 2, so `-5` does not belong before `2`).
- **`filter(v, keep)` -> `std::vector<T>`** -- returns a new vector containing
  every element of `v` for which `keep(element)` is `true`, in original
  relative order. Does not modify `v`.
  - **Example:** `filter(v = {1, 2, 3, 4, 5, 6}, [](int x) { return x % 2 == 0; }) == {2, 4, 6}`.
  - **Edge case (empty input):** `filter(v = {}, keep) == {}`.
  - **Edge case (no matches):** `filter(v = {1, 3, 5}, [](int x) { return x % 2 == 0; }) == {}` (**no element satisfies `keep`**, so the result is empty even though `v` is not).
- **`for_each_apply(v, f)` -> `void`** -- applies `f` to every element of `v`
  IN PLACE: `f` takes a `T&` and mutates it directly.
  - **Example:** `for_each_apply(v = {1, 2, 3}, [](int& x) { x *= 10; })` leaves `v == {10, 20, 30}`.
  - **Edge case (empty):** `for_each_apply(v = {}, f)` leaves `v == {}` (nothing to apply `f` to).
  - **Example (strings):** `for_each_apply(v = {"a", "bb"}, [](std::string& s) { s += "!"; })` leaves `v == {"a!", "bb!"}`.
- **`count_matching(v, pred)` -> `std::size_t`** -- returns how many elements
  of `v` satisfy `pred(element)`. Does not modify `v`.
  - **Example:** `count_matching(v = {1, 2, 3, 4, 5, 6}, [](int x) { return x > 3; }) == 3`.
  - **Edge case (empty):** `count_matching(v = {}, pred) == 0`.
  - **Edge case (no matches):** `count_matching(v = {1, 3, 5}, [](int x) { return x % 2 == 0; }) == 0` (**no matches** -- absent, not an error).

`filter`, `for_each_apply`, and `count_matching` all work with any of the
three callable species too, exactly like `sort_by`.

---

## Files

| File | Purpose |
|------|---------|
| `sort_with_anything.hpp` | Declarations -- implement every function here (header-only, no matching .cpp) |

## Compilation and Testing

```bash
cd visible-tests
mkdir build && cd build
cmake .. -DSUBMISSION_DIR=<path-to-your-sort_with_anything.hpp-directory>
cmake --build .
./sort-with-anything_tests
```

---

## Constraints

- Do not use exceptions (`throw`/`try`/`catch`) anywhere in
  `sort_with_anything.hpp`.
- Do not use `std::sort`, `std::stable_sort`, `std::partial_sort`, or
  `qsort` anywhere in `sort_with_anything.hpp` -- implement `sort_by`'s
  merge sort yourself. (Using `std::sort` inside your OWN tests, to build
  an expected result to compare against, is fine -- the restriction is
  scoped to `sort_with_anything.hpp` only.)
- Do not modify the public interface (function/template signatures)
  declared in `sort_with_anything.hpp`.
- `sort_by` must run in O(n log n) time -- see PerformanceTest below.
- `sort_by` must be stable -- equal-key elements (per `cmp`) must keep
  their original relative order.

---

## Grading

| Component | Points |
|-----------|--------|
| Source constraints (no `std::sort`/`std::stable_sort`/`std::partial_sort`/`qsort`, no exceptions) | 10 |
| Compilation | 0 |
| Visible correctness (Catch2) | 30 |
| Hidden correctness (Catch2) | 50 |
| `sort_by` performance (O(n log n), not quadratic) | 10 |
| **Total** | **100** |

The performance component calls `sort_by` once on a vector of 1,000,000
random integers with a lambda comparator, inside a generous time budget.
A correct O(n log n) implementation finishes comfortably inside that
budget; an implementation that is secretly quadratic does not, even
though it produces exactly the right sorted array every time.

## Submission

Submit a single file named `sort_with_anything.hpp`. Do not rename it.

## Going further

- Write a comparator that captures a target value by value and sorts a
  vector of ints by distance from that target (closest first) --
  `sort_by(v, [target](int a, int b) { return std::abs(a - target) <
  std::abs(b - target); })`.
- Add a `transform(v, f)` template that returns a NEW `std::vector<U>` by
  applying `f` (which may return a different type than it takes) to every
  element of `v`, without modifying `v`. How does its signature differ
  from `for_each_apply`'s?
- Time `sort_by` against a hand-written comparator-taking function
  pointer version (same algorithm, but `Compare` is a raw `bool
  (*)(const T&, const T&)` instead of a template parameter) on a few
  million elements. Does the template version actually run faster, and
  can you explain why from what you know about inlining?
- Use `count_matching` and `filter` together to implement a `partition`
  helper that returns BOTH the matching and non-matching elements as a
  `std::pair` of vectors, without calling either helper twice.
