#!/usr/bin/env python3
"""
stale-build activity launcher.

Drops the student into a shell with the broken repo, then validates:
  Stage 1 -- clean build produces the expected output.
  Stage 2 -- stale scenario: the validator compiles .o files with a
             temporarily modified limits.h (SIEVE_LIMIT=50), restores the
             real limits.h, then runs make without cleaning.  A Makefile that
             lists limits.h as a prerequisite detects the change and rebuilds;
             one that does not will silently produce the wrong answer.
"""
import os, sys, shutil, subprocess, tempfile, textwrap, time, zipfile
import hashlib as _hl, hmac as _hm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ZIP   = os.path.join(SCRIPT_DIR, "repo.zip")

# -- Crypto -------------------------------------------------------------------

_SALT      = bytes.fromhex("a3f1b2c4d5e6f7a8b9c0d1e2f3a4b5c6")
_KDF_ITERS = 100000
_BLOB      = "4b70b506eec5e930efa4420fac314ee387e24d07a4c1344cf4b306d8d7c13e37c149e72b1ec05713141b6c3e46fa300ce8ff"
_EXPECTED  = "Primes up to 10000: 1229"

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

def _wrap(text):
    for line in textwrap.wrap(text, width=_LINE_WIDTH - 4,
                              initial_indent="  ",
                              subsequent_indent="    "):
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

def _run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          text=True)

def _run_binary(path):
    try:
        r = subprocess.run([path], capture_output=True, text=True, timeout=10)
        return r.stdout.strip(), None
    except subprocess.TimeoutExpired:
        return None, "binary timed out"

_REAL_LIMITS = (
    "#ifndef LIMITS_H\n#define LIMITS_H\n\n"
    "static const int SIEVE_LIMIT = 10000;\n\n#endif\n"
)

def _stage1_clean_build(repo_dir):
    with open(os.path.join(repo_dir, "limits.h"), "w") as f:
        f.write(_REAL_LIMITS)
    _run(["make", "clean"], cwd=repo_dir)
    r = _run(["make"], cwd=repo_dir)
    if r.returncode != 0:
        return None, "make failed:\n" + r.stderr
    binary = os.path.join(repo_dir, "count_primes")
    if not os.path.isfile(binary):
        return None, "count_primes not found after make"
    return _run_binary(binary)

def _stage1b_nothing_to_do(repo_dir):
    """After a clean build, make should report nothing to do."""
    r = _run(["make"], cwd=repo_dir)
    combined = (r.stdout + r.stderr).lower()
    if "nothing to be done" in combined or "is up to date" in combined:
        return True, None
    return False, (
        "make rebuilt targets after a fresh build -- are all file-producing "
        "targets (count_primes, sieve.o, main.o) absent from .PHONY?"
    )

def _stage2_stale_scenario(repo_dir):
    """
    Manufactures a genuine stale state, independent of what the student did:
      1. Write a temporary limits.h with SIEVE_LIMIT=50.
      2. Compile fresh sieve.o and main.o against it (they now encode 50).
      3. Restore the real limits.h (SIEVE_LIMIT=10000).
      4. Set .o timestamps to T and limits.h to T+2 so limits.h appears newer.
      5. Remove the binary so the link step always runs.
      6. Run make (no clean).
         - Fixed Makefile:  detects limits.h changed, rebuilds -> 1229
         - Buggy Makefile:  ignores limits.h, reuses stale .o -> wrong output
    """
    limits_h = os.path.join(repo_dir, "limits.h")
    sieve_o  = os.path.join(repo_dir, "sieve.o")
    main_o   = os.path.join(repo_dir, "main.o")
    binary   = os.path.join(repo_dir, "count_primes")

    stale_limits = (
        "#ifndef LIMITS_H\n#define LIMITS_H\n\n"
        "static const int SIEVE_LIMIT = 50;\n\n#endif\n"
    )
    with open(limits_h, "w") as f:
        f.write(stale_limits)

    r = _run(["g++", "-std=c++17", "-O0", "-c", "sieve.cpp", "-o", "sieve.o"], cwd=repo_dir)
    if r.returncode != 0:
        return None, "internal: could not compile stale sieve.o"
    r = _run(["g++", "-std=c++17", "-O0", "-c", "main.cpp", "-o", "main.o"], cwd=repo_dir)
    if r.returncode != 0:
        return None, "internal: could not compile stale main.o"

    with open(limits_h, "w") as f:
        f.write(_REAL_LIMITS)

    t = time.time()
    os.utime(sieve_o,  (t, t))
    os.utime(main_o,   (t, t))
    os.utime(limits_h, (t + 2, t + 2))

    if os.path.isfile(binary):
        os.remove(binary)

    r = _run(["make"], cwd=repo_dir)
    if r.returncode != 0:
        return None, "make failed during stale test:\n" + r.stderr
    if not os.path.isfile(binary):
        return None, "count_primes not found after incremental make"

    return _run_binary(binary)

