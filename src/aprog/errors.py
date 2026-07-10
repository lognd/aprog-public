"""Shared CLI error/exit-code helpers so every command reports failures the same way."""

from __future__ import annotations

from enum import IntEnum
from typing import NoReturn

import typer
from rich.console import Console

console = Console()


class ExitCode(IntEnum):
    """Process exit codes used across aprog commands. Values are load-bearing:
    scripts and CI steps branch on them, so they must never be renumbered."""

    OK = 0
    ERROR = 1
    USAGE = 2
    STALE = 4
    MISSING_GRADER = 5


def fail(message: str, code: ExitCode = ExitCode.ERROR) -> NoReturn:
    """Print a standardized `[red]Error:[/red] ...` line and exit with `code`.

    Always raised with `from None`: typer.Exit carries no diagnostic payload,
    so chaining the original exception onto it only adds console noise.
    """
    console.print(message)
    raise typer.Exit(code) from None
