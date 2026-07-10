// Visible Catch2 test suite for Word Ledger.
//
// Compile and run locally:
//   mkdir build && cd build
//   cmake .. -DSUBMISSION_DIR=<path-to-your-submission>
//   cmake --build .
//   ./word-ledger_tests

#include <catch2/catch_test_macros.hpp>
#include "word_ledger.hpp"

using namespace wledger;

TEST_CASE("word_frequencies basic", "[word_frequencies]") {
    std::vector<std::string> words = {"the", "cat", "sat", "the", "cat", "the"};
    auto freq = word_frequencies(words);
    REQUIRE(freq.size() == 3);
    REQUIRE(freq.at("the") == 3);
    REQUIRE(freq.at("cat") == 2);
    REQUIRE(freq.at("sat") == 1);
}

TEST_CASE("first_occurrence_index basic", "[first_occurrence_index]") {
    std::vector<std::string> words = {"a", "b", "a", "c", "b"};
    auto idx = first_occurrence_index(words);
    REQUIRE(idx.size() == 3);
    REQUIRE(idx.at("a") == 0);
    REQUIRE(idx.at("b") == 1);
    REQUIRE(idx.at("c") == 3);
}

TEST_CASE("unique_words_sorted basic", "[unique_words_sorted]") {
    std::vector<std::string> words = {"banana", "apple", "banana", "cherry"};
    auto u = unique_words_sorted(words);
    std::vector<std::string> as_vec(u.begin(), u.end());
    REQUIRE(as_vec == std::vector<std::string>{"apple", "banana", "cherry"});
}

TEST_CASE("common_words basic", "[common_words]") {
    std::vector<std::string> a = {"cat", "dog", "bird"};
    std::vector<std::string> b = {"dog", "fish", "cat"};
    auto c = common_words(a, b);
    std::vector<std::string> as_vec(c.begin(), c.end());
    REQUIRE(as_vec == std::vector<std::string>{"cat", "dog"});
}

TEST_CASE("words_only_in basic", "[words_only_in]") {
    std::vector<std::string> a = {"cat", "dog", "bird"};
    std::vector<std::string> b = {"dog", "fish"};
    auto d = words_only_in(a, b);
    std::vector<std::string> as_vec(d.begin(), d.end());
    REQUIRE(as_vec == std::vector<std::string>{"bird", "cat"});
}

TEST_CASE("most_frequent basic", "[most_frequent]") {
    std::vector<std::string> words = {"a", "b", "a", "c", "b", "a"};
    auto top = most_frequent(words, 2);
    REQUIRE(top.size() == 2);
    REQUIRE(top[0] == std::make_pair(std::string("a"), 3));
    REQUIRE(top[1] == std::make_pair(std::string("b"), 2));
}
