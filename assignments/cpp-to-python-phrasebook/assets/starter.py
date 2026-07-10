# cpp-to-python-phrasebook -- starter file.
#
# You already built these six ideas once, in C++, for word-ledger. This time
# you are porting them to Python -- same underlying logic, new syntax, and a
# few genuinely different tools (Python's dict, sort-by-key, and string
# methods replace std::map, std::sort with a comparator, and hand-rolled
# character loops).
#
# Do not rename this file. Do not import anything -- every function below
# is implementable with plain string/list/dict operations from the language
# itself, no standard-library modules required (the reference solution uses
# none). See README.md for the exact spec of each function, including the
# word-tokenization rule shared by all of them.


def word_count(text):
    """Return the number of words in text."""
    raise NotImplementedError


def unique_words_sorted(text):
    """Return a sorted list of the distinct words in text (case-sensitive)."""
    raise NotImplementedError


def word_frequencies(text):
    """Return a dict mapping each word in text to its occurrence count."""
    raise NotImplementedError


def most_frequent(text, k):
    """Return the k most frequent words in text, ties broken alphabetically ascending."""
    raise NotImplementedError


def reverse_words(text):
    """Return text's words, in reverse order, joined by a single space."""
    raise NotImplementedError


def is_palindrome_sentence(text):
    """Return True if text reads the same forwards and backwards, ignoring case and punctuation."""
    raise NotImplementedError
