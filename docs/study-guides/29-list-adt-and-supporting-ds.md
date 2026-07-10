# Study Guide 29: List ADT & Supporting DS

This module introduces the ADT/implementation distinction and puts it to
work on the List: the same operations contract can be backed by a dynamic
array or a linked list, with wildly different real costs. Students pick
the right backing structure for concrete workloads and count exact shifts,
hops, and capacity changes rather than only quoting Big-O classes.

## Know before you start

- Big-O growth classes, amortized O(1), and the capacity-doubling rule
  [assumed: row 28 -- Complexity Theory]
- Cache lines and spatial locality of contiguous memory [assumed: row 19 --
  Structs (DOD & OOP intro)]
- `std::vector` size vs. capacity and reallocation [assumed: row 7 --
  Standard Library Types]
- Pointers and pointer-chasing through heap-allocated nodes [assumed:
  row 11 -- Pointers]

## Taught here

Concept: ADT vs. implementation
- Know that an ADT (Abstract Data Type) is a description of behavior only:
  a set of operations and the contract each honors (e.g. insert(index,
  value), remove(index), get(index), size()), with no mention of how they
  are carried out.
- Know that a dynamic array (one contiguous block of memory) and a linked
  list (a chain of separately allocated nodes, each pointing to the next)
  are both implementations of a similar List ADT, and that the mechanical
  difference is exactly why the same abstract operation can have wildly
  different real cost.

Concept: the cost profile of each backing structure
- Know random access: a dynamic array computes an element's address by
  arithmetic in O(1); a linked list must chase pointers from the head, an
  O(n) sequential walk.
- Know front insertion: a dynamic array must shift every existing element
  over (O(n)); a linked list relinks a couple of pointers (O(1)).
- Know splicing: cutting a run of elements out and reinserting them
  elsewhere is pointer rearrangement for a linked list, but wholesale data
  movement for an array.
- Know the cache-locality reality check: iterating contiguous memory is
  much faster on real hardware than pointer-chasing scattered nodes, so
  dynamic arrays often beat linked lists in wall-clock time even where the
  list's Big-O looks better -- two O(n) operations can differ by a large
  constant factor.
- Be able to choose per scenario: dynamic array, linked list, or "either
  works," by asking what physical work each structure does -- does it
  copy/shift element data (scales with elements affected) or just repoint
  pointers (does not)?

Concept: exact counting instead of complexity classes
- Be able to count exactly how many elements `insert(index, v)` or
  `erase(index)` shifts in an array of a given size (elements from the
  index to the end move; the rest do not).
- Be able to count exactly how many pointer hops a linked-list traversal
  or insertion needs to reach a given index from `head`.
- Be able to trace a dynamic array's size and capacity as two separate
  running numbers through a sequence of `push_back` calls: size counts
  pushes; capacity changes only on a push that occurs while the array is
  already full, doubling each time.

## Study checklist

- [ ] Define ADT in one sentence and name two implementations of the List
      ADT.
- [ ] State the array vs. list cost for random access, front insertion,
      and splicing.
- [ ] Explain why a vector can beat a list in practice even at equal
      Big-O.
- [ ] Count the shifts for `insert(2, 99)` on a five-element array.
- [ ] Trace size and capacity through eight pushes starting from an empty
      array.

## Practiced in

`list-tradeoff-tribunal`, `index-vs-node`
