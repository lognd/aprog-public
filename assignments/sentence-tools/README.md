# Sentence Tools

## Overview

You will implement a small C-style string library that works at the level of
words, not just characters.  Each function in the interface takes `const char*`
or `char*` parameters -- no `std::string` allowed.  The challenge is reasoning
about word boundaries, in-place mutation, and the null terminator convention
simultaneously.

## Learning goals

- Implement word-level string operations using only `const char*` and `char*` -- no `std::string`
- Reason about word boundaries, whitespace runs, and null terminators simultaneously
- Perform in-place mutation of C strings (capitalize, lowercase, trim) without heap allocation
- Mark functions `inline` and understand why it is required for header-only definitions

## Task

Implement every function declared in `sentence_tools.hpp` inside that same
file.  Mark each function `inline` so the header-only build works -- "header-only"
means the full body of every function lives in the `.hpp` file itself instead
of a separate `.cpp` file.  Without `inline`, defining a function body directly
in a header causes a linker error ("multiple definition") as soon as that
header is `#include`d from more than one `.cpp` file.

### Interface

```cpp
namespace stools {

// Returns the number of whitespace-separated words in s.
// "  hello  world  " -> 2.  Empty or all-spaces -> 0.
// Examples:
//   word_count("hello world") == 2
//   word_count("") == 0
//   word_count("     ") == 0  (spaces only, still zero words)
int word_count(const char* s);

// Copies the n-th word (0-indexed) into dst, writing at most dst_len-1
// characters plus a null terminator.  Returns true if the n-th word
// exists, false otherwise.  On failure, dst[0] is set to '\0'.
// Precondition (a condition the caller must guarantee is true before
// calling): dst_len >= 1.
// Examples (dst is a char buffer with room for dst_len bytes):
//   word_at("  the  cat   sat   on   the    mat  ", 4, dst, 32) == true,
//     dst == "the"  (the SECOND "the", found by counting, not by spelling)
//   word_at("hello world", 5, dst, 32) == false, dst == ""
//     (there is no 6th word)
//   word_at("hello world", 0, dst, 4) == true, dst == "hel"
//     (dst_len is only 4, so the copy is truncated to 3 chars + '\0')
int word_at(const char* s, int n, char* dst, size_t dst_len);

// Returns true if `word` appears as a complete word in `sentence`.
// "cat" must NOT match in "concatenate" or "scat".
// Matching is case-sensitive.
// Examples:
//   contains_word("the cat sat", "cat") == true
//   contains_word("the cat sat", "at") == false
//     ("at" is a substring of "cat" and "sat" but never a whole word)
//   contains_word("the cat sat", "") == true
//     (an empty search word is trivially present -- there is no character
//     it needs to match)
bool contains_word(const char* sentence, const char* word);

// Removes all leading and trailing spaces from s in-place.
// Interior spaces are left unchanged.
// "  hello   world  " -> "hello   world".
// Examples:
//   trim(s) where s == "  hello  " leaves s == "hello"
//   trim(s) where s == "  hello   world  " leaves s == "hello   world"
//     (the wide interior gap is untouched)
//   trim(s) where s == "     " (spaces only) leaves s == ""
void trim(char* s);

// Capitalizes the first character of every word in s in-place.
// All other characters are left unchanged.
// "hello world" -> "Hello World".
// Examples:
//   capitalize_words(s) where s == "hello world" leaves s == "Hello World"
//   capitalize_words(s) where s == "HELLO world" leaves s == "HELLO world"
//     (only the FIRST character of each word changes -- the rest of
//     "HELLO" is left exactly as it was, still all uppercase)
//   capitalize_words(s) where s == "" leaves s == "" (nothing to do)
void capitalize_words(char* s);

// Converts every character of s to lowercase in-place.
// Examples:
//   to_lower(s) where s == "HELLO World" leaves s == "hello world"
//   to_lower(s) where s == "already lower" leaves s == "already lower"
//   to_lower(s) where s == "" leaves s == "" (nothing to do)
void to_lower(char* s);

// Returns the 0-based index of the first whole-word occurrence of `word`
// in `s`.  Returns -1 if not found.
// "the cat sat" with word="cat" -> 1.
// Examples:
//   word_index("the cat sat on the mat", "cat") == 1
//   word_index("the cat sat on the mat", "the") == 0
//     (the FIRST "the" wins, at word index 0, even though "the" also
//     appears again later in the sentence)
//   word_index("the cat sat", "dog") == -1
int word_index(const char* s, const char* word);

} // namespace stools
```

## Word definition

A word is a maximal non-empty sequence of non-space characters.  The only
whitespace character you need to handle is the regular space `' '`.

---

## Examples at a glance

To make all seven functions concrete, here is **one** sentence, with the index
of every word written above it, and what each function returns for it. Read
this table first -- it is the whole assignment in miniature.

```
 word index:   0      1     2     3    4      5
 s          = "  the  cat   sat   on   the    mat  "
```

(There are two leading spaces, three interior gaps that are wider than one
space, and two trailing spaces -- deliberately, so you can see that extra
whitespace never confuses word boundaries.)

