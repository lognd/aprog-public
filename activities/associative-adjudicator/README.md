# Activity: Associative Adjudicator

An **associative container** stores elements looked up by a **key** (a
value used to find something) rather than by position. This activity is
about choosing the right one for a given workload: `std::map`,
`std::unordered_map`, `std::set`, or `std::unordered_set`. No code to trace
-- pure reasoning about hash tables versus balanced trees, keys versus
key-value pairs, and when a plain `std::vector` of pairs quietly beats all
four.

## Background

A **hash table** stores key-value pairs by running each key through a
**hash function** (a function that turns a key into a number) to pick a
**bucket** to store it in directly. This gives average O(1) insert, lookup,
and erase, but no ordering between keys at all -- iterating a hash table
visits elements in whatever order the buckets happen to lay them out. A
**balanced tree** (typically a red-black tree) keeps every key-value pair
in a tree structure that stays balanced (no path through the tree is much
longer than any other), giving guaranteed O(log n) insert/lookup/erase --
slower on average than a hash table, but with a guaranteed worst case, and
with the bonus that iterating the tree always visits keys in **sorted**
order.

`std::map` and `std::set` are backed by a balanced tree. `std::unordered_map`
and `std::unordered_set` are backed by a hash table -- the "unordered"
prefix is the standard library's way of telling you upfront that you get no
sorted-iteration guarantee in exchange for faster average operations. A
**map** stores a key mapped to an associated **value** (like a word mapped
to its definition); a **set** stores keys only, with no associated value,
answering pure membership questions ("have I seen this key before").

## Concepts covered

- Hash table versus balanced tree, defined from scratch, and the O(1)-average
  versus O(log n)-guaranteed tradeoff between them
- Map (key -> value) versus set (keys only, membership questions)
- Choosing sorted iteration (`std::map`/`std::set`) versus raw average
  lookup speed (`std::unordered_map`/`std::unordered_set`)
- The dedup-with-order versus dedup-without-order distinction
- Recognizing when a plain `std::vector` of pairs, scanned linearly, beats
  any map for a genuinely small, close-to-fixed number of entries
- Why `std::unordered_map`'s average O(1) lookup can degrade to worst-case
  O(n) when many keys collide into the same bucket

## How it works

Each question describes a workload and asks which of the four associative
containers (or, in one case, a plain vector of pairs) fits best. Type the
exact container name or phrase requested by the prompt. Getting a question
wrong shows a detailed explanation of the tradeoff you missed; answer every
question correctly to reveal the passphrase.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly answered all eight scenarios and the launcher prints the
activity's passphrase.

## Hints

<details>
<summary>Hint 1 -- ask two questions in order: value or no value, then order or no order</summary>

First: does this workload need a VALUE associated with each key (map), or
just a yes/no membership check (set)? Second, of the two map or two set
options that leaves: does the workload need SORTED iteration (the plain
`std::map`/`std::set` variant), or is raw average speed the priority with
no ordering need (the `unordered_` variant)?

</details>

<details>
<summary>Hint 2 -- "how many entries, checked how often" matters more than it looks</summary>

A map's or set's overhead (tree traversal and per-node allocation, or hash
computation and bucket lookup) only pays for itself once there are enough
entries and enough lookups to matter. For a genuinely small, close-to-fixed
collection, a linear scan over a plain vector is a real, valid alternative
-- not a beginner's mistake.

</details>

## Going further

- Benchmark `std::map<std::string, int>` against a `std::vector<std::pair<std::string, int>>`
  scanned linearly, for n = 5, n = 50, and n = 5000 lookups. Where does the
  crossover happen on your machine?
- Look up how `std::unordered_map` decides when to grow its bucket array
  (its "load factor"). How does growing the bucket array relate to keeping
  average lookup close to O(1) as more keys are inserted?
- Write a small program that deliberately picks keys with a bad hash
  function (e.g. always returning 0) for a hand-rolled hash table. Measure
  how lookup time changes as you insert more keys, and compare it to
  `std::unordered_map`'s real hash function on the same keys.
