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
your input for you. A consequence students often trip on: `std::map`'s
"sorted order" means sorted by **byte value** (ASCII), not dictionary
order, and every uppercase letter has a SMALLER ASCII value than every
lowercase letter (`'A'` is 65, `'a'` is 97). So a word starting with an
uppercase letter, like `"Cat"`, sorts BEFORE every word starting with a
lowercase letter, including `"bird"` -- `"Cat"` is not anywhere near where
a dictionary would put it. See the worked example below for this exact
case.

---

## Examples at a glance

To make all six functions concrete, here is **one** representative input,
`words`, with what every function returns for it. Read this table first
-- it is the whole assignment in miniature.

```
 index:  0      1      2      3       4      5      6
 words = {"cat", "dog", "cat", "bird", "dog", "cat", "Cat"}
```

A second vector, `b = {"dog", "fish", "dog"}`, is used for the two
functions that take two inputs.

| Call | Returns | Why |
|------|---------|-----|
| `word_frequencies(words)` | `{"Cat": 1, "bird": 1, "cat": 3, "dog": 2}` | `std::map` sorts keys by ASCII value, not dictionary order -- uppercase `"Cat"` (`'C'` = 67) sorts BEFORE lowercase `"bird"` (`'b'` = 98), even though a dictionary would put `bird` first |
| `first_occurrence_index(words)` | `{"cat": 0, "dog": 1, "bird": 3, "Cat": 6}` (some order) | this returns `std::unordered_map`, whose iteration order is unspecified -- do not rely on any particular order, only on the values stored for each key |
| `unique_words_sorted(words)` | `{"Cat", "bird", "cat", "dog"}` | same ASCII-before-dictionary-order surprise as `word_frequencies` -- `"Cat"` and `"cat"` are two different keys, and `"Cat"` sorts first |
| `common_words(words, b)` | `{"dog"}` | `"dog"` is the only word appearing in both `words` and `b`; `"fish"` is only in `b`, everything else is only in `words` |
| `words_only_in(words, b)` | `{"Cat", "bird", "cat"}` | every distinct word of `words` that never appears in `b` -- `"dog"` is excluded because `b` contains it |
| `most_frequent(words, 2)` | `[("cat", 3), ("dog", 2)]` | `cat` has the highest count (3), `dog` is next (2) -- no tie to break yet |
| `most_frequent(words, 3)` | `[("cat", 3), ("dog", 2), ("Cat", 1)]` | the third slot is a tie between `"bird"` (count 1) and `"Cat"` (count 1); ties break alphabetically ASCENDING, and by ASCII order `"Cat"` (`'C'` = 67) comes before `"bird"` (`'b'` = 98), so `"Cat"` wins the slot |
| `most_frequent(words, 0)` | `[]` (empty) | `k <= 0` always returns empty, regardless of input |

## Worked example: watch `most_frequent(words, 3)` run, step by step

This is the trickiest function in the assignment (it is the only one with a
tie to break), so here is every step spelled out, using the same
`words = {"cat", "dog", "cat", "bird", "dog", "cat", "Cat"}` from above.

**Step 1 -- build the frequency map.** This is exactly `word_frequencies(words)`:

```
freq = {"Cat": 1, "bird": 1, "cat": 3, "dog": 2}
```

Because `freq` is a `std::map`, iterating it always visits these four
entries in this exact order (ASCII order of the key): `Cat`, `bird`, `cat`,
`dog`.

**Step 2 -- repeated max-scan, `k = 3` times.** Each round scans every entry
not yet chosen and keeps the entry with the strictly highest count seen so
far (so on a tie, the FIRST entry encountered in map order -- i.e. the
alphabetically/ASCII-earliest one -- keeps its lead, since a later equal
count is not STRICTLY greater):

| Round | Entries considered (in map order) | Running best | Chosen this round | Why |
|-------|-----------------------------------|---------------|--------------------|-----|
| 1 | `Cat`(1), `bird`(1), `cat`(3), `dog`(2) | starts at `Cat`(1), then `cat`(3) beats it (3 > 1), `dog`(2) does not beat `cat` | `("cat", 3)` | `cat` has the single highest count in the whole map |
| 2 | `Cat`(1), `bird`(1), `dog`(2) (`cat` already chosen, skipped) | starts at `Cat`(1), then `dog`(2) beats it | `("dog", 2)` | `dog` is the highest remaining count |
| 3 | `Cat`(1), `bird`(1) (`cat`, `dog` already chosen, skipped) | starts at `Cat`(1); `bird`(1) does NOT beat it because `1 > 1` is false (not a STRICT improvement) | `("Cat", 1)` | `Cat` and `bird` are tied at count 1, but `Cat` was seen FIRST in map order (ASCII `'C'` < `'b'`), so it keeps the lead and wins the tie |

