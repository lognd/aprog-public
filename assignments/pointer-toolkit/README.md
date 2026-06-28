# Pointer Toolkit

## Overview

A pointer stores the address of another object. Pointer arithmetic lets you navigate
memory by incrementing or decrementing the pointer itself rather than using an index.
In this assignment you implement eight array and string utility functions using only
pointer arithmetic -- no subscript operators on the core traversals.

## Learning goals

- Navigate arrays and C strings using pointer arithmetic (`p++`, `*(p + i)`) without subscript operators
- Use two-pointer technique for in-place reversal of arrays and strings
- Implement C string utilities (`strlen`, `strcpy`, `strcmp`) from first principles
- Return `nullptr` to signal "not found" and use it correctly at the call site

## Task

Implement all functions in `pointer_toolkit.cpp`. Declarations are in
`pointer_toolkit.hpp` inside the `ptk` namespace.

### `reverse`

```cpp
void reverse(int* arr, int n);
```

Reverse arr[0..n-1] in-place. Use two pointers: one starting at the front, one at
the back, moving toward each other.

### `find`

```cpp
const int* find(const int* arr, int n, int target);
```

Return a pointer to the first occurrence of target, or nullptr if not found.
Walk the array with a pointer, not an index.

### `copy_ints`

```cpp
void copy_ints(int* dst, const int* src, int n);
```

Copy n ints from src to dst. Advance both pointers simultaneously.

### `str_len`

```cpp
size_t str_len(const char* s);
```

Return the number of characters before the null terminator. Advance the pointer
until you reach `'\0'`.

### `str_copy`

```cpp
char* str_copy(char* dst, const char* src);
```

Copy src into dst including the null terminator. Returns dst.

### `str_compare`

```cpp
int str_compare(const char* a, const char* b);
```

Compare two C strings lexicographically, like `strcmp`. Return negative, zero, or
positive.

### `str_reverse`

```cpp
char* str_reverse(char* s);
```

Reverse the string in-place (up to, but not including, the null terminator).
Returns s.

### `str_find_char`

```cpp
const char* str_find_char(const char* s, char c);
```

Return a pointer to the first occurrence of c in s, or nullptr if not found.

## Files

- `pointer_toolkit.hpp` -- declarations; do not modify
- `pointer_toolkit.cpp` -- your implementations (create this file)

## Compilation & Testing

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
- Run your implementations under Valgrind and confirm no out-of-bounds reads.
  Then deliberately break one function and see how Valgrind reports it.
