#!/usr/bin/env python3
"""
Vector Inspector & Corrector activity launcher.
Opens a shell for the student to work in, then validates their fix by
compiling and running main.cpp before cleaning up the temp directory.
"""
import os, sys, shutil, subprocess, tempfile, zipfile, textwrap
import hashlib as _hl, hmac as _hm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ZIP   = os.path.join(SCRIPT_DIR, "repo.zip")

# -- Crypto -------------------------------------------------------------------
# The blob is keyed on the "Moves: X" line from the program's stdout.
# _decrypt() cannot succeed without first running the binary and extracting
# that line -- calling it directly with a guessed key will fail the HMAC.

_SALT      = bytes.fromhex("a3f1b2c4d5e6f7a8b9c0d1e2f3a4b5c6")
_KDF_ITERS = 100000
_BLOB      = "ce7eef0d21aa3950907612091fb664b848acd35f1b35695dd3dd8d5eb97a809b9c964f697afb418dd11d82d8f781bbb6ac5fa0ddc22451"

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
    """Compile main.cpp, run it, and extract the 'Moves: X' line as the key."""
    binary = os.path.join(repo_dir, "inspector")
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
    # Extract the "Moves: X" line as the decryption key
    key_str = next(
        (line.strip() for line in run.stdout.splitlines() if line.strip().startswith("Moves:")),
        None,
    )
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

    work_dir = tempfile.mkdtemp(prefix="vector-inspector-corrector-")

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
       Vector Inspector & Corrector
      ============================================================

       Files: main.cpp, Makefile

       Step 1 -- compile and run to see what is happening:
         make && ./inspector

         Look at the data-address column.  Pay attention to
         when and why it changes.

       Step 2 -- find and fix the problem with reserve(), then
       run again:
         make && ./inspector

       When the buffer never moves, type 'exit'.
       The launcher will check your work automatically.
      ============================================================

    """)
    rcfile.write(textwrap.dedent(f"""\
        PS1='\\u@vector-inspector:\\W\\$ '
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
            _banner("Vector Inspector & Corrector -- Checking Your Work")
            print()

            ok, key_str, detail = _validate(repo_dir)

            if ok:
                passphrase = _decrypt(key_str) if key_str else None
                if passphrase is not None:
                    _show_passphrase(passphrase)
                    break
                print("  The buffer still moves.  Check the output and try again.")

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
