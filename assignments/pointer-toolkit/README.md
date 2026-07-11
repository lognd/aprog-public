# Pointer Toolkit

## Overview

A pointer stores the address of another object. Pointer arithmetic lets you navigate
memory by incrementing or decrementing the pointer itself (e.g. `p++` to move to the
next element) rather than using an index and the subscript operator (the `[]` in
`arr[i]`). In this assignment you implement eight array and string utility functions
using only pointer arithmetic -- no subscript operators on the core traversals.

Every higher-level container you will ever use (`std::vector`, `std::string`,
even a plain C array) is, underneath, a contiguous block of memory that
something walks one element at a time. `arr[i]` is not magic -- it is
literally shorthand for `*(arr + i)`, computed by adding `i` to the address
`arr` and reading whatever is at the resulting address. This assignment
exists to make that fact concrete and automatic: once you have written
`reverse`, `find`, and the C-string functions using only pointer
increments/decrements, subscript notation stops being a black box, and
bugs involving off-by-one addresses, dangling pointers, and "reading past
the end" become things you can reason about directly, address by address.

## Learning goals

- Navigate arrays and C strings using pointer arithmetic (`p++`, `*(p + i)`) without subscript operators
- Use the two-pointer technique (walking two pointers toward each other from
  opposite ends) for in-place reversal (rewriting the data in its own memory,
  without copying it into a second array) of arrays and strings
- Implement C string utilities (`strlen`, `strcpy`, `strcmp`) from first principles
- Return `nullptr` to signal "not found" and use it correctly at the call site

## Examples at a glance

To make all eight functions concrete, here is **one** representative int
array and **one** representative pair of strings, with what every function
in this assignment produces for them. Read this table first -- it is the
whole assignment in miniature.

```
 index:   0   1   2   3   4
 arr   = { 5,  3,  8,  3,  1 }   (n = 5)

 s        = "hello"
 a, b     = "apple", "apply"
```

| Call | Returns | Why |
|------|---------|-----|
| `reverse(arr, 5)` | `arr` becomes `{1, 3, 8, 3, 5}` | two pointers walk toward each other from both ends, swapping as they go; nothing is returned because the array is modified in place |
| `find(arr, 5, 8)` | pointer to `arr[2]` (`*p == 8`) | walking forward from `arr`, the first (and only) `8` is two positions in |
| `find(arr, 5, 9)` | `nullptr` | `9` never appears in `arr`, so the walk reaches the end without matching |
| `copy_ints(dst, arr, 5)` | `dst == {5, 3, 8, 3, 1}` | copies the ORIGINAL contents of `arr` (call this before `reverse`, or the copy reflects whatever `arr` currently holds) |
| `str_len("hello")` | `5` | five characters before the `'\0'` |
| `str_len("")` | `0` | the very first byte is already `'\0'`, so nothing is counted -- empty string is not the same as a null pointer |
| `str_copy(dst, "hello")` | `dst` holds `"hello"`, returns `dst` | copies every character up through and including the terminating `'\0'` |
| `str_compare("apple", "apply")` | negative (exactly `-20`) | first four characters match; at position 4, `'e'` (97+4=101) is less than `'y'` (121), so `'e' - 'y' = -20` |
| `str_compare("abc", "abc")` | `0` | every character matches, including both terminating `'\0'` bytes |
| `str_compare("abc", "ab")` | positive (exactly `99`) | first two characters match; at position 2, `"abc"` still has `'c'` (99) while `"ab"` has already hit `'\0'` (0), so `99 - 0 = 99` |
| `str_reverse("hello")` (in a mutable buffer) | buffer becomes `"olleh"`, returns pointer to it | swaps front/back characters inward, stopping before the `'\0'` (which never moves) |
| `str_find_char("hello", 'l')` | pointer to index 2 (the FIRST `'l'`) | walking forward, the first `'l'` in `"he[l]lo"` is at offset 2 -- the second `'l'` (offset 3) is never reached because the walk stops at the first match |
| `str_find_char("hello", 'z')` | `nullptr` | `'z'` never appears before the `'\0'`, so the walk falls off the end without matching |

## Worked example: watch `find(arr, 5, 8)` run, address by address

This is the clearest place to see pointer arithmetic happen, so here is every
step spelled out. We are searching `arr = {5, 3, 8, 3, 1}` for the value `8`,
using a pointer `p` that starts at `arr` and is compared against `end = arr +
n` (one past the last element -- the same fence-post idea used everywhere
else in this course).

