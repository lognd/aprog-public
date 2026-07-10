"""Visible tests for Lazy Pipeline.

Run locally:
    python -m pytest visible-tests/test_visible.py -v
"""

import os
import sys

sys.path.insert(0, os.environ["SUBMISSION_DIR"])

from pipeline import chunked, only_level, parse_records, running_count, take  # noqa: E402


# ---------------------------------------------------------------------------
# parse_records
# ---------------------------------------------------------------------------


def test_parse_records_basic():
    lines = ["INFO:started", "ERROR:boom", "DEBUG:trace"]
    records = list(parse_records(lines))
    assert records == [
        {"level": "INFO", "msg": "started"},
        {"level": "ERROR", "msg": "boom"},
        {"level": "DEBUG", "msg": "trace"},
    ]


def test_parse_records_skips_malformed():
    lines = ["INFO:ok", "not a valid line", "ERROR:bad"]
    records = list(parse_records(lines))
    assert records == [
        {"level": "INFO", "msg": "ok"},
        {"level": "ERROR", "msg": "bad"},
    ]


def test_parse_records_message_may_contain_colons():
    lines = ["INFO:time is 10:30:00"]
    records = list(parse_records(lines))
    assert records == [{"level": "INFO", "msg": "time is 10:30:00"}]


def test_parse_records_returns_a_generator():
    result = parse_records(["INFO:x"])
    assert hasattr(result, "__next__")


def test_parse_records_empty_input():
    assert list(parse_records([])) == []


# ---------------------------------------------------------------------------
# only_level
# ---------------------------------------------------------------------------


def test_only_level_filters():
    records = [
        {"level": "INFO", "msg": "a"},
        {"level": "ERROR", "msg": "b"},
        {"level": "INFO", "msg": "c"},
    ]
    result = list(only_level(records, "INFO"))
    assert result == [{"level": "INFO", "msg": "a"}, {"level": "INFO", "msg": "c"}]


def test_only_level_no_matches():
    records = [{"level": "INFO", "msg": "a"}]
    assert list(only_level(records, "ERROR")) == []


def test_only_level_returns_a_generator():
    result = only_level([{"level": "INFO", "msg": "a"}], "INFO")
    assert hasattr(result, "__next__")


# ---------------------------------------------------------------------------
# take
# ---------------------------------------------------------------------------


def test_take_fewer_than_available():
    assert list(take([1, 2, 3, 4, 5], 3)) == [1, 2, 3]


def test_take_more_than_available():
    assert list(take([1, 2], 5)) == [1, 2]


def test_take_zero():
    assert list(take([1, 2, 3], 0)) == []


def test_take_exact_count():
    assert list(take([1, 2, 3], 3)) == [1, 2, 3]


def test_take_returns_a_generator():
    result = take([1, 2, 3], 2)
    assert hasattr(result, "__next__")


# ---------------------------------------------------------------------------
# running_count
# ---------------------------------------------------------------------------


def test_running_count_basic():
    records = [{"level": "INFO", "msg": "a"}] * 4
    assert list(running_count(records)) == [1, 2, 3, 4]


def test_running_count_empty():
    assert list(running_count([])) == []


def test_running_count_returns_a_generator():
    result = running_count([{"level": "INFO", "msg": "a"}])
    assert hasattr(result, "__next__")


# ---------------------------------------------------------------------------
# chunked
# ---------------------------------------------------------------------------


def test_chunked_exact_multiple():
    assert list(chunked([1, 2, 3, 4], 2)) == [[1, 2], [3, 4]]


def test_chunked_partial_final_chunk():
    assert list(chunked([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]


def test_chunked_size_larger_than_input():
    assert list(chunked([1, 2], 5)) == [[1, 2]]


def test_chunked_empty_input():
    assert list(chunked([], 3)) == []


def test_chunked_returns_a_generator():
    result = chunked([1, 2, 3], 2)
    assert hasattr(result, "__next__")


# ---------------------------------------------------------------------------
# full pipeline, chained
# ---------------------------------------------------------------------------


def test_full_pipeline_chained():
    lines = [
        "INFO:one", "ERROR:bad", "INFO:two", "garbage",
        "INFO:three", "ERROR:worse", "INFO:four", "INFO:five",
    ]
    records = parse_records(lines)
    info_only = only_level(records, "INFO")
    limited = take(info_only, 3)
    result = list(limited)
    assert result == [
        {"level": "INFO", "msg": "one"},
        {"level": "INFO", "msg": "two"},
        {"level": "INFO", "msg": "three"},
    ]
