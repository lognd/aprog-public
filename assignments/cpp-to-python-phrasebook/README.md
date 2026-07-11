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

## Examples: every function on one text

To make all six functions concrete, here is **one** text, and what each
function returns for it. Read this table first -- it is the whole
assignment in miniature.

```
text = "The fox ran, the dog ran, the fox won!"
```

Tokenizing this text (splitting it into maximal runs of ASCII letters/digits,
discarding everything else) gives nine words, in this order:

```
["The", "fox", "ran", "the", "dog", "ran", "the", "fox", "won"]
```

| Call | Returns | Why |
|------|---------|-----|
| `word_count(text)` | `9` | there are nine words total (commas, spaces, and the trailing `!` are not words and are not counted) |
| `unique_words_sorted(text)` | `['The', 'dog', 'fox', 'ran', 'the', 'won']` | six DISTINCT words, sorted; `"The"` and `"the"` are different words (case-sensitive) and both appear, so both are kept, with `"The"` sorting before `"dog"` because uppercase letters sort before lowercase letters |
| `word_frequencies(text)` | `{'The': 1, 'fox': 2, 'ran': 2, 'the': 2, 'dog': 1, 'won': 1}` | `"fox"`, `"ran"`, and lowercase `"the"` each occur twice; `"The"` (capitalized, only at the start of the sentence), `"dog"`, and `"won"` each occur once |
| `most_frequent(text, 2)` | `['fox', 'ran']` | `"fox"`, `"ran"`, and `"the"` are tied at count 2, but only the top 2 are wanted; alphabetically `"fox"` and `"ran"` come before `"the"` |
| `most_frequent(text, 0)` | `[]` | `k <= 0` always returns an empty list, no matter what `text` contains |
| `most_frequent(text, 100)` | `['fox', 'ran', 'the', 'The', 'dog', 'won']` | asking for more words than exist (100) just returns every distinct word, ranked by count then alphabetically; note `"The"` (count 1) sorts after `"the"` (count 2) because it is ranked by count FIRST, alphabetical order only breaks ties within the same count |
| `reverse_words(text)` | `'won fox the ran dog the ran fox The'` | the same nine words, in reverse order, joined by single spaces -- punctuation is gone for good, it never reappears in the output |
| `is_palindrome_sentence(text)` | `False` | ignoring case and punctuation this reads `thefoxranthedogranthefoxwon`, which is not the same forwards and backwards |
| `is_palindrome_sentence("")` | `True` | an empty text has no letters to disagree with each other, so it counts as a (trivial) palindrome |

## Worked example: watch tokenization run, step by step

This is the single most important thing to understand in the assignment,
because every one of the six functions is built on top of it: turning raw
text into a list of words. Here is that process traced character by
character, for the short text `"Hi, Sam!"`.

The rule: walk the text one character at a time, building up a "current
word" buffer. Every time a character is an ASCII letter or digit, add it to
the buffer. Every time a character is NOT a letter or digit (a comma, a
space, `!`, ...), the current word (if the buffer is non-empty) is finished
and added to the word list, and the buffer is reset to empty for the next
word.

| Step | Character | Is letter/digit? | Action | Buffer after | Words finished so far |
|------|-----------|-------------------|--------|---------------|-----------------------|
| 1 | `'H'` | yes | append to buffer | `"H"` | `[]` |
| 2 | `'i'` | yes | append to buffer | `"Hi"` | `[]` |
| 3 | `','` | no | buffer is non-empty -> close word `"Hi"`, reset buffer | `""` | `["Hi"]` |
| 4 | `' '` | no | buffer is empty -> nothing to close | `""` | `["Hi"]` |
| 5 | `'S'` | yes | append to buffer | `"S"` | `["Hi"]` |
| 6 | `'a'` | yes | append to buffer | `"Sa"` | `["Hi"]` |
| 7 | `'m'` | yes | append to buffer | `"Sam"` | `["Hi"]` |
| 8 | `'!'` | no | buffer is non-empty -> close word `"Sam"`, reset buffer | `""` | `["Hi", "Sam"]` |
| end | -- | -- | text is exhausted; buffer is empty, so nothing left to close | `""` | `["Hi", "Sam"]` |

The final word list is `["Hi", "Sam"]`. From here, `word_count("Hi, Sam!")`
is just `len(["Hi", "Sam"])`, which is `2`; `unique_words_sorted` sorts that
same list and removes duplicates (there are none here, so it stays
`["Hi", "Sam"]`); `word_frequencies` counts occurrences in that list
(`{"Hi": 1, "Sam": 1}`); and so on -- every function's answer traces back to
this same word list. Notice the one detail that trips people up: a
character check happens on EVERY character, including the very last one --
if the text ended mid-word (e.g. `"Hi, Sam"` with no trailing `!`), the loop
finishing would still need to close whatever is left in the buffer, or the
final word would be silently dropped.

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

**`word_count(text)` examples:**
- `word_count("the quick brown fox") == 4` -- four space-separated words
- `word_count("") == 0` -- an empty text has zero words (not an error)
- `word_count("!!!") == 0` -- punctuation-only text also has zero words; `!` is never part of a word

**`unique_words_sorted(text)` examples:**
- `unique_words_sorted("the fox and the hound") == ['and', 'fox', 'hound', 'the']` -- four distinct words, alphabetical
- `unique_words_sorted("The the THE") == ['THE', 'The', 'the']` -- all three are DIFFERENT words (case-sensitive); sorted order is by character code, so all-uppercase `THE` comes first, then `The`, then all-lowercase `the`
- `unique_words_sorted("") == []` -- empty text, empty list, never an error

**`word_frequencies(text)` examples:**
- `word_frequencies("a b a c b a") == {'a': 3, 'b': 2, 'c': 1}` -- one entry per distinct word, mapped to its count
- `word_frequencies("The the") == {'The': 1, 'the': 1}` -- case-sensitive, so this is two entries, not one merged into `2`
- `word_frequencies("") == {}` -- empty text produces an empty dict, not an error and not `None`

**`most_frequent(text, k)` examples:**
- `most_frequent("a b a c b a", 2) == ['a', 'b']` -- `a` (count 3) then `b` (count 2), the two highest counts
- `most_frequent("a a c b", 3) == ['a', 'b', 'c']` -- `b` and `c` tie at count 1; the tie is broken alphabetically, ascending
- `most_frequent("a b a c b a", 0) == []` -- `k <= 0` (zero, or negative) always returns `[]`, never an error
- `most_frequent("a b c", 100) == ['a', 'b', 'c']` -- asking for more words than exist (`k` larger than the number of distinct words) just returns every distinct word, still ranked; it does not raise or pad the result

**`reverse_words(text)` examples:**
- `reverse_words("the quick brown fox") == 'fox brown quick the'` -- words in reverse order, single spaces, punctuation gone for good
- `reverse_words("") == ''` -- empty text reverses to an empty string
- `reverse_words("one") == 'one'` -- a single word reversed is itself

**`is_palindrome_sentence(text)` examples:**
- `is_palindrome_sentence("A man, a plan, a canal: Panama") == True` -- ignoring case and punctuation this reads `amanaplanacanalpanama` both forwards and backwards
- `is_palindrome_sentence("this is not a palindrome") == False` -- reads differently forwards and backwards
- `is_palindrome_sentence("") == True` -- an empty text has no letters at all, so there is nothing to contradict; it counts as a (trivial) palindrome

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
