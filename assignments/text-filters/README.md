# Text Filters

A text filter takes a string and returns a transformed string: uppercase it,
trim it, censor a word in it. There are two completely different ways to
write code that works with "any filter" in C++, and this assignment asks you
to build the same four filters both ways so you can see the contrast
directly.

---

## Overview

In Part 1 you define a pure-virtual interface, `TextFilter`, and four classes
that inherit from it. Code that wants to work with "any filter" takes a
`const TextFilter*` and calls `apply()` on it. Which `apply()` actually runs
is decided at runtime, by looking up the object's vtable (a hidden table of
function pointers the compiler attaches to every object of a class with
virtual functions, used to find the correct override) -- this is runtime
polymorphism ("polymorphism" means one piece of calling code can work with
several different concrete types), the same mechanism you used in the
inheritance assignment.

In Part 2 you write function templates -- functions written once against a
placeholder type name (here called `F`) instead of a fixed type, where the
compiler generates a separate real function for each concrete type the
template is actually used with -- that do the same kind of work: apply a
filter, apply several filters, check a property of a filter. The functions
never mention `TextFilter` at all. They just call `f.apply(s)`
on whatever type `F` happens to be. If that expression compiles, the
template compiles. This is duck typing: "if it walks like a filter and
quacks like a filter, it's a filter" -- resolved entirely at compile time,
with no shared base class required.

## Learning goals

- Implement a pure-virtual interface and multiple classes that override it
- Understand that virtual dispatch looks up the correct override at runtime
  through the vtable, and that this requires an inheritance relationship
- Write function templates that operate on "any type with the right method,"
  with no common base class
- Understand that template instantiation (the compiler generating one
  concrete function from a template for a specific type) happens at compile
  time: the compiler only checks that the expressions inside the template
  body compile for the type it is instantiated with
- Compare the two approaches on the same problem and recognize when each is
  the better tool

## Background

Consider a function that reverses two ways to "work with any filter":

```cpp
// Runtime polymorphism: works through a common base class.
std::string run(const TextFilter& f, const std::string& s) {
    return f.apply(s);
}
```

`run` takes a reference to the base class. At the call site, the compiler
generates code that looks up `apply` in the object's vtable at runtime and
calls whichever override actually lives there. `f` could be a
`UppercaseFilter`, a `CensorFilter`, or any other class that inherits from
`TextFilter` -- `run` does not need to be recompiled or even know those
classes exist. The cost is that every such class must inherit from
`TextFilter`, and every call goes through one extra pointer indirection (the
vtable lookup).

```cpp
// Compile-time polymorphism: works through duck typing.
template <typename F>
std::string run(const F& f, const std::string& s) {
    return f.apply(s);
}
```

This `run` never mentions `TextFilter`. When you write `run(my_filter, s)`,
the compiler substitutes the actual type of `my_filter` for `F` and tries to
compile the resulting function. If `my_filter.apply(s)` is a valid
expression, it compiles -- no matter what `my_filter`'s type is or what it
inherits from. Two unrelated classes that both happen to define `apply()`
can both be passed to this `run`, even though neither one inherits from the
other or from any shared interface. The cost is that each distinct type you
call `run` with causes the compiler to generate a separate copy of the
function, and if the expression inside doesn't compile for some type, you
find out only when you try to instantiate the template with that type.

Both versions solve the same problem. The interface version needs the
inheritance relationship to exist ahead of time; the template version needs
nothing but the expression to compile. This assignment asks you to build
both so the contrast is something you have written, not just read about.

---

## Examples at a glance

To make every filter concrete, here is **one** sample string, run through
every function this assignment asks you to build. The sample has leading and
trailing spaces, an interior double space, a comma and a period, and both
lowercase and uppercase copies of the word "cat" -- on purpose, so every
filter's edge-case behavior shows up somewhere in the table.

Leading/trailing/doubled spaces would otherwise be invisible (or collapsed
by markdown) if written as plain text, so every string below is wrapped in
backticks (an inline code span); GitHub-flavored markdown preserves spaces
exactly inside a code span, so what you see between the backticks is exactly
what the function returns, space for space.

