# Study Guide 33: Map & Set ADT

This module introduces associative containers -- lookup by key instead of
by position -- and the hash-table-versus-balanced-tree tradeoff behind
them. `word-ledger` applies all four (`std::map`, `std::unordered_map`,
`std::set`, `std::unordered_set`) to text analysis, including two classic
set operations and a repeated-max-scan top-k without a custom comparator.

## Know before you start

- Big-O growth classes, O(1) vs. O(log n) vs. O(n) [assumed: row 28 --
  Complexity Theory]
- `std::vector` as the sequence-container default and when a linear scan
  over a small collection is competitive [assumed: row 32 -- Standard
  Containers p1]
- Amortized cost reasoning [assumed: row 28 -- Complexity Theory]

## Taught here

Concept: hash table vs. balanced tree
- Know that a hash table stores key-value pairs by running each key
  through a hash function (turns a key into a number) to pick a bucket to
  store it in directly, giving average O(1) insert/lookup/erase but no
  ordering guarantee at all when iterating.
- Know that a balanced tree (typically red-black) keeps entries in a tree
  structure kept balanced so no path is much longer than any other, giving
  guaranteed O(log n) insert/lookup/erase (slower on average than a hash
  table, but with a guaranteed worst case) plus sorted-order iteration for
  free.
- Know that `std::map` and `std::set` are balanced trees (sorted
  iteration, guaranteed O(log n)); `std::unordered_map` and
  `std::unordered_set` are hash tables (average O(1), unspecified
  iteration order).
- Know that `std::unordered_map`'s average O(1) lookup can degrade to
  worst-case O(n) when many keys hash into the same bucket (a hash
  collision pileup).

Concept: map vs. set, and picking the right one
- Know that a map stores a key mapped to an associated value (e.g. a word
  mapped to its count); a set stores keys only, with no associated value,
  answering pure membership questions ("have I seen this key before?").
- Be able to pick the right one of the four in two questions: does this
  need a VALUE per key (map) or just membership (set)? Then, does it need
  SORTED iteration (plain `map`/`set`) or just raw average speed with no
  ordering need (`unordered_` variant)?
- Know that for a genuinely small, close-to-fixed collection, a plain
  `std::vector` of key-value pairs scanned linearly is a real, valid
  alternative to any map -- a map's tree/hash overhead only pays for
  itself once there are enough entries and enough lookups to matter.

Concept: `operator[]`'s insert-on-read trap
- Know that `operator[]` on `std::map`/`std::unordered_map` silently
  inserts a default-constructed value (0 for `int`) for a missing key
  when merely READ, even inside a condition or a print statement -- it is
  never a pure read on a possibly-missing key.
- Know `count()` and `find()` as the safe, non-inserting ways to check for
  a key's presence.
- Know that `insert()` leaves an existing key's value untouched if the key
  is already present, while `operator[]` used for assignment always
  overwrites the existing value.
- Know that `erase()` returns how many elements were actually removed (0
  or 1, since keys are unique in map/set).
- Know that `std::map` guarantees ascending sorted-key iteration order;
  `std::unordered_map`'s iteration order is unspecified and must never be
  relied on or predicted exactly.

Concept: implementing associative-container algorithms
- Be able to build a frequency map with `map[key]++` (relying on the
  insert-on-read default of 0).
- Be able to implement set intersection (`common_words`) by iterating one
  container and checking membership in the other with `count()`/`find()`.
- Be able to implement set difference (`words_only_in`) the same way, kept
  by membership absence rather than presence.
- Be able to implement a top-k ranking via a repeated max-scan (k passes
  over the frequency map, each time picking the highest-count unused entry
  with alphabetical tie-breaking) as a documented, accepted O(k*n)
  approach when no custom sort comparator is available yet.

## Study checklist

- [ ] Given a workload, answer "value or no value" then "order or no
      order" to pick map/unordered_map/set/unordered_set.
- [ ] Explain what causes std::unordered_map's worst-case O(n) lookup.
- [ ] Predict the output of a snippet where operator[] reads a missing
      key and silently inserts it.
- [ ] Explain insert() vs. operator[]-as-assignment on an existing key.
- [ ] Implement set intersection/difference using count() or find().
- [ ] Explain why a small, near-fixed collection can beat a map with a
      plain vector linear scan.

## Practiced in

`associative-adjudicator`, `bracket-trap`, `word-ledger`