Suppose (purely for illustration -- the real address will differ every time
you run the program) `arr` happens to live at address `0x1000`, and `int` is
4 bytes wide on this machine. Then `arr + i` is `0x1000 + 4*i`, because
pointer arithmetic on an `int*` advances by `sizeof(int)` bytes per step, not
by 1 byte -- this is exactly what lets `p++` mean "next int" instead of "next
byte."

| Step | `p` (address) | `*p` (value at that address) | `p == end`? | Action | Reason |
|------|----------------|-------------------------------|-------------|--------|--------|
| start | `0x1000` (`arr + 0`) | `5` | no (`end = 0x1014`) | `5 != 8`, keep going | not a match, and not off the end yet |
| 2 | `0x1004` (`arr + 1`) | `3` | no | `3 != 8`, keep going | still not a match |
| 3 | `0x1008` (`arr + 2`) | `8` | no | `8 == 8` -> return `p` | found it: the address itself, `0x1008`, is the answer |

The function returns `p`, which is `arr + 2` -- a pointer whose numeric
value is 8 bytes past `arr` (two `int`s at 4 bytes each), but whose MEANING
is "index 2." Dereferencing the returned pointer (`*find(arr, 5, 8)`) gives
back `8`, and subtracting the base (`find(arr, 5, 8) - arr`) gives back the
index `2`, without ever writing `arr[2]` anywhere in the implementation.
If the loop had instead reached `p == end` (`0x1014`) without matching --
which is exactly what happens searching for `9` -- the function returns
`nullptr` instead, and the caller must check for that before dereferencing.

## Task

Implement all functions in `pointer_toolkit.cpp`. Declarations are in
`pointer_toolkit.hpp` inside the `ptk` namespace (a named grouping that
prevents these function names from clashing with other code that happens to
define its own `reverse` or `find`).

### `reverse`

```cpp
void reverse(int* arr, int n);
```

**Reverse `arr[0..n-1]` in-place.** Use two pointers: one starting at the
front, one at the back, moving toward each other.

- **Example (odd length):** `arr = {5, 3, 8, 3, 1}` then `reverse(arr, 5)`
  leaves **`arr == {1, 3, 8, 3, 5}`**.
- **Example (even length):** `arr = {1, 2}` then `reverse(arr, 2)` leaves
  **`arr == {2, 1}`**.
- **Edge case (single element):** `arr = {7}` then `reverse(arr, 1)` leaves
  `arr == {7}` **unchanged** (a single element, or `n == 0`, has nothing to
  swap).

### `find`

```cpp
const int* find(const int* arr, int n, int target);
```

**Return a pointer to the first occurrence of `target`, or `nullptr` if not
found.** Walk the array with a pointer, not an index. (`arr = {5, 3, 8, 3,
1}` for all examples below.)

- **Example (found once):** `find(arr, 5, 8)` returns a pointer to `arr[2]`
  (**`*find(arr, 5, 8) == 8`**).
- **Tricky case (duplicate values):** `find(arr, 5, 3)` returns a pointer to
  `arr[1]` -- **the FIRST `3`**, not the one at index 3.
- **Example (not found):** `find(arr, 5, 9)` returns **`nullptr`** because
  `9` is absent.

### `copy_ints`

```cpp
void copy_ints(int* dst, const int* src, int n);
```

**Copy `n` ints from `src` to `dst`.** Advance both pointers simultaneously.
(`src = {5, 3, 8, 3, 1}`, `dst` uninitialized, for all examples below.)

- **Example (full copy):** `copy_ints(dst, src, 5)` leaves **`dst == {5, 3,
  8, 3, 1}`** and `src` unchanged.
- **Empty-input case:** `copy_ints(dst, src, 0)` leaves `dst` **untouched**
  (nothing to copy).
- **Edge case (bounds):** copying `n` elements never writes to `dst[n]` or
  beyond.

### `str_len`

```cpp
size_t str_len(const char* s);
```

**Return the number of characters before the null terminator** -- the
`'\0'` byte that C strings use to mark where the text ends, since a `char*`
has no built-in length of its own. Advance the pointer until you reach
`'\0'`.

- **Example (typical string):** `str_len("hello")` returns **`5`**.
- **Empty-input case:** `str_len("")` returns **`0`** (the buffer holds a
  single `'\0'` byte and nothing else).
