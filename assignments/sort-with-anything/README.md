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

- `sort_by(v, cmp)` -> `void` -- sorts `v` in place using merge sort,
  ordering elements according to `cmp` (see the comparator contract
  above). Must be **stable**. Must run in O(n log n) time. `Compare` may
  be a free function, a functor, or a lambda.
- `by_length_asc(a, b)` -> `bool` -- a FREE FUNCTION comparator: orders
  `std::string`s by ascending length.
- `ByAbsoluteValue` -- a FUNCTOR: `operator()(int a, int b)` orders ints
  by ascending absolute value. On a tie in absolute value, the smaller
  ACTUAL value comes first (e.g. `-3` belongs before `3`, since `-3 < 3`,
  even though both have absolute value `3`).
- `filter(v, keep)` -> `std::vector<T>` -- returns a new vector containing
  every element of `v` for which `keep(element)` is `true`, in original
  relative order. Does not modify `v`.
- `for_each_apply(v, f)` -> `void` -- applies `f` to every element of `v`
  IN PLACE: `f` takes a `T&` and mutates it directly.
- `count_matching(v, pred)` -> `std::size_t` -- returns how many elements
  of `v` satisfy `pred(element)`. Does not modify `v`.

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
