#!/usr/bin/env python3
"""
Array Foray activity launcher.
Opens a shell for the student to work in, then validates their fix by
compiling and running main.cpp before cleaning up the temp directory.
"""
import os, sys, shutil, subprocess, tempfile, atexit, zipfile, textwrap
import hashlib as _hl, hmac as _hm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ZIP   = os.path.join(SCRIPT_DIR, "repo.zip")

# -- Crypto -------------------------------------------------------------------
# The blob is keyed on the exact output of the correctly-fixed program.
# _decrypt() cannot succeed without first running the binary and extracting
# the key from its stdout.

_SALT      = bytes.fromhex("a3f1b2c4d5e6f7a8b9c0d1e2f3a4b5c6")
_KDF_ITERS = 100000
_BLOB      = "332340fbc6146f3e9a5d4c679a597823f9dae837e90bf82ac8172b912ecbefd84674e41dd30b139fbc8e993b7edd02b8e13a50e1bc"

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

# -- Validation ---------------------------------------------------------------

def _validate(repo_dir):
    """Compile main.cpp, run it, and return the key extracted from stdout."""
    binary = os.path.join(repo_dir, "foray")
    r = subprocess.run(
        ["g++", "-std=c++17", "-o", binary,
         os.path.join(repo_dir, "main.cpp")],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        return False, "compile-error", r.stderr
    try:
        run = subprocess.run([binary], capture_output=True, text=True, timeout=10)
    except subprocess.TimeoutExpired:
        return False, "timeout", ""
    # Extract the stable key: the stripped stdout (address-free, deterministic)
    key_str = run.stdout.strip()
    return True, key_str, run.stdout

# -- Helpers ------------------------------------------------------------------

_LINE_WIDTH = 70

def _banner(title):
    print("=" * _LINE_WIDTH)
    pad = (_LINE_WIDTH - len(title) - 2) // 2
    print(" " * pad + " " + title + " " + " " * pad)
    print("=" * _LINE_WIDTH)

def _hr():
    print("-" * _LINE_WIDTH)

def _show_passphrase(passphrase):
    print()
    _hr()
    print(f"  Passphrase: {passphrase}")
    _hr()
    print()

def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)

# -- Main ---------------------------------------------------------------------

def main():
    if not os.path.isfile(REPO_ZIP):
        die("repo.zip not found.")

    work_dir = tempfile.mkdtemp(prefix="array-foray-")

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
       Array Foray
      ============================================================

       Files: explore.cpp, main.cpp, Makefile

       Step 1 -- run the exploration program and read the output:
         make explore && ./explore

       Step 2 -- try to compile main.cpp:
         make

       Step 3 -- fix the error and compile again:
         make run

       When main.cpp compiles and runs successfully, type 'exit'.
       The launcher will check your work automatically.
      ============================================================

    """)
    rcfile.write(textwrap.dedent(f"""\
        PS1='\\u@array-foray:\\W\\$ '
        cd "{repo_dir}"
        cat << 'BANNER'
{banner_text}BANNER
    """))
    rcfile.close()

    shell = os.environ.get("SHELL", "/bin/bash")

    try:
        while True:
            subprocess.run([shell, "--rcfile", rcfile.name])

            print()
            _banner("Array Foray -- Checking Your Work")
            print()

            ok, key_str, detail = _validate(repo_dir)

            if ok:
                passphrase = _decrypt(key_str)
                if passphrase is not None:
                    _show_passphrase(passphrase)
                    break
                print("  The program compiled and ran, but the output was not correct.")

            elif key_str == "compile-error":
                print("  main.cpp did not compile.  Error:\n")
                for line in detail.strip().splitlines():
                    print(f"    {line}")
            elif key_str == "timeout":
                print("  The program did not finish in time.")

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
        shutil.rmtree(work_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
