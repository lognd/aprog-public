#!/usr/bin/env python3
"""
String Methods activity launcher.
Opens a shell for the student to work in.  The LMS passcode is the word
spelled by the first letter of each output line when the fix is correct.
"""
import os, sys, shutil, subprocess, tempfile, zipfile, textwrap

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ZIP   = os.path.join(SCRIPT_DIR, "repo.zip")

_LINE_WIDTH = 70

def _banner(title):
    print("=" * _LINE_WIDTH)
    pad = (_LINE_WIDTH - len(title) - 2) // 2
    print(" " * pad + " " + title + " " + " " * pad)
    print("=" * _LINE_WIDTH)

def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def main():
    if not os.path.isfile(REPO_ZIP):
        die("repo.zip not found.")

    work_dir = tempfile.mkdtemp(prefix="string-methods-")

    with zipfile.ZipFile(REPO_ZIP, "r") as zf:
        zf.extractall(work_dir)

    entries = os.listdir(work_dir)
    if len(entries) != 1:
        shutil.rmtree(work_dir, ignore_errors=True)
        die("unexpected zip structure")
    repo_dir = os.path.join(work_dir, entries[0])

    rcfile = tempfile.NamedTemporaryFile(mode="w", suffix=".rc", delete=False)
    banner_text = textwrap.dedent(f"""\

      ============================================================
       String Methods -- Fix the Word Wrapper
      ============================================================

       Files: wrap.cpp, Makefile

       Step 1 -- compile and run to see the broken output:
         make run

       Step 2 -- find and fix the bugs in word_wrap(), then
       run again:
         make run

       When the output looks correct, type 'exit'.
       The LMS passcode is the word (all lowercase) spelled by
       the first letter of each output line, read top to bottom.
      ============================================================

    """)
    rcfile.write(textwrap.dedent(f"""\
        PS1='\\u@string-methods:\\W\\$ '
        cd "{repo_dir}"
        cat << 'BANNER'
{banner_text}BANNER
    """))
    rcfile.close()

    try:
        subprocess.run([os.environ.get("SHELL", "/bin/bash"), "--rcfile", rcfile.name])

        print()
        _banner("String Methods -- Done")
        print()
        print("  The LMS passcode is the word (all lowercase) spelled by")
        print("  the first letter of each output line, read top to bottom.")
        print()
    finally:
        try:
            os.remove(rcfile.name)
        except OSError:
            pass
        shutil.rmtree(work_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
