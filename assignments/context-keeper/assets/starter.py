# context-keeper -- starter file.
#
# Implement two context-manager classes, one @contextmanager-based
# generator function, and two plain functions. See README.md for the
# exact spec of each.
#
# Stdlib only (contextlib is explicitly allowed -- it is the standard
# tool for the @contextmanager-based transaction function).
#
# The signatures are left UNANNOTATED on purpose: the type-annotation
# bonus asks you to add the hints yourself (the exact types are in the
# README). The one exception is the __enter__/__exit__ pair below, whose
# context-manager-protocol signatures are pre-filled as scaffolding -- you
# still annotate __init__, transaction, divide_or, and cleanup_chain.

from __future__ import annotations

from contextlib import contextmanager
from typing import Callable, Iterator  # noqa: F401 -- for you to annotate with


class Workspace:
    """Context manager that journals "open" on entry and "close" on exit, always, never suppressing."""

    def __init__(self, journal):
        raise NotImplementedError

    def __enter__(self) -> "Workspace":
        raise NotImplementedError

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None,
                 exc_tb: object) -> bool:
        raise NotImplementedError


class Muffle:
    """Context manager that suppresses only exceptions matching exc_type (or a subclass); records what it caught."""

    def __init__(self, exc_type):
        raise NotImplementedError

    def __enter__(self) -> "Muffle":
        raise NotImplementedError

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None,
                 exc_tb: object) -> bool:
        raise NotImplementedError


@contextmanager
def transaction(ledger):
    """Yield a working copy of ledger; commit (mutate ledger in place) only on clean exit, else discard."""
    raise NotImplementedError
    yield  # pragma: no cover -- keeps this a generator function before you fill it in


def divide_or(a, b, fallback):
    """Return a / b, or fallback if that raises ZeroDivisionError."""
    raise NotImplementedError


def cleanup_chain(steps):
    """Run every step in order, always running all remaining steps even if one raises; return caught exception type names in order."""
    raise NotImplementedError