The sample string, call it `s`:

`"  The cat sat,  the CAT ran.  "`

| Call | Returns | Why |
|------|---------|-----|
| `UppercaseFilter().apply(s)` | `"  THE CAT SAT,  THE CAT RAN.  "` | every letter is uppercased; spaces, the comma, and the period are not alphabetic, so they pass through unchanged |
| `TrimFilter().apply(s)` | `"The cat sat,  the CAT ran."` | only the leading and trailing whitespace is removed; the interior double space (after the comma) is not at either end, so it is left alone |
| `CensorFilter("cat").apply(s)` | `"  The *** sat,  the CAT ran.  "` | `CensorFilter` matches the literal characters `"cat"` -- it finds the lowercase `cat` and replaces it with three asterisks, but leaves the uppercase `CAT` alone because `"CAT" != "cat"` |
| `SqueezeSpacesFilter().apply(s)` | `" The cat sat, the CAT ran. "` | every run of two or more consecutive `' '` characters collapses to exactly one space -- both the leading pair and the interior pair shrink to one space each; the trailing pair also shrinks to one. Nothing is trimmed, so one leading and one trailing space remain |
| `apply_filters(s, {trim, sq, up, cen})` | `"THE CAT SAT, THE CAT RAN."` | filters run in the order given: `trim` strips the ends, `sq` squeezes the interior double space, `up` uppercases everything -- and only THEN does `cen` run, by which point the string is already all-uppercase, so `CensorFilter("cat")` finds no lowercase `"cat"` left to censor. Order changes the outcome |
| `apply_twice(s, TrimFilter{})` | `"The cat sat,  the CAT ran."` | identical to trimming once: after the first trim there is no more leading/trailing whitespace for the second pass to remove |
| `is_idempotent(s, TrimFilter{})` | `true` | applying `TrimFilter` twice gives the same string as applying it once, for the reason above |
| `CensorFilter("").apply(s)` | `"  The cat sat,  the CAT ran.  "` | the word to censor is empty, and the spec says an empty word leaves the input unchanged |
| `apply_filters(s, {})` | `"  The cat sat,  the CAT ran.  "` | an empty filter list returns the input unchanged |

## Worked example: watch `apply_filters(s, {trim, sq, up, cen})` run, step by step

This is the example above that most surprises people, so here is every
intermediate string spelled out. `apply_filters` feeds the result of each
filter into the next, in list order: `trim`, then `sq` (`SqueezeSpacesFilter`),
then `up` (`UppercaseFilter`), then `cen` (`CensorFilter("cat")`).

| Step | Filter applied | Result after this step | Why |
|------|-----------------|-------------------------|-----|
| start | -- | `"  The cat sat,  the CAT ran.  "` | the original sample string |
| 1 | `trim` | `"The cat sat,  the CAT ran."` | leading and trailing whitespace removed; the interior double space survives because it isn't at either end |
| 2 | `sq` | `"The cat sat, the CAT ran."` | the one remaining run of consecutive spaces (after the comma) collapses to a single space |
| 3 | `up` | `"THE CAT SAT, THE CAT RAN."` | every letter, in both the lowercase and uppercase copies of "cat", becomes uppercase; punctuation and spaces are untouched |
| 4 | `cen` | `"THE CAT SAT, THE CAT RAN."` | unchanged! `CensorFilter("cat")` searches for the literal substring `"cat"` (lowercase), but step 3 already uppercased every letter, so no lowercase `"cat"` exists anywhere in the string for it to find |

Final result: **`"THE CAT SAT, THE CAT RAN."`**

Notice that running the exact same four filters in a different order (say,
censoring before uppercasing) would produce a different final string --
`apply_filters` does not know or care what each filter does, it just feeds
each filter's output into the next one, in the order you gave it.

---

## Task

Implement everything declared in `text_filters.hpp` inside that same file.

### Part 1 -- interface (runtime polymorphism)

```cpp
class TextFilter {
public:
    virtual ~TextFilter() = default;
    virtual std::string apply(const std::string& s) const = 0;
};
```