| Call | Returns | Why |
|------|---------|-----|
| `word_count(s)` | `6` | six whitespace-separated words, regardless of how many spaces sit between or around them |
| `word_at(s, 0, dst, 32)` | `true`, `dst = "the"` | word index 0 is the first word, leading spaces are skipped |
| `word_at(s, 4, dst, 32)` | `true`, `dst = "the"` | `"the"` appears twice; index 4 is the SECOND occurrence, found by counting words left to right |
| `word_at(s, 6, dst, 32)` | `false`, `dst = ""` | there is no 7th word (only indices 0-5 exist), so `dst[0]` is set to `'\0'` |
| `contains_word(s, "cat")` | `true` | `"cat"` appears as a complete word |
| `contains_word(s, "at")` | `false` | `"at"` is a substring of `"cat"` and `"sat"` but never a WHOLE word on its own |
| `contains_word(s, "")` | `true` | an empty search word is treated as trivially present (see its per-function example below) |
| `word_index(s, "cat")` | `1` | `"cat"` is the word at index 1 |
| `word_index(s, "the")` | `0` | `word_index` returns the FIRST matching word's index, even though `"the"` also occurs at index 4 |
| `word_index(s, "dog")` | `-1` | `"dog"` never appears, so the function reports "not found" |
| `trim(s)` (in place) | `"the  cat   sat   on   the    mat"` | leading and trailing spaces are removed; the wider interior gaps are left exactly as they were |
| `capitalize_words("the cat sat on the mat")` (in place) | `"The Cat Sat On The Mat"` | the first letter of every word becomes uppercase; every other letter is untouched |
| `to_lower("The CAT Sat ON The Mat")` (in place) | `"the cat sat on the mat"` | every letter becomes lowercase, independent of word boundaries |

---

## Worked example: watch `word_at(s, 4, dst, 32)` run, step by step

This is the trickiest function to get right, because it must find a word by
COUNTING through the string rather than jumping straight to it (there is no
array of pre-split words -- only the raw characters and their positions). We
walk `s = "  the  cat   sat   on   the    mat  "` one character at a time,
tracking whether we are currently "inside a word" (`in_word`) and how many
complete words we have finished (`idx`), looking for word index `n = 4`.

| Position (character) | `in_word` before | Action | `idx` after |
|---|---|---|---|
| `' '`, `' '` (2 leading spaces) | false | not in a word, nothing happens | 0 |
| `'t'` starts `"the"` | false -> true | a new word begins, remember its start pointer | 0 |
| `'h'`, `'e'` | true | still inside `"the"`, keep scanning | 0 |
| `' '` (space after `"the"`) | true -> false | word index 0 (`"the"`) just ended; `idx` is not yet 4, so keep going | 1 |
| (more spaces) | false | still not in a word | 1 |
| `'c'` starts `"cat"` | false -> true | a new word begins | 1 |
| `'a'`, `'t'` | true | still inside `"cat"` | 1 |
| `' '` (space after `"cat"`) | true -> false | word index 1 (`"cat"`) ended; still not 4 | 2 |
| `"sat"` scanned the same way | -- | word index 2 ends | 3 |
| `"on"` scanned the same way | -- | word index 3 ends | 4 |
| `'t'` starts the SECOND `"the"` | false -> true | a new word begins; this is the word we want, since `idx` is now `4` | 4 |
| `'h'`, `'e'` | true | still scanning this word | 4 |
| `' '` (space after the second `"the"`) | true -> false | this word just ended, and `idx == n` (`4 == 4`), so **this is the match**: copy it into `dst` | -- |

The characters between the start of that second `"the"` and the space that
ends it get copied into `dst`, followed by a `'\0'`. The function returns
`true` and `dst` now holds `"the"` -- specifically the SECOND `"the"` in the
sentence, not the first, because `word_at` counts words by position, not by
which spelling matches first. (Contrast this with `word_index(s, "the")`,
which stops at the FIRST `"the"` it finds, at word index `0`.)

## Files

- `sentence_tools.hpp` -- the file you edit; contains both declarations and
  your `inline` implementations
- `visible-tests/test_catch.cpp` -- visible tests you can run locally, written
  with Catch2 (a C++ library for writing and running automated test cases)

## Compilation and Testing

```bash
mkdir build && cd build
cmake .. -DSUBMISSION_DIR=<path-to-your-submission>
cmake --build .
./sentence-tools_tests
```

The `SUBMISSION_DIR` variable tells CMake where to find your
`sentence_tools.hpp`.

## Constraints

- Do not `#include <string>` or use `std::string` anywhere in your header.
- You may use `<cstring>`, `<cctype>`, and `<cstddef>`.
- Every function must be marked `inline`.
- Do not allocate heap memory -- all functions operate on caller-owned buffers.

## Grading

| Component | Points |
|---|---|
| Compilation | 0 (required to proceed) |
| Visible tests (Catch2) | 30 |
| Hidden tests (Catch2) | 60 |
| Memory safety (Valgrind) | 10 |
| **Total** | **100** |
| Extra credit (ASan) | +10 |

Catch2 is the test-writing library used above. Valgrind is a tool that runs
your compiled program and reports memory errors (like reading past the end of
a buffer) that would otherwise pass silently. ASan (AddressSanitizer) is a
compiler flag (`-fsanitize=address`) that instruments your program at compile
time to catch those same kinds of memory errors as it runs.

## Submission

Submit a single file named `sentence_tools.hpp`. Do not rename the file.

## Going further

- Add a `word_wrap(const char* s, int width, char* dst, size_t dst_len)` function
  that wraps `s` at `width` characters. No `std::string` allowed.
- Look up `std::string_view` (C++17). Rewrite `word_count` to accept a
  `std::string_view` instead of `const char*`. What changes?
- Benchmark `contains_word` on a 10,000-word string. Profile with `gprof` (a
  profiling tool that measures how much time your program spends in each
  function) and see how much time is spent in character comparison.
