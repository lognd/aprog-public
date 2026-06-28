// Sentence Tools -- implement all functions in this file.
// Rules:
//   - Mark every function inline.
//   - Do not #include <string> or use std::string.
//   - Do not allocate heap memory.
//   - You may use <cstring>, <cctype>, and <cstddef>.
#pragma once
#include <cctype>
#include <cstddef>
#include <cstring>

namespace stools {

// Returns the number of whitespace-separated words in s.
// "  hello  world  " -> 2.  Empty or all-spaces -> 0.
inline int word_count(const char* s) {
    // TODO
    return 0;
}

// Copies the n-th word (0-indexed) into dst, writing at most dst_len-1
// characters plus a null terminator.  Returns true if the n-th word
// exists, false otherwise.  On failure, dst[0] is set to '\0'.
// Precondition: dst_len >= 1.
inline bool word_at(const char* s, int n, char* dst, size_t dst_len) {
    // TODO
    dst[0] = '\0';
    return false;
}

// Returns true if `word` appears as a complete word in `sentence`.
// "cat" must NOT match in "concatenate" or "scat".
// Matching is case-sensitive.
inline bool contains_word(const char* sentence, const char* word) {
    // TODO
    return false;
}

// Removes all leading and trailing spaces from s in-place.
// Interior spaces are left unchanged.
// "  hello   world  " -> "hello   world".
inline void trim(char* s) {
    // TODO
}

// Capitalizes the first character of every word in s in-place.
// All other characters are left unchanged.
// "hello world" -> "Hello World".
inline void capitalize_words(char* s) {
    // TODO
}

// Converts every character of s to lowercase in-place.
inline void to_lower(char* s) {
    // TODO
}

// Returns the 0-based index of the first whole-word occurrence of `word`
// in `s`.  Returns -1 if not found.
// "the cat sat" with word="cat" -> 1.
inline int word_index(const char* s, const char* word) {
    // TODO
    return -1;
}

} // namespace stools