Implement four classes that inherit from `TextFilter`:

- `UppercaseFilter` -- converts every alphabetic character to uppercase.
  Non-alphabetic characters are left unchanged.
  *Examples:* `UppercaseFilter().apply("hello, World!") == "HELLO, WORLD!"`;
  `UppercaseFilter().apply("!!! ,,, ???") == "!!! ,,, ???"` (no letters, so
  nothing changes); `UppercaseFilter().apply("") == ""`.
- `TrimFilter` -- removes leading and trailing whitespace. Interior
  whitespace is left unchanged. Whitespace is any character for which
  `std::isspace` returns true.
  *Examples:* `TrimFilter().apply("  hi  there  ") == "hi  there"` (only the
  ends are trimmed; the interior double space stays); `TrimFilter().apply("
  ") == ""` (a string that is entirely whitespace trims down to nothing);
  `TrimFilter().apply("") == ""`.
- `CensorFilter(std::string word)` -- stores `word` in the constructor.
  `apply()` replaces every non-overlapping occurrence of `word` with
  asterisks of the same length, scanning left to right. If `word` is empty,
  `apply()` returns the input unchanged.
  *Examples:* `CensorFilter("cat").apply("catcat") == "******"` (two
  back-to-back, non-overlapping matches, each replaced independently);
  `CensorFilter("cat").apply("the CAT sat") == "the CAT sat"` (matching is
  case-sensitive, so an uppercase `CAT` is not touched by a lowercase
  `"cat"` filter); `CensorFilter("").apply("anything") == "anything"` (empty
  word means no censoring at all).
- `SqueezeSpacesFilter` -- collapses every run of two or more consecutive
  space characters (`' '`) into a single space. Tabs, newlines, and other
  whitespace are left unchanged, and single spaces are left unchanged.
  *Examples:* `SqueezeSpacesFilter().apply("a   b") == "a b"`;
  `SqueezeSpacesFilter().apply("a\t\tb   c") == "a\t\tb c"` (tabs are not
  spaces, so the `\t\t` run is left exactly as-is while the three-space run
  collapses); `SqueezeSpacesFilter().apply("!!!   ???") == "!!! ???"`
  (works on punctuation-only strings too, since it only ever looks at
  spaces).

Also implement:

```cpp
std::string apply_filters(const std::string& s,
                           const std::vector<const TextFilter*>& filters);
```

`apply_filters` applies each filter in `filters` to the running result, in
order, and returns the final string. `filters` holds non-owning pointers --
the caller keeps ownership of the filter objects, and `apply_filters` must
not call `new` or `delete`. An empty `filters` vector returns `s` unchanged.

*Examples:* with `TrimFilter trim;` and `UppercaseFilter up;`,
`apply_filters("  hello  ", {&trim, &up}) == "HELLO"`; reversing the order,
`apply_filters("  hello  ", {&up, &trim}) == "HELLO"` too, since trimming
whitespace and uppercasing letters don't interfere with each other here;
`apply_filters("anything", {}) == "anything"` (empty filter list).

### Part 2 -- templates (compile-time polymorphism)

Implement three function templates. None of them may mention `TextFilter`,
`UppercaseFilter`, or any of the other Part 1 classes by name -- they must
work purely off of the expression `f.apply(...)` compiling for whatever type
`F` is.

```cpp
template <typename F>
std::string apply_twice(const std::string& s, const F& f);
```

Returns `f.apply(f.apply(s))`.

*Examples:* `apply_twice("a     b", SqueezeSpacesFilter{}) == "a b"` (one pass
already collapses the whole run, so the second pass has nothing left to do);
`apply_twice("  hi  ", TrimFilter{}) == "hi"` (same reasoning: after the
first trim there is no more whitespace at the ends for the second trim to
remove); `apply_twice("", UppercaseFilter{}) == ""`.

```cpp
template <typename F>
std::string apply_all(const std::string& s, const std::vector<F>& filters);
```

