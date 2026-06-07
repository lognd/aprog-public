#!/usr/bin/env python3
"""
Control Gauntlet activity launcher.
Three programs, three bugs.  Student fixes all three, then exits.
Validation: compile and run each program; combine outputs as the decryption key.
"""
import os, sys, shutil, subprocess, tempfile, zipfile, textwrap
import hashlib as _hl, hmac as _hm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ZIP   = os.path.join(SCRIPT_DIR, "repo.zip")

_SALT      = bytes.fromhex("a3f1b2c4d5e6f7a8b9c0d1e2f3a4b5c6")
_KDF_ITERS = 100000
_BLOB      = "d4629944a9eb8b0f095a47442b9ce2597d62b6be05bb230073f4ee82cd81eb8648175e83bb8aee679c902ce5fb677fd6f0f47ff781229add"

_PROGRAMS = [
    ("search.cpp",  "search",  "First prime in [100..200]: 101"),
    ("filter.cpp",  "filter",  "Sum coprime to 10 in [1..100]: 2000"),
    ("leap.cpp",    "leap",    "Leap years in [1900..2000]: 25\n2000 is a leap year\n1900 is not a leap year\n1996 is a leap year"),
]

def _decrypt(key_str):
    key  = _hl.pbkdf2_hmac("sha256", key_str.encode(), _SALT, _KDF_ITERS)
    blob = bytes.fromhex(_BLOB)
    ct, mac = blob[:-32], blob[-32:]
    if not _hm.compare_digest(mac, _hm.new(key, ct, _hl.sha256).digest()):
        return None
    ks, i, stream = b"", 0, b""
    while len(stream) < len(ct):
        stream += _hl.sha256(key + i.to_bytes(4, "little")).digest()
        i += 1
    return bytes(a ^ b for a, b in zip(ct, stream)).decode()

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

def _show_passphrase(p):
    print()
    _hr()
    print(f"  Passphrase: {p}")
    _hr()
    print()

def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)

def _all_binaries_exist(repo_dir):
    return all(
        os.path.isfile(os.path.join(repo_dir, name))
        for _, name, _ in _PROGRAMS
    )

def _compile_run(src, name, repo_dir):
    binary = os.path.join(repo_dir, name)
    r = subprocess.run(
        ["g++", "-std=c++17", "-Wall", "-o", binary,
         os.path.join(repo_dir, src)],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        return None, r.stderr
    try:
        run = subprocess.run([binary], capture_output=True, text=True, timeout=10)
    except subprocess.TimeoutExpired:
        return None, "timeout"
    return run.stdout.strip(), None

def _validate(repo_dir):
    _banner("Control Gauntlet -- Checking Your Work")
    print()
    outputs = []
    all_ok = True
    for src, name, expected in _PROGRAMS:
        out, err = _compile_run(src, name, repo_dir)
        if err:
            if err == "timeout":
                print(f"  FAIL  {src}: timed out")
            else:
                print(f"  FAIL  {src}: compile error")
                for line in err.strip().splitlines():
                    print(f"        {line}")
            all_ok = False
            continue
        if out == expected:
            print(f"  PASS  {src}")
        else:
            print(f"  FAIL  {src}")
            print(f"        got:      {out!r}")
            print(f"        expected: {expected!r}")
            all_ok = False
        outputs.append(out)
    print()
    if not all_ok:
        return False, None
    key = "|".join(outputs)
    return True, key

def main():
    if not os.path.isfile(REPO_ZIP):
        die("repo.zip not found.")

    work_dir = tempfile.mkdtemp(prefix="control-gauntlet-")

    def cleanup():
        shutil.rmtree(work_dir, ignore_errors=True)

    import atexit
    atexit.register(cleanup)

    with zipfile.ZipFile(REPO_ZIP, "r") as zf:
        zf.extractall(work_dir)

    entries = [e for e in os.listdir(work_dir)
               if os.path.isdir(os.path.join(work_dir, e))]
    if len(entries) != 1:
        die("unexpected zip structure")
    repo_dir = os.path.join(work_dir, entries[0])

    rcfile = tempfile.NamedTemporaryFile(mode="w", suffix=".rc", delete=False)
    banner_text = textwrap.dedent(f"""\

      ============================================================
       Control Gauntlet
      ============================================================

       Four programs.  One is a demo -- compile and run it to
       observe short-circuit evaluation in action.  The other
       three have bugs.  Fix all three to earn the passphrase.

         short_circuit.cpp  -- exploration demo (nothing to fix)
         search.cpp         -- one bug
         filter.cpp         -- one bug
         leap.cpp           -- one bug

       Build any program with:
         g++ -std=c++17 -Wall -o <name> <name>.cpp && ./<name>

       Type 'exit' when you think all three are fixed.
      ============================================================

    """)
    rcfile.write(
        f'PS1=\'\\u@control-gauntlet:\\W\\$ \'\n'
        f'cd "{repo_dir}"\n'
        "cat << 'BANNER'\n" + banner_text + "\nBANNER\n"
    )
    rcfile.close()

    shell = os.environ.get("SHELL", "/bin/bash")

    try:
        while True:
            subprocess.run([shell, "--rcfile", rcfile.name])
            print()
            ok, key = _validate(repo_dir)
            if ok:
                passphrase = _decrypt(key)
                if passphrase:
                    _show_passphrase(passphrase)
                    break
                print("  All programs ran but combined output did not match.")
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