**Final result:** `[("cat", 3), ("dog", 2), ("Cat", 1)]`.

Notice the tie-break is not implemented by any explicit alphabetical
comparison -- it falls out for free from two facts working together:
`std::map` already iterates in ASCII-sorted key order, and the max-scan
only replaces its running best on a STRICT `>` comparison. That combination
is exactly why `most_frequent` is built on top of `word_frequencies`
(a `std::map`) instead of `first_occurrence_index`'s `std::unordered_map`,
whose iteration order is unspecified and would make the tie-break
unpredictable.

---

## Task

Implement every function declared in `word_ledger.hpp`, inside the
`wledger` namespace:

- `word_frequencies(words)` -> `std::map<std::string, int>` -- how many
  times each distinct word appears, sorted by word.
  *Examples:* `word_frequencies({"the", "cat", "the"})` ==
  `{"cat": 1, "the": 2}`; `word_frequencies({})` == `{}` (empty in, empty
  out); `word_frequencies({"Cat", "cat"})` == `{"Cat": 1, "cat": 1}` --
  two entries, because comparison is case-sensitive and `"Cat"` sorts
  before `"cat"` (uppercase letters have smaller ASCII values); a single
  repeated word like `word_frequencies({"go", "go", "go"})` == `{"go": 3}`.
- `first_occurrence_index(words)` -> `std::unordered_map<std::string, int>`
  -- for each distinct word, the 0-based index of its first appearance.
  Order does not matter here, so this returns the faster hash-table-backed
  map rather than a sorted one.
  *Examples:* `first_occurrence_index({"a", "b", "a"})` == `{"a": 0, "b":
  1}` (note `"a"`'s SECOND appearance at index 2 does not change its
  recorded index); `first_occurrence_index({})` == `{}`;
  `first_occurrence_index({"only"})` == `{"only": 0}`.
- `unique_words_sorted(words)` -> `std::set<std::string>` -- every distinct
  word, in sorted order (a `std::set`'s own iteration order already gives
  you this, for free).
  *Examples:* `unique_words_sorted({"banana", "apple", "banana"})` ==
  `{"apple", "banana"}`; `unique_words_sorted({})` == `{}`;
  `unique_words_sorted({"Cat", "bird", "cat"})` == `{"Cat", "bird",
  "cat"}` -- three distinct entries in ASCII order, not dictionary order
  (`"Cat"` first, since uppercase sorts before lowercase).
- `common_words(a, b)` -> `std::set<std::string>` -- the set
  **intersection**: every word that appears in both `a` and `b`.
  *Examples:* `common_words({"cat", "dog"}, {"dog", "fish"})` ==
  `{"dog"}`; `common_words({}, {"x"})` == `{}` (either side empty means no
  overlap is possible); `common_words({"a", "A"}, {"a"})` == `{"a"}` --
  `"A"` does not match `"a"` because comparison is case-sensitive.
- `words_only_in(a, b)` -> `std::set<std::string>` -- the set
  **difference**: every word in `a` that does not appear anywhere in `b`.
  *Examples:* `words_only_in({"cat", "dog", "bird"}, {"dog"})` == `{"bird",
  "cat"}`; `words_only_in({"x"}, {})` == `{"x"}` (`b` empty means nothing
  gets excluded); `words_only_in({}, {"x"})` == `{}` (`a` empty means
  there is nothing to report, regardless of `b`).
- `most_frequent(words, k)` -> `std::vector<std::pair<std::string, int>>`
  -- the top `k` most frequent words, ordered by count descending, with
  ties broken alphabetically ascending.
  *Examples:* `most_frequent({"a", "b", "a", "c", "b", "a"}, 2)` ==
  `[("a", 3), ("b", 2)]`; `most_frequent({"cat", "bird", "Cat"}, 2)` ==
  `[("Cat", 1), ("bird", 1)]` -- a three-way count tie (all count 1),
  broken by ASCII order, so `"Cat"` (uppercase `'C'`) beats `"bird"` and
  `"cat"`; `most_frequent({}, 3)` == `[]` (empty input); `most_frequent({"x",
  "y"}, 0)` == `[]` (`k <= 0` always returns empty, even with real words
  available).

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
