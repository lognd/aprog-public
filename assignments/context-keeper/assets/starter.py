# context-keeper -- starter file.
#
# Implement two context-manager classes, one @contextmanager-based
# generator function, and two plain functions. See README.md for the
# exact spec of each.
#
# Stdlib only (contextlib is explicitly allowed -- it is the standard
# tool for the @contextmanager-based transaction function). Type hints
# are REQUIRED on every function/method signature.

from __future__ import annotations

from contextlib import contextmanager
from typing import Callable, Iterator


class Workspace:
    """Context manager that journals "open" on entry and "close" on exit, always, never suppressing."""

    def __init__(self, journal: list[str]) -> None:
        raise NotImplementedError

    def __enter__(self) -> "Workspace":
        raise NotImplementedError

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None,
                 exc_tb: object) -> bool:
        raise NotImplementedError


class Muffle:
    """Context manager that suppresses only exceptions matching exc_type (or a subclass); records what it caught."""

    def __init__(self, exc_type: type[BaseException]) -> None:
        raise NotImplementedError

    def __enter__(self) -> "Muffle":
        raise NotImplementedError

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None,
                 exc_tb: object) -> bool:
        raise NotImplementedError


@contextmanager
def transaction(ledger: list) -> Iterator[list]:
    """Yield a working copy of ledger; commit (mutate ledger in place) only on clean exit, else discard."""
    raise NotImplementedError
    yield  # pragma: no cover -- keeps this a generator function before you fill it in


def divide_or(a: float, b: float, fallback: float) -> float:
    """Return a / b, or fallback if that raises ZeroDivisionError."""
    raise NotImplementedError


def cleanup_chain(steps: list[Callable[[], None]]) -> list[str]:
    """Run every step in order, always running all remaining steps even if one raises; return caught exception type names in order."""
    raise NotImplementedError
