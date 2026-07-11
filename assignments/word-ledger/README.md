# Word Ledger

An **associative container** stores elements looked up by a **key** rather
than by position -- a **key** is a value used to find something, like a
word used to find its count. This assignment asks you to implement a small
text-analysis toolkit, entirely as free functions over an already
tokenized `std::vector<std::string>` of words (no file reading, no
splitting a sentence apart -- that part is done for you), exercising
three of the standard library's associative containers:
`std::map`, `std::unordered_map`, and `std::set`.

---

## Learning goals

- Choose the right associative container for a task: a **map** stores a
  key mapped to a **value** (like a word mapped to its count); a **set**
  stores keys only, with no associated value, answering pure membership
  questions
- Understand the **hash table** (average O(1) operations, no ordering) versus
  **balanced tree** (guaranteed O(log n), sorted iteration) tradeoff behind
  `std::unordered_map`/`std::unordered_set` versus `std::map`/`std::set`
- Rely on `std::map`'s and `std::set`'s guaranteed sorted-key iteration
  order to produce sorted output without a separate sort step
- Implement set operations (intersection, difference) by iterating one
  container and checking membership in another with `count()` or `find()`
- Solve a small top-k ranking problem with a repeated max-scan, without
  needing a sorting comparator, a function pointer, or a lambda

## Background

### Hash table versus balanced tree, defined from scratch

A **hash table** stores key-value pairs by running each key through a
**hash function** (a function that turns a key into a number) to pick a
**bucket** to store it in directly. Looking a key back up means hashing it
again and going straight to that bucket -- average O(1), because you never
have to search most of the container. The tradeoff: a hash table makes no
promise about what order you get elements back in when you iterate over
it. `std::unordered_map` and `std::unordered_set` are hash tables.

A **balanced tree** (typically a red-black tree) stores key-value pairs in
a tree structure that is kept balanced, so no path through it is much
longer than any other. Looking a key up means walking down the tree,
comparing at each step -- guaranteed O(log n), slower on average than a
hash table, but with a guaranteed worst case (a hash table's worst case,
when many keys collide into the same bucket, can degrade to O(n)). The
bonus: walking a balanced tree in order always visits keys in **sorted**
order. `std::map` and `std::set` are balanced trees.

### Iteration-order guarantees

- `std::map` and `std::set`: iterating always visits keys in **ascending
  sorted order**. This is a standard guarantee, not an implementation
  detail -- you can rely on it.
- `std::unordered_map` and `std::unordered_set`: iteration order is
  **unspecified**. Never write code (or a test) that depends on the exact
  order elements come out of one of these in.

This assignment picks which container each function returns specifically
so that "sorted output" functions return `std::map`/`std::set` (getting
sorted order for free) and "I only need fast lookup, order doesn't
matter" functions return `std::unordered_map`.

### Case sensitivity

Every function in this assignment treats words **case-sensitively**:
`"The"` and `"the"` are counted as two different words. Nothing lowercases
your input for you.

---

## Task

Implement every function declared in `word_ledger.hpp`, inside the
`wledger` namespace:

- `word_frequencies(words)` -> `std::map<std::string, int>` -- how many
  times each distinct word appears, sorted by word.
- `first_occurrence_index(words)` -> `std::unordered_map<std::string, int>`
  -- for each distinct word, the 0-based index of its first appearance.
  Order does not matter here, so this returns the faster hash-table-backed
  map rather than a sorted one.
- `unique_words_sorted(words)` -> `std::set<std::string>` -- every distinct
  word, in sorted order (a `std::set`'s own iteration order already gives
  you this, for free).
- `common_words(a, b)` -> `std::set<std::string>` -- the set
  **intersection**: every word that appears in both `a` and `b`.
- `words_only_in(a, b)` -> `std::set<std::string>` -- the set
  **difference**: every word in `a` that does not appear anywhere in `b`.
- `most_frequent(words, k)` -> `std::vector<std::pair<std::string, int>>`
  -- the top `k` most frequent words, ordered by count descending, with
  ties broken alphabetically ascending.

The full contract for every function -- exact return type, tie-breaking
rule, and behavior on empty input -- is documented as a comment directly
above each declaration in `word_ledger.hpp`. Do not change any function
signature.

### A note on `most_frequent`

You do not yet have lambdas or function pointers as tools, so you cannot
pass a custom comparator to `std::sort`. Instead, build the top-k list
with a **repeated max-scan**: build the frequency map once (you can reuse
`word_frequencies`), then, `k` times, scan the whole map for the
highest-count entry not yet chosen (breaking ties alphabetically), record
it, and mark it used. This is O(k * n) where n is the number of distinct
words -- perfectly fine for the small `k` values this assignment uses, and
documented here as an accepted, non-penalized approach.

---

## Files

| File | Purpose |
|------|---------|
| `word_ledger.hpp` | Declarations -- implement every function here (header-only, no matching .cpp) |

## Compilation and Testing

```bash
cd visible-tests
mkdir build && cd build
cmake .. -DSUBMISSION_DIR=<path-to-your-word_ledger.hpp-directory>
cmake --build .
./word-ledger_tests
```

---

## Constraints

- Do not use exceptions (`throw`/`try`/`catch`) anywhere in
  `word_ledger.hpp`.
- Do not modify the public interface (function signatures) declared in
  `word_ledger.hpp`.
- Do not lowercase, trim, or otherwise transform input words -- comparisons
  are case-sensitive by design.

---

## Grading

| Component | Points |
|-----------|--------|
| Compilation | 0 |
| Visible correctness (Catch2) | 30 |
| Hidden correctness (Catch2) | 70 |
| **Total** | **100** |

## Submission

Submit a single file named `word_ledger.hpp`. Do not rename it.

## Going further

- Implement a `word_frequencies_fast` variant returning
  `std::unordered_map<std::string, int>` instead, and benchmark it against
  `word_frequencies` for a large input. How much does giving up sorted
  order actually save?
- Extend `most_frequent` to accept a custom minimum-count threshold,
  ignoring words that appear fewer than that many times.
- Look up `std::set_intersection` and `std::set_difference` from
  `<algorithm>`, which work on any sorted range. Could you use one of them
  to implement `common_words` or `words_only_in` more directly? What
  precondition would you need to satisfy first?
