#!/usr/bin/env python3
"""
Extracts a fresh copy of the git-heist repo into a temp directory
and opens a shell inside it. Cleans up on exit.
Does not require sudo.
Usage: python3 launch.py
"""
import os
import sys
import shutil
import subprocess
import tempfile
import atexit
import zipfile
import textwrap

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ZIP = os.path.join(SCRIPT_DIR, "repo.zip")


def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def main():
    if not os.path.isfile(REPO_ZIP):
        die(f"repo.zip not found; this file should be included.")

    work_dir = tempfile.mkdtemp(prefix="git-heist-")

    def cleanup():
        shutil.rmtree(work_dir, ignore_errors=True)

    atexit.register(cleanup)

    with zipfile.ZipFile(REPO_ZIP, "r") as zf:
        zf.extractall(work_dir)

    # repo.zip contains a single top-level directory
    entries = os.listdir(work_dir)
    if len(entries) != 1:
        die("unexpected zip structure")
    repo_dir = os.path.join(work_dir, entries[0])

    rcfile = tempfile.NamedTemporaryFile(mode="w", suffix=".rc", delete=False)
    rcfile.write(textwrap.dedent(f"""\
        PS1='\\u@git-heist:\\W\\$ '
        cd "{repo_dir}"
        echo ""
        echo "  Welcome to git-heist. The repo is at: {repo_dir}"
        echo "  Type 'exit' or Ctrl-D when done."
        echo ""
    """))
    rcfile.close()
    atexit.register(lambda: os.path.exists(rcfile.name) and os.remove(rcfile.name))

    shell = os.environ.get("SHELL", "/bin/bash")
    subprocess.run([shell, "--rcfile", rcfile.name])

    _check_history_clean(repo_dir)


# Markers that only ever appear in the leaked .env file. If any of these
# show up in the full history of any ref after the student exits, the
# credentials commit was not actually removed (or was reintroduced, e.g.
# via a merge that replayed it onto a rewritten branch). Best-effort
# sanity check only, not a grading gate -- git-heist is self-checked via
# `cat PASSPHRASE.txt`.
_CREDENTIAL_MARKERS = ("DB_PASSWORD", "API_KEY", "SECRET_TOKEN")


def _check_history_clean(repo_dir):
    """Scan every ref's full history for leaked-credential markers and warn if found."""
    if not os.path.isdir(os.path.join(repo_dir, ".git")):
        return
    try:
        result = subprocess.run(
            ["git", "log", "--all", "-p"],
            cwd=repo_dir, capture_output=True, text=True, check=True,
        )
    except subprocess.CalledProcessError:
        return

    hits = [m for m in _CREDENTIAL_MARKERS if m in result.stdout]
    if hits:
        print("")
        print("  warning: the repo's history still contains leaked credentials")
        print(f"  (found: {', '.join(hits)}) on at least one ref.")
        print("  The credentials commit was not fully removed -- check every")
        print("  branch, not just main, for its own copy of the problem.")
        print("")


if __name__ == "__main__":
    main()