def _validate(repo_dir):
    _banner("Checking Your Work")
    print()

    _wrap("Stage 1: clean build")
    out, err = _stage1_clean_build(repo_dir)
    if err:
        print(f"  FAIL  {err}")
        return False
    if out != _EXPECTED:
        print(f"  FAIL  got:      {out!r}")
        print(f"        expected: {_EXPECTED!r}")
        return False
    print(f"  PASS  {out}")
    print()

    _wrap("Stage 1b: nothing rebuilt when already up to date")
    ok, err = _stage1b_nothing_to_do(repo_dir)
    if not ok:
        print(f"  FAIL  {err}")
        return False
    print(f"  PASS  make reports nothing to do")
    print()

    _wrap("Stage 2: stale scenario (limits.h changed, no make clean)")
    out, err = _stage2_stale_scenario(repo_dir)
    if err:
        print(f"  FAIL  {err}")
        return False
    if out != _EXPECTED:
        print(f"  FAIL  got:      {out!r}")
        print(f"        expected: {_EXPECTED!r}")
        _wrap("The Makefile did not detect that limits.h changed. Make sure "
              "every .o rule that includes limits.h lists it as a prerequisite.")
        return False
    print(f"  PASS  {out}")
    return True

# -- Main ---------------------------------------------------------------------

def main():
    if not os.path.isfile(REPO_ZIP):
        die("repo.zip not found.")

    work_dir = tempfile.mkdtemp(prefix="stale-build-")
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
    banner_text = (
        "\n"
        "  ============================================================\n"
        "   stale-build\n"
        "  ============================================================\n"
        "\n"
        "   You have inherited a prime-counting utility.\n"
        "   Your colleague just left for vacation. Before they left,\n"
        "   they mentioned that editing limits.h and running make\n"
        "   locally (no clean) does nothing -- the binary ignores the\n"
        "   change. CI always passes because it runs make clean first.\n"
        "\n"
        "   Files in this repo:\n"
        "     limits.h    -- defines SIEVE_LIMIT (compile-time constant)\n"
        "     sieve.cpp   -- counts primes up to SIEVE_LIMIT\n"
        "     main.cpp    -- calls prime_count(), prints the result\n"
        "     Makefile    -- builds count_primes\n"
        "\n"
        "   Expected outputs for various SIEVE_LIMIT values:\n"
        "     10    ->  Primes up to 10: 4\n"
        "     50    ->  Primes up to 50: 15\n"
        "     100   ->  Primes up to 100: 25\n"
        "     500   ->  Primes up to 500: 95\n"
        "     10000 ->  Primes up to 10000: 1229\n"
        "\n"
        "   Investigate. Edit limits.h, run make, see what happens.\n"
        "   Fix the Makefile so that editing any source file causes\n"
        "   make to rebuild what depends on it.\n"
        "\n"
        "   Type 'exit' when you think you have fixed it.\n"
        "  ============================================================\n"
    )
    rcfile.write(
        f'PS1=\'\\u@stale-build:\\W\\$ \'\n'
        f'cd "{repo_dir}"\n'
        "cat << 'BANNER'\n" + banner_text + "BANNER\n"
    )
    rcfile.close()

    shell = os.environ.get("SHELL", "/bin/bash")

    while True:
        subprocess.run([shell, "--rcfile", rcfile.name])
        print()
        ok = _validate(repo_dir)
        if ok:
            passphrase = _decrypt(_EXPECTED)
            if passphrase:
                _show_passphrase(passphrase)
            else:
                print("  Internal error: decryption failed.")
            break
        print()
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
