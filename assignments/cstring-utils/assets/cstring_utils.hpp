#pragma once
#include <cstddef>

namespace csu {

// Returns the number of characters before the null terminator (like strlen).
size_t length(const char* s);

// Copies src into dst including the null terminator. Returns dst.
char* copy(char* dst, const char* src);

// Appends src onto the end of dst. Returns dst. dst must have enough space.
char* append(char* dst, const char* src);

// Compares a and b lexicographically (like strcmp).
// Returns negative if a < b, zero if a == b, positive if a > b.
int compare(const char* a, const char* b);

// Returns a pointer to the first occurrence of c in s, or nullptr.
const char* find_char(const char* s, char c);

// Returns a pointer to the first occurrence of needle in haystack, or nullptr.
// Naive O(n*m) search is acceptable.
const char* find_str(const char* haystack, const char* needle);

// Reverses s in-place. Returns s.
char* reverse(char* s);

// Returns true if every character in s is a decimal digit ('0'-'9').
// An empty string returns true.
bool is_digits(const char* s);

// Converts n (>= 0) to its decimal string representation and writes it
// into buf. buf must be at least 12 bytes. Returns buf.
char* int_to_str(int n, char* buf);

} // namespace csu
