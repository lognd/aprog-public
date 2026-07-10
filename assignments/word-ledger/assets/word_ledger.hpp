// Word Ledger -- implement every function in this file.
// Rules:
//   - Mark every function inline.
//   - Do not use exceptions (throw/try/catch) anywhere in this file.
//   - Words are compared case-sensitively ("The" and "the" are different
//     words). Nothing in this assignment lowercases input for you.
#pragma once

#include <map>
#include <set>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

namespace wledger {

// Returns how many times each word appears in `words`, as a map sorted by
// word (alphabetically). Every distinct word in `words` appears as a key,
// mapped to its total count. Empty input -> empty map.
inline std::map<std::string, int> word_frequencies(const std::vector<std::string>& words) {
    // TODO
    return {};
}

// Returns, for every distinct word in `words`, the index of that word's
// FIRST appearance in `words` (0-based). Empty input -> empty map.
inline std::unordered_map<std::string, int> first_occurrence_index(
    const std::vector<std::string>& words) {
    // TODO
    return {};
}

// Returns the set of distinct words in `words`, in sorted order (a
// std::set always iterates in sorted order -- that sorted order IS the
// "unique_words_sorted" result). Empty input -> empty set.
inline std::set<std::string> unique_words_sorted(const std::vector<std::string>& words) {
    // TODO
    return {};
}

// Returns the set INTERSECTION: every word that appears in BOTH `a` and
// `b`, in sorted order. Either input being empty -> empty result.
inline std::set<std::string> common_words(
    const std::vector<std::string>& a, const std::vector<std::string>& b) {
    // TODO
    return {};
}

// Returns the set DIFFERENCE: every word that appears in `a` but does NOT
// appear anywhere in `b`, in sorted order. `a` empty -> empty result. `b`
// empty -> every distinct word in `a`.
inline std::set<std::string> words_only_in(
    const std::vector<std::string>& a, const std::vector<std::string>& b) {
    // TODO
    return {};
}

// Returns the top `k` most frequent words in `words`, as (word, count)
// pairs, ordered by count DESCENDING; ties (equal counts) are broken by
// word, ALPHABETICALLY ASCENDING. If fewer than `k` distinct words exist,
// returns all of them. k <= 0 or words empty -> empty result.
//
// Implementation note: with a small k, a repeated max-scan over the
// frequency map (find the highest-count remaining word k times) is the
// expected approach -- no sorting comparator or lambda required.
inline std::vector<std::pair<std::string, int>> most_frequent(
    const std::vector<std::string>& words, int k) {
    // TODO
    return {};
}

} // namespace wledger