- **Edge case (single character):** `str_len("a")` returns **`1`**.

### `str_copy`

```cpp
char* str_copy(char* dst, const char* src);
```

**Copy `src` into `dst` including the null terminator.** Returns `dst`.

- **Example (typical string):** `str_copy(dst, "hello")` leaves `dst`
  holding `"hello"` (**six bytes written**: `'h','e','l','l','o','\0'`) and
  returns the same pointer passed in as `dst`.
- **Empty-input case:** `str_copy(dst, "")` writes just the single `'\0'`
  byte and leaves `dst` **an empty string**.
- **Edge case (buffer size):** `dst` must be large enough to hold
  `str_len(src) + 1` characters, or the copy overruns the buffer.

### `str_compare`

```cpp
int str_compare(const char* a, const char* b);
```

**Compare two C strings lexicographically** (character by character, the
way words are ordered in a dictionary), like `strcmp`. Return negative,
zero, or positive.

- **Example (identical strings):** `str_compare("abc", "abc")` returns
  **`0`** (identical, including both `'\0'` bytes matching).
- **Example (differing character):** `str_compare("apple", "apply")` is
  **negative** -- the strings match through `"appl"`, then `'e'` (101) is
  less than `'y'` (121).
- **Tricky case (prefix string):** `str_compare("abc", "ab")` is
  **positive** -- matches through `"ab"`, then `"abc"` still has `'c'` (99)
  while `"ab"` has already hit `'\0'` (0). A longer string that starts with
  a shorter one always compares greater.

### `str_reverse`

```cpp
char* str_reverse(char* s);
```

**Reverse the string in-place** (up to, but not including, the null
terminator). Returns `s`.

- **Example (typical string):** `s = "hello"` (in a mutable buffer) then
  `str_reverse(s)` leaves **`s == "olleh"`** and returns the same pointer
  passed in.
- **Edge case (single character):** `s = "a"` then `str_reverse(s)` leaves
  `s == "a"` **unchanged** (one character, nothing to swap).
- **Empty-input case:** `s = ""` then `str_reverse(s)` leaves `s == ""`
  **unchanged** (the `'\0'` itself never moves).

### `str_find_char`

```cpp
const char* str_find_char(const char* s, char c);
```

**Return a pointer to the first occurrence of `c` in `s`, or `nullptr` if
not found.**

- **Tricky case (duplicate characters):** `str_find_char("hello", 'l')`
  returns a pointer to **index 2** -- the FIRST `'l'` in `"he[l]lo"`, not
  the second one at index 3.
- **Example (not found):** `str_find_char("hello", 'z')` returns
  **`nullptr`** (`'z'` never appears).
- **Empty-input case:** `str_find_char("", 'a')` returns **`nullptr`** (an
  empty string has no characters before its terminator to match against).

## Files

| File | Purpose |
|------|---------|
| `pointer_toolkit.hpp` | Declarations -- do not modify |
| `pointer_toolkit.cpp` | Write your implementation here (create this file) |

## Compilation and Testing

```bash
g++ -std=c++17 -Wall -I. -o tests pointer_toolkit.cpp visible-tests/test_visible.cpp
./tests
```

## Constraints

- Traverse arrays and strings using pointer arithmetic (incrementing/decrementing
  a pointer), not with `arr[i]` subscript expressions.
- No `<cstring>` functions (strlen, strcpy, strcmp, etc.) in your implementations.

## Grading

| Component | Points |
|---|---|
| reverse (3 cases) | 15 |
| find (3 cases) | 15 |
| copy_ints (2 cases) | 10 |
| str_len (2 cases) | 10 |
| str_copy (2 cases) | 10 |
| str_compare (3 cases) | 15 |
| str_reverse (2 cases) | 10 |
| str_find_char (2 cases) | 10 |
| Gimme (>= 50% correct) | 5 |
| **Total** | **100** |

## Going further

- Rewrite `reverse` and `find` using array subscripts (`arr[i]`) and compare
  the assembly output at `-O2`. Are the two versions identical?
- Add a `str_contains(const char* haystack, const char* needle)` function
  without using `strstr`. Implement it using only the pointer patterns from this
  assignment.
- Run your implementations under Valgrind (a tool that watches your program run and
  reports memory errors like reading past the end of an array) and confirm no
  out-of-bounds reads. Then deliberately break one function and see how Valgrind
  reports it.
