# lazy-pipeline -- starter file.
#
# Implement five generator functions forming a small log-processing
# pipeline. See README.md for the exact spec of each function.
#
# Do not rename this file. Do not import anything except (optionally)
# typing -- itertools is specifically forbidden, since the whole point
# of this assignment is to hand-write the pause/resume logic yourself,
# not reach for itertools.islice or itertools.chain to do it for you.
#
# The signatures below are left UNANNOTATED on purpose: the type-annotation
# bonus asks you to add the Iterable/Iterator hints yourself (the exact
# types are in the README's per-function spec). Iterable and Iterator are
# imported below, ready for you to annotate with.

from __future__ import annotations

from typing import Iterable, Iterator  # noqa: F401 -- for you to annotate with


def parse_records(lines):
    """Lazily parse "LEVEL:message" lines into {"level", "msg"} dicts, skipping malformed lines."""
    raise NotImplementedError


def only_level(records, level):
    """Lazily filter records down to those whose "level" equals level exactly."""
    raise NotImplementedError


def take(iterable, n):
    """Yield at most n items from iterable, consuming no more than n items from the source."""
    raise NotImplementedError


def running_count(records):
    """Yield the cumulative count of records seen so far, one per input record."""
    raise NotImplementedError


def chunked(iterable, size):
    """Yield successive lists of up to size items; the final partial chunk is included."""
    raise NotImplementedError
