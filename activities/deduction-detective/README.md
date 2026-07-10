# Activity: Deduction Detective

`auto` lets the compiler figure out a variable's type from its
initializer, instead of you writing the type out by hand. That sounds
purely convenient -- and mostly it is -- but `auto` follows one
specific, learnable rule that surprises almost everyone the first time
it bites: it deduces the **value type**, stripped of any reference and
any top-level `const`, no matter what the initializer expression's own
type actually was. This activity is a series of "what type does this
deduce to?" questions built to make that rule, and its consequences,
impossible to forget.

## Background

The mental model this whole activity is built around: **`auto` strips,
then you re-qualify.** Given some initializer expression, `auto` first
figures out its underlying value type -- with any reference-ness and
any top-level `const` removed -- and that stripped-down type is what
gets assigned to your variable. If you actually wanted a reference, or
wanted to keep the `const`, you have to write `auto&` or `const auto&`
yourself; `auto` never adds those back on its own.

"Top-level `const`" specifically means a `const` that applies directly
to the variable itself (`const int cx`), as opposed to a `const`
reached through a pointer or reference to something else (`const int*
p` -- `p` itself is not const, only the `int` it points to is). Only
top-level `const` gets stripped by `auto`.

`decltype(expr)` is a completely different tool that this activity
touches on once for contrast: applied to a plain existing variable
name, it reproduces that variable's EXACT declared type, with nothing
stripped at all -- the opposite instinct from `auto`.

## Concepts covered

- `auto`'s basic deduction from integer, floating-point, and string
  literals (including the classic `const char*` trap on string
  literals)
- `auto` dropping a function's reference return type, and `auto&` as
  the fix
- `auto` stripping top-level `const`, and `const auto&` as the fix
- `auto` deducing `std::pair<const K, V>` in a range-for over a
  `std::map`, and the resulting copy trap
- `decltype(expr)` vs. `auto` on the same variable
- `auto*` for pointer-typed declarations

## How it works

Each question shows a short code fragment and asks what type `auto`
(or, once, `decltype`) deduces for a specific variable. Type your
answer exactly as the prompt specifies -- a C++ type name, written the
way you would write it in a declaration. Getting a question wrong
shows a detailed explanation of the deduction rule you missed; answer
every question correctly to reveal the passphrase.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have answered every question correctly and the launcher prints
the passphrase.

## Hints

<details>
<summary>Hint 1 -- the strip-then-requalify rule</summary>

For any `auto` declaration, first figure out the initializer
expression's OWN type. Then strip off any reference-ness and any
top-level `const` -- what remains is what plain `auto` deduces. If the
declaration itself also writes `&` or `const` (as in `auto&` or
`const auto&`), add those back on top of the stripped type; that
combination is the variable's real, final type.

</details>

<details>
<summary>Hint 2 -- string literals are never std::string</summary>

A double-quoted literal like `"hi"` has type `const char[3]` (counting
the null terminator), which decays to `const char*` when used to
initialize a pointer-compatible variable. It never becomes
`std::string` unless something explicitly converts it -- an `s`
suffix from `<string>`, or an explicit `std::string(...)` call. `auto`
just reports whatever type the initializer expression actually has;
it never upgrades a raw string literal into a friendlier container
type for you.

</details>

<details>
<summary>Hint 3 -- what a std::map actually stores</summary>

`std::map<K, V>` stores each element as `std::pair<const K, V>` -- the
key half is permanently `const` so a key can never be mutated in place
and silently corrupt the map's sorted internal ordering. Whatever
`auto` deduces for a range-for variable over a map always keeps that
`const K`, whether or not you also add `&`.

</details>

## Going further

- Compile one of this activity's function-returning-a-reference
  snippets for real, print the address of both the original object
  and your `auto`-deduced copy with `&`, and confirm they differ (while
  an `auto&` version's address matches).
- Try `auto` on a `const std::vector<int>&` parameter inside a
  function body -- what type does a plain `auto x = v[0];` deduce
  compared to `auto& x = v[0];`, given that `v` itself is a
  const-reference parameter?
- Look up C++14's generalized `decltype(auto)`. What problem does it
  solve that plain `auto` cannot, and how does it relate to the
  `decltype(expr)` question in this activity?
