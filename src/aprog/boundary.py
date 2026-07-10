"""Single source of truth for the public/private boundary scan used by both
`aprog validate` and `aprog scan-public`.

Both commands used to reimplement the same rglob-and-match algorithm with
constant sets that had quietly drifted apart (`scan-public` allowed "grader"
as a public directory name; `validate` did not). This module owns the union
of both rule sets and the one scan function both commands call.
"""

from __future__ import annotations

import re
from pathlib import Path

#: Kebab-case slug pattern shared by assignment and template slugs.
SLUG_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")

#: File/directory basenames that must never appear anywhere under a public
#: assignment root.
PROHIBITED_NAMES = frozenset(
    {
        "solution",
        "solutions",
        "hidden",
        "hidden-tests",
        "hidden_tests",
        "private",
        "private-notes.md",
        "answer-key.md",
        "grader",
        "pipeline.py",
    }
)

#: Directory names that make everything beneath them private, regardless of
#: what the files themselves are named.
PRIVATE_DIRS = frozenset(
    {
        "solution",
        "solutions",
        "hidden",
        "hidden-tests",
        "hidden_tests",
        "private",
        "grader",
    }
)

#: Filename prefixes that flag a file as a leaked solution/answer artifact.
PROHIBITED_PATTERNS = (
    "solution.",
    "answer.",
    "reference-solution.",
    "reference_solution.",
)

#: Directories that are always safe to keep in the public assignment tree.
SAFE_DIRS = frozenset({"visible-tests", "assets", "expected"})

#: Slugs and directory names reserved because they collide with the
#: public/private boundary vocabulary above.
RESERVED_SLUGS = frozenset(
    {
        "private",
        "hidden",
        "solution",
        "solutions",
        "answer",
        "answers",
        "key",
        "generated",
        "secret",
        "grader",
        "pipeline",
    }
)


def scan_public_violations(assignment_root: Path) -> list[str]:
    """Walk a public assignment tree and report every boundary violation found."""
    violations: list[str] = []
    for path in assignment_root.rglob("*"):
        rel = path.relative_to(assignment_root)
        parts = rel.parts
        name = path.name

        if name in PROHIBITED_NAMES:
            violations.append(f"{rel} -- prohibited name")
            continue

        for part in parts[:-1]:
            if part in PRIVATE_DIRS:
                violations.append(f"{rel} -- '{part}/' directory is private")
                break

        if path.is_file():
            for pat in PROHIBITED_PATTERNS:
                if name.startswith(pat) or name == pat.rstrip("."):
                    violations.append(f"{rel} -- matches prohibited pattern '{pat}*'")
                    break

    return violations
