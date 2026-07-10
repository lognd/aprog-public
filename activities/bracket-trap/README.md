# Activity: Bracket Trap

`std::map` and `std::unordered_map`'s `operator[]` has a surprise built
into it: reading a key that does not exist with `operator[]` silently
**inserts** a default-constructed value for that key. This activity traces
that trap directly, alongside the operations that never insert
(`count()`, `find()`), `std::map`'s guaranteed sorted iteration order, and
the difference between `insert()` (keeps an existing value) and `operator[]`
used as an assignment (always overwrites).

## Concepts covered

- `operator[]` on a missing key inserting a default value (0 for `int`) as
  a side effect, even when it looks like a plain read
- `count()` and `find()` as the safe, non-inserting ways to check for a key
- `std::map`'s guaranteed sorted-key iteration order versus
  `std::unordered_map`'s unspecified order
- `erase()`'s return value reporting how many elements were actually
  removed (0 or 1, since keys are unique)
- `insert()` leaving an existing key's value untouched versus `operator[]`
  always overwriting it

## How it works

Each snippet is a complete, compilable C++ program manipulating a
`std::map` or `std::unordered_map`. Read the code, trace through it by
hand, and type the exact output it prints -- for multi-line output you
will be prompted to enter one line at a time. The launcher compiles and
runs each program itself and checks your prediction against the real,
measured output. Predict every snippet correctly to reveal the passphrase.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly predicted the output of all six snippets and the
launcher prints the activity's passphrase.

## Hints

<details>
<summary>Hint 1 -- any bare operator[] on a map is a potential insert</summary>

Whenever you see `m[key]` anywhere -- inside a `printf`, an `if`, or an
assignment's right-hand side -- ask whether `key` is already known to be
present. If you're not sure, `operator[]` just made sure for you, by
inserting it.

</details>

<details>
<summary>Hint 2 -- unordered_map's element order is never something to predict</summary>

Every snippet using `std::unordered_map` in this activity asks about
`size()`, `count()`, or an order-independent aggregate (like a sum) -- never
the exact printed order of its elements, because the standard does not
guarantee one.

</details>

## Going further

- Write a function that "safely" reads a value from a `const std::map<K, V>&`
  (a reference the function cannot modify) for a possibly-missing key. Why
  does `operator[]` not even compile there, and what do you have to use
  instead?
- Look up `std::map::emplace` and `try_emplace`. How do they compare to
  `insert()` for avoiding an unnecessary temporary value?
- Modify the sorted-iteration snippet (snippet 3) to use `std::greater<std::string>`
  as `std::map`'s comparator template argument. Predict, then verify, how
  the iteration order changes.
