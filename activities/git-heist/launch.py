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


if __name__ == "__main__":
    main()
