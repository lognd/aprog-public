# C++ to Python Phrasebook

You already built word-ledger: a set of pure C++ functions that count words,
find unique words, rank words by frequency, and compare two texts. That
project already contains every idea this assignment needs. What is new
here is not the logic -- it is the language. You are porting your own
working design from C++ to Python, function by function, and along the way
you will meet the handful of Python tools (the `dict`, sorting with a
`key=` function, and plain string methods) that replace what `std::map`,
a hand-written comparator, and character-array parsing did in C++.

## Problem statement

Implement six pure functions in a file named `phrasebook.py`. Every
function takes a piece of text (a Python `str`, the direct equivalent of a
C++ `std::string`) and returns an answer computed from its **words**.

A **word**, for every function in this file, is defined the same way: a
maximal run of one or more ASCII letters or digits. Punctuation, spaces,
and any other characters are not part of any word and never appear in one
-- `"Hello, world!"` contains exactly two words, `"Hello"` and `"world"`,
with the comma and exclamation point discarded entirely. Word matching is
**case-sensitive**: `"The"` and `"the"` are different words, just as they
would be if you compared two `std::string`s with `==` in C++.

## Interface

```python
def word_count(text):
    """Number of words in text."""

def unique_words_sorted(text):
    """Sorted list of the distinct words in text (case-sensitive)."""

def word_frequencies(text):
    """dict mapping each word in text to its occurrence count."""

def most_frequent(text, k):
    """The k most frequent words in text, ties broken alphabetically ascending."""

def reverse_words(text):
    """text's words, in reverse order, joined by a single space."""

def is_palindrome_sentence(text):
    """True if text reads the same forwards and backwards, ignoring case and punctuation."""
```

### Examples

```python
>>> word_count("the quick brown fox")
4
>>> unique_words_sorted("the fox and the hound")
['and', 'fox', 'hound', 'the']
>>> word_frequencies("a b a c b a")
{'a': 3, 'b': 2, 'c': 1}
>>> most_frequent("a b a c b a", 2)
['a', 'b']
>>> most_frequent("a a c b", 3)     # b and c tie at count 1; alphabetical order breaks the tie
['a', 'b', 'c']
>>> reverse_words("the quick brown fox")
'fox brown quick the'
>>> is_palindrome_sentence("A man, a plan, a canal: Panama")
True
>>> is_palindrome_sentence("this is not a palindrome")
False
```

`most_frequent` with `k <= 0`, or with `text` containing fewer distinct
words than `k`, should not raise -- return `[]` for the former, and every
distinct word (still ranked by frequency, ties alphabetical) for the
latter.

## Every Python concept here, defined via its C++ counterpart

This project deliberately introduces Python's core vocabulary by pointing
straight at the C++ feature you already know that plays the same role.

<details>
<summary>def -- Python's function definition, no return type written</summary>

C++ requires a return type before a function's name: `int word_count(const
std::string& text) { ... }`. Python's `def` has no return-type annotation
at all (and no parameter types, unless you choose to add optional type
*hints*, which Python never enforces at runtime the way C++ enforces its
types at compile time): `def word_count(text):`. A Python function can
return any type, and different calls to the same function are even allowed
to return different types -- nothing checks this for you the way the
compiler does in C++.

</details>

<details>
<summary>str -- Python's string type, and its one big difference from std::string</summary>

Python's `str` plays the same conceptual role as C++'s `std::string`: a
sequence of characters, with `+` for concatenation, `len(s)` for length
(like `s.size()`), and `s[i]` for indexing a single character. The genuine
difference: `str` is **immutable** -- there is no equivalent of
`std::string::operator[]=` that mutates a character in place, and no
`+=` that grows a string's own storage. Every string "modification" in
Python (slicing, `+`, `.lower()`, ...) builds a brand-new string object and
leaves the original untouched. This matters directly in this assignment:
see the `str.join()` note under `reverse_words` below.

</details>

<details>
<summary>dict -- Python's associative container, and why it is NOT std::map</summary>

Python's `dict` is the direct counterpart of an associative container --
the same role `std::map` or `std::unordered_map` plays in C++, mapping
keys to values. The important difference for this assignment: a Python
`dict` remembers **insertion order** -- iterating over it (or printing it)
always visits keys in the order they were first inserted, which is
neither `std::map`'s sorted-by-key order nor `std::unordered_map`'s
unspecified order. `word_frequencies` relies on nothing about this order
(the tests only check its contents, via `==` against another `dict`), but
you may notice it when you print one while debugging.

</details>

<details>
<summary>sorting with a key function -- Python's replacement for a comparator</summary>

C++ sorting a `std::vector` with custom logic typically means writing a
comparator: `std::sort(v.begin(), v.end(), [](auto& a, auto& b) { ... });`.
Python's `sorted(iterable, key=...)` takes a different shape: instead of a
function that compares two elements directly, you give it a function that
computes, for a single element, the *value to sort by* -- `sorted(words,
key=lambda w: len(w))` sorts by each word's length. `sorted(..., key=...)`
is the tool `most_frequent` needs: you want to rank words by count
(descending), with ties broken alphabetically (ascending) -- both at once,
from a single key.

</details>

<details>
<summary>tuple, and tuple unpacking -- Python's lightweight, unnamed struct</summary>

A Python `tuple`, like `(word, count)`, is a fixed-size, ordered group of
values -- similar in spirit to a `std::pair` (for two elements) or
`std::tuple` (for any number) in C++, but Python's version needs no
`#include` and no template arguments; `(a, b)` alone builds one. `dict`'s
`.items()` method returns exactly this: `(key, value)` tuples, one per
entry. Unpacking a tuple directly into named variables -- `for word, count
in freq.items():` -- is Python's equivalent of C++17's structured bindings
(`for (auto& [word, count] : freq)`), and it is worth using here instead of
indexing into each tuple by position.

</details>

## Constraints

- `phrasebook.py` must contain **no `import` statements of `re` or
  `collections`** -- the point of this assignment is to write the
  tokenization and ranking logic yourself, the way you did in C++, rather
  than reach for `re` (regex) or `collections.Counter` to skip past it.
  Every function is implementable with plain `str`/`list`/`dict` methods.
- All six functions must be **pure**: no `print`, no reading from a file,
  no mutating anything outside the function. Given the same arguments, each
  function must always return the same result.
- **Type-annotation bonus (10 pts):** fully annotate every one of the six
  functions -- each parameter and the return type, e.g.
  `def word_count(text: str) -> int:`. The bonus is awarded only when all six
  signatures are completely annotated. A separate, informational `ty` check
  (a fast, modern Python [type checker](https://docs.astral.sh/ty/)) then runs
  over `phrasebook.py` to flag annotations that do not hold up -- fix any it
  reports. The bonus is not required to pass the assignment, but earning it
  means actually typing your code, not just leaving it unannotated.

## Grading

| Component                          | Points |
|-------------------------------------|--------|
| No `re`/`collections` shortcuts     | 0 (gate) |
| Visible correctness tests           | 40     |
| Hidden correctness tests            | 50     |
| Complete type annotations (bonus)   | 10     |

## Submission

Submit your implementation as `phrasebook.py`. Do not rename the module,
and do not change any function's name or parameter list.
