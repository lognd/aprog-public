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
int word_count(const char* s);

// Copies the n-th word (0-indexed) into dst, writing at most dst_len-1
// characters plus a null terminator.  Returns true if the n-th word
// exists, false otherwise.  On failure, dst[0] is set to '\0'.
// Precondition (a condition the caller must guarantee is true before
// calling): dst_len >= 1.
bool word_at(const char* s, int n, char* dst, size_t dst_len);

// Returns true if `word` appears as a complete word in `sentence`.
// "cat" must NOT match in "concatenate" or "scat".
// Matching is case-sensitive.
bool contains_word(const char* sentence, const char* word);

// Removes all leading and trailing spaces from s in-place.
// Interior spaces are left unchanged.
// "  hello   world  " -> "hello   world".
void trim(char* s);

// Capitalizes the first character of every word in s in-place.
// All other characters are left unchanged.
// "hello world" -> "Hello World".
void capitalize_words(char* s);

// Converts every character of s to lowercase in-place.
void to_lower(char* s);

// Returns the 0-based index of the first whole-word occurrence of `word`
// in `s`.  Returns -1 if not found.
// "the cat sat" with word="cat" -> 1.
int word_index(const char* s, const char* word);

} // namespace stools
```

## Word definition

A word is a maximal non-empty sequence of non-space characters.  The only
whitespace character you need to handle is the regular space `' '`.

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