Applies every filter in `filters` (all of the same type `F`) to the running
result, in order, and returns the final string. An empty `filters` vector
returns `s` unchanged. Note the difference from `apply_filters`:
`apply_filters` takes a vector of pointers to a common base class, so it can
hold different filter types in one container; `apply_all` takes a vector of
`F` by value, so every element must be the exact same type, and that type
never needs to inherit from anything.

*Examples:* `apply_all("a   b", std::vector<SqueezeSpacesFilter>{SqueezeSpacesFilter{}, SqueezeSpacesFilter{}})
== "a b"` (running the same idempotent filter twice in the vector produces
the same result as running it once); `apply_all("anything", std::vector<UppercaseFilter>{}) == "anything"`
(empty filter vector).

```cpp
template <typename F>
bool is_idempotent(const std::string& s, const F& f);
```

Returns `true` if applying `f` to `s` twice gives the same result as
applying it once (`f.apply(f.apply(s)) == f.apply(s)`), `false` otherwise.
Applying a filter twice and getting the same result as applying it once is
called being **idempotent**.

`F` can be any type with a method `std::string apply(const std::string&)
const` -- it does not need to inherit from `TextFilter`. The hidden test
suite instantiates these templates with a small struct defined only in the
test file to confirm this.

*Examples:* `is_idempotent("  hi  ", TrimFilter{}) == true` (trimming twice
never removes more than trimming once); `is_idempotent("a   b", SqueezeSpacesFilter{}) == true`
(same idea: once every run of spaces is down to one space, squeezing again
changes nothing). Note that all four Part 1 filters happen to be idempotent
on every input, for reasons specific to what each one does -- `is_idempotent`
itself does not know that; it only ever calls `apply` twice and compares.
The hidden tests exercise a custom, non-idempotent `apply()` (defined only in
the test file) to confirm the function correctly reports `false` too.

## Files

| File | Purpose |
|------|---------|
| `text_filters.hpp` | The file you edit; contains declarations and your implementations |
| `visible-tests/test_catch.cpp` | Visible Catch2 tests you can run locally |

## Compilation and Testing

```bash
mkdir build && cd build
cmake .. -DSUBMISSION_DIR=<path-to-your-submission>
cmake --build .
./text-filters_tests
```

The `SUBMISSION_DIR` variable tells CMake where to find your
`text_filters.hpp`.

## Constraints

- Do not modify the class or function signatures in `text_filters.hpp`.
- Do not use `new`, `delete`, or `throw` anywhere in this file.
- Do not use lambdas.
- `apply_filters`, `apply_twice`, and `apply_all` must not mutate the
  filter objects they are given -- take them by `const` reference or
  `const` pointer, matching the declared signatures.

---

## Grading

| Component | Points |
|-----------|--------|
| Compilation | 0 (required to proceed) |
| No `new`/`delete`/`throw` (source check) | 10 |
| Visible tests (Catch2) | 30 |
| Hidden tests (Catch2) | 60 |
| **Total** | **100** |

## Submission

Submit a single file named `text_filters.hpp`. Do not rename it.

---

## Going further

- Add a fifth filter, `ReverseFilter`, that reverses the characters of the
  string. Add it to both a `TextFilter*` vector and an `apply_all` call and
  confirm both still compile and run.
- Chain filters by composition: write a `CompositeFilter` that itself
  inherits from `TextFilter`, stores a `std::vector<const TextFilter*>` in
  its constructor, and applies them all in its own `apply()`. Now a
  `CompositeFilter*` can be passed anywhere a `TextFilter*` is expected --
  what does that buy you?
- Look up `std::function<std::string(const std::string&)>`. Could you
  replace `std::vector<const TextFilter*>` in `apply_filters` with a
  `std::vector<std::function<std::string(const std::string&)>>`? What would
  you gain, and what would you lose, compared to the interface version?
- Try calling `apply_twice` with a plain struct that has an `apply()` method
  but does not inherit from `TextFilter`. Then try calling `apply_filters`
  with a pointer to that same struct. One compiles and one does not --
  explain why in terms of what each function actually requires from its
  argument.
