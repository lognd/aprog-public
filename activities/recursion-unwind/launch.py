#!/usr/bin/env python3
"""
recursion-unwind activity launcher.
Students are given a broken recursive program and must fix two bugs:
  1. A missing base case in digit_sum (causes infinite recursion)
  2. An incorrect index in reverse_str (off-by-one in swap)
The passphrase unlocks when the program produces the correct output.
"""

import atexit
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import hashlib as _hl
import hmac as _hm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

_SALT = bytes.fromhex("a3f1b2c4d5e6f7a8b9c0d1e2f3a4b5c6")
_KDF_ITERS = 100000
_BLOB = "3ce2d0617544b7d26304513787debe5daa39a2ba9bb8a0537e98090e237b4f56300d76f883c3484c44d23a153fbe96"

_LINE_WIDTH = 70


def _stream(key, length):
    ks, i = b"", 0
    while len(ks) < length:
        ks += _hl.sha256(key + i.to_bytes(4, "little")).digest()
        i += 1
    return ks[:length]


def _decrypt(got):
    key = _hl.pbkdf2_hmac("sha256", got.encode(), _SALT, _KDF_ITERS)
    blob = bytes.fromhex(_BLOB)
    ct, mac = blob[:-32], blob[-32:]
    if not _hm.compare_digest(mac, _hm.new(key, ct, _hl.sha256).digest()):
        return None
    return bytes(a ^ b for a, b in zip(ct, _stream(key, len(ct)))).decode()


def _banner(title):
    print("=" * _LINE_WIDTH)
    pad = (_LINE_WIDTH - len(title) - 2) // 2
    print(" " * pad + " " + title + " " * pad)
    print("=" * _LINE_WIDTH)


def _hr():
    print("-" * _LINE_WIDTH)


def _wrap(text):
    for line in textwrap.wrap(
        text, width=_LINE_WIDTH - 4, initial_indent="  ", subsequent_indent="    "
    ):
        print(line)


def _show_passphrase(p):
    print()
    _hr()
    print(f"  Passphrase: {p}")
    _hr()
    print()


def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def _setup_work_dir():
    work_dir = tempfile.mkdtemp(prefix="recursion-unwind-")
    atexit.register(lambda: shutil.rmtree(work_dir, ignore_errors=True))

    src_main = os.path.join(SCRIPT_DIR, "main.cpp")
    src_make = os.path.join(SCRIPT_DIR, "Makefile")

    if not os.path.isfile(src_main):
        die("main.cpp not found next to launch.py")
    if not os.path.isfile(src_make):
        die("Makefile not found next to launch.py")

    shutil.copy(src_main, os.path.join(work_dir, "main.cpp"))
    shutil.copy(src_make, os.path.join(work_dir, "Makefile"))

    return work_dir


def _validate(work_dir):
    _banner("recursion-unwind -- Checking Your Work")
    print()

    _wrap("Building with: make")
    r = subprocess.run(
        ["make"],
        capture_output=True,
        text=True,
        cwd=work_dir,
    )
    if r.returncode != 0:
        print("  FAIL  -- build error")
        for line in r.stderr.strip().splitlines()[-15:]:
            print(f"    {line}")
        print()
        _wrap("Hint: Check for syntax errors. Both functions must compile.")
        return False, None
    print("  PASS")
    print()

    _wrap("Running: ./prog")
    try:
        run = subprocess.run(
            ["./prog"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=work_dir,
        )
    except subprocess.TimeoutExpired:
        print("  FAIL  -- program timed out (infinite recursion?)")
        print()
        _wrap(
            "Hint: If digit_sum never terminates, you are probably missing the "
            "base case. A recursive function MUST have a condition that stops "
            "the recursion without making another recursive call."
        )
        return False, None

    got = run.stdout.rstrip("\n")
    passphrase = _decrypt(got)
    if passphrase is None:
        print("  FAIL  -- output does not match")
        print()
        print(f"  Your output:")
        for line in got.splitlines():
            print(f"    {line}")
        print()
        _wrap(
            "Expected: digit_sum(493) on the first line, "
            "reverse_str(\"hello\", 0, 4) on the second line. "
            "Trace each function carefully."
        )
        return False, None

    print("  PASS")
    return True, passphrase


def main():
    work_dir = _setup_work_dir()

    banner_text = textwrap.dedent("""\

  ============================================================
   recursion-unwind
  ============================================================

   This program has TWO bugs. Both are in recursive functions.

   Bug 1: digit_sum(int n)
     The function computes the sum of digits of n.
     It is missing its base case -- it will recurse forever.

   Bug 2: reverse_str(const string& s, int i, int j)
     The function should reverse string s between indices i and j.
     There is an off-by-one error in the swap statement.

   Fix both bugs so that running the program produces:
     16
     olleh

   To build and run:
     make run

   Type 'exit' when you think both bugs are fixed.
  ============================================================

""")

    rcfile = tempfile.NamedTemporaryFile(mode="w", suffix=".rc", delete=False)
    rcfile.write(
        f"PS1='\\u@recursion-unwind:\\W\\$ '\n"
        f'cd "{work_dir}"\n'
        "cat << 'BANNER'\n" + banner_text + "\nBANNER\n"
    )
    rcfile.close()

    shell = os.environ.get("SHELL", "/bin/bash")

    try:
        while True:
            subprocess.run([shell, "--rcfile", rcfile.name])
            print()
            ok, passphrase = _validate(work_dir)
            if ok:
                _show_passphrase(passphrase)
                break
            print()
            try:
                again = input("  Try again? [y/n] ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if again == "y":
                print()
                continue
            break
    finally:
        try:
            os.remove(rcfile.name)
        except OSError:
            pass


if __name__ == "__main__":
    main()
