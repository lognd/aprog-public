"""
Visible tests for C++ to Python Phrasebook.

Run locally:
    python -m pytest visible-tests/test_visible.py -v
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from phrasebook import (  # noqa: E402
    is_palindrome_sentence,
    most_frequent,
    reverse_words,
    unique_words_sorted,
    word_count,
    word_frequencies,
)


def test_word_count_basic():
    assert word_count("the quick brown fox") == 4


def test_word_count_punctuation():
    assert word_count("Hello, world!") == 2


def test_unique_words_sorted_basic():
    assert unique_words_sorted("the fox and the hound") == ["and", "fox", "hound", "the"]


def test_unique_words_sorted_case_sensitive():
    assert unique_words_sorted("The the THE") == ["THE", "The", "the"]


def test_word_frequencies_basic():
    assert word_frequencies("a b a c b a") == {"a": 3, "b": 2, "c": 1}


def test_most_frequent_basic():
    assert most_frequent("a b a c b a", 2) == ["a", "b"]


def test_most_frequent_ties_alphabetical():
    assert most_frequent("a a c b", 3) == ["a", "b", "c"]


def test_reverse_words_basic():
    assert reverse_words("the quick brown fox") == "fox brown quick the"


def test_is_palindrome_sentence_basic():
    assert is_palindrome_sentence("racecar") is True


def test_is_palindrome_sentence_with_punctuation():
    assert is_palindrome_sentence("A man, a plan, a canal: Panama") is True
