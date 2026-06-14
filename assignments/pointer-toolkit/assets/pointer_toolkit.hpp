#pragma once
#include <cstddef>

namespace ptk {

// Reverses arr[0..n-1] in-place using pointer arithmetic.
void reverse(int* arr, int n);

// Returns a pointer to the first occurrence of target in arr[0..n-1],
// or nullptr if not found. Must use pointer arithmetic (not indexing).
const int* find(const int* arr, int n, int target);

// Copies n ints from src to dst. Regions do not overlap.
void copy_ints(int* dst, const int* src, int n);

// Returns the number of characters before the null terminator (like strlen).
// Must advance a pointer rather than use indexing.
size_t str_len(const char* s);

// Copies src into dst including the null terminator. Returns dst.
char* str_copy(char* dst, const char* src);

// Compares a and b lexicographically.
// Returns negative if a < b, zero if a == b, positive if a > b.
int str_compare(const char* a, const char* b);

// Reverses s in-place. Returns s.
char* str_reverse(char* s);

// Returns a pointer to the first occurrence of c in s, or nullptr if not found.
const char* str_find_char(const char* s, char c);

} // namespace ptk
