#!/usr/bin/env python3
"""
Text Stream Surgery activity launcher.

Drops the student into a shell with three broken C++ programs.
Each program has one file-stream bug.  After the student fixes all three
and types 'exit', the launcher compiles them, runs them, and checks the
combined output against the expected result.
"""
import os, shutil, subprocess, sys, tempfile, zipfile, textwrap
import hashlib as _hl, hmac as _hm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ZIP   = os.path.join(SCRIPT_DIR, "repo.zip")

# -- Crypto -------------------------------------------------------------------
# Blob is keyed on the stripped, |-joined stdout of all three fixed programs.

_SALT      = bytes.fromhex("a3f1b2c4d5e6f7a8b9c0d1e2f3a4b5c6")
_KDF_ITERS = 100000
_BLOB      = "155a9c981ddcd76e5d88f2e69a1feb5266e0062ff49f5f3beebb8620efcf9b43a473a8b43efa56d1485c8f6bff3f56216219e940c9"

def _decrypt(key_str):
    key  = _hl.pbkdf2_hmac("sha256", key_str.encode(), _SALT, _KDF_ITERS)
    blob = bytes.fromhex(_BLOB)
    ct, mac = blob[:-32], blob[-32:]
    if not _hm.compare_digest(mac, _hm.new(key, ct, _hl.sha256).digest()):
        return None
    out, i = b"", 0
    while len(out) < len(ct):
        out += _hl.sha256(key + i.to_bytes(4, "little")).digest()
        i += 1
    return bytes(a ^ b for a, b in zip(ct, out)).decode()

# -- Helpers ------------------------------------------------------------------

_LINE_WIDTH = 70

def _banner(title):
    print("=" * _LINE_WIDTH)
    pad = (_LINE_WIDTH - len(title) - 2) // 2
    print(" " * pad + " " + title + " " * pad)
    print("=" * _LINE_WIDTH)

def _hr():
    print("-" * _LINE_WIDTH)

def _wrap(text, indent="  "):
    for line in textwrap.wrap(text, width=_LINE_WIDTH - 4,
                              initial_indent=indent,
                              subsequent_indent=indent + "  "):
        print(line)

def _show_passphrase(passphrase):
    print()
    _hr()
    print(f"  Passphrase: {passphrase}")
    _hr()
    print()

def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)

# -- Validation ---------------------------------------------------------------

def _compile(src, name, repo_dir):
    r = subprocess.run(
        ["g++", "-std=c++17", "-Wall", "-o", name, src],
        capture_output=True, text=True, cwd=repo_dir,
    )
    return r.returncode == 0, r.stderr

def _run_bin(name, repo_dir):
    path = os.path.join(repo_dir, name)
    if not os.path.isfile(path):
        return None, f"{name} binary not found -- did you compile it?"
    try:
        r = subprocess.run(
            [f"./{name}"], capture_output=True, text=True,
            timeout=10, cwd=repo_dir,
        )
        return r.stdout.strip(), None
    except subprocess.TimeoutExpired:
        return None, f"{name} timed out"

_PROGRAMS = [
    ("eof_loop.cpp",  "eof_loop",  "Sum: 60"),
    ("no_check.cpp",  "no_check",  "error: cannot open missing.txt"),
    ("mixed_io.cpp",  "mixed_io",  "Alice: Likes C++ and file I/O"),
]

def _validate(repo_dir):
    _banner("Checking Your Work")
    print()
    outputs = []
    all_ok = True
    for src, name, expected in _PROGRAMS:
        ok, err = _compile(src, name, repo_dir)
        if not ok:
            print(f"  FAIL  {src} did not compile:")
            for line in err.strip().splitlines():
                print(f"        {line}")
            all_ok = False
            outputs.append(None)
            continue
        out, err = _run_bin(name, repo_dir)
        if err:
            print(f"  FAIL  {name}: {err}")
            all_ok = False
            outputs.append(None)
            continue
        if out == expected:
            print(f"  PASS  {name}: {out}")
            outputs.append(out)
        else:
            print(f"  FAIL  {name}")
            print(f"        got:      {out!r}")
            print(f"        expected: {expected!r}")
            all_ok = False
            outputs.append(out)
    print()
    return all_ok, "|".join(o for o in outputs if o is not None)

# -- Main ---------------------------------------------------------------------

BANNER_TEXT = """\

  ============================================================
   Text Stream Surgery
  ============================================================

   Three C++ programs.  Each has one file-stream bug.
   Fix all three, then type 'exit'.

   Step 1 -- fix eof_loop.cpp
     The program sums integers from numbers.txt.
     Expected:  Sum: 60
     Actual:    Sum: 90

     Hint: what does eof() return before vs. after a failed read?

   Step 2 -- fix no_check.cpp
     The program counts lines in missing.txt (which does not exist).
     Expected:  error: cannot open missing.txt
     Actual:    Lines: 0

     Hint: how do you know if ifstream actually opened the file?

   Step 3 -- fix mixed_io.cpp
     The program reads a name and bio from profile.txt.
     Expected:  Alice: Likes C++ and file I/O
     Actual:    Alice: (bio is always empty)

     Hint: what does operator>> leave in the stream buffer?

   Compile commands:
     g++ -std=c++17 -o eof_loop eof_loop.cpp
     g++ -std=c++17 -o no_check no_check.cpp
     g++ -std=c++17 -o mixed_io mixed_io.cpp

   Or: make

   Type 'exit' when all three print the expected output.
  ============================================================

"""

def main():
    if not os.path.isfile(REPO_ZIP):
        die("repo.zip not found.")

    work_dir = tempfile.mkdtemp(prefix="text-stream-surgery-")
    import atexit
    atexit.register(lambda: shutil.rmtree(work_dir, ignore_errors=True))

    with zipfile.ZipFile(REPO_ZIP, "r") as zf:
        zf.extractall(work_dir)

    entries = [e for e in os.listdir(work_dir)
               if os.path.isdir(os.path.join(work_dir, e))]
    if len(entries) != 1:
        die("unexpected zip structure")
    repo_dir = os.path.join(work_dir, entries[0])

    rcfile = tempfile.NamedTemporaryFile(mode="w", suffix=".rc", delete=False)
    atexit.register(lambda: os.unlink(rcfile.name))
    rcfile.write(
        "PS1='\\u@text-stream-surgery:\\W\\$ '\n"
        f'cd "{repo_dir}"\n'
        "cat << 'BANNER'\n" + BANNER_TEXT + "BANNER\n"
    )
    rcfile.close()

    shell = os.environ.get("SHELL", "/bin/bash")

    _banner("Text Stream Surgery")
    print()
    _wrap("Three C++ programs.  Each has one file-stream bug.  Fix all three "
          "and the passphrase unlocks.")
    print()

    while True:
        subprocess.run([shell, "--rcfile", rcfile.name])
        print()
        all_ok, combined = _validate(repo_dir)
        if all_ok:
            passphrase = _decrypt(combined)
            if passphrase:
                _show_passphrase(passphrase)
            else:
                print("  [internal error] Decryption failed -- contact your instructor.")
            break
        try:
            again = input("  Try again? [y/n] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if again != "y":
            break
        print()


if __name__ == "__main__":
    main()
