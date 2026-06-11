#!/usr/bin/env python3
"""
cpp-standards-hunt activity launcher.
Student identifies the minimum C++ standard that compiles main.cpp,
then sets CMAKE_CXX_STANDARD in CMakeLists.txt to that version.
Validation: cmake configure + build + binary output unlocks the passphrase.
"""

import atexit, os, shutil, subprocess, sys, tempfile, textwrap, zipfile  # noqa: E401, I001
import hashlib as _hl, hmac as _hm  # noqa: E401

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ZIP = os.path.join(SCRIPT_DIR, "repo.zip")

_SALT = bytes.fromhex("a3f1b2c4d5e6f7a8b9c0d1e2f3a4b5c6")
_KDF_ITERS = 100000
_BLOB = "301dc5fbaaace7761c41b453fac181b918b6c5f3390024cd3e93081707925beb1fc209acd579a002e0d149e4a2f760233296285e8f1674904f03"


def _decrypt(key_str):
    key = _hl.pbkdf2_hmac("sha256", key_str.encode(), _SALT, _KDF_ITERS)
    blob = bytes.fromhex(_BLOB)
    ct, mac = blob[:-32], blob[-32:]
    if not _hm.compare_digest(mac, _hm.new(key, ct, _hl.sha256).digest()):
        return None
    _, i, stream = b"", 0, b""
    while len(stream) < len(ct):
        stream += _hl.sha256(key + i.to_bytes(4, "little")).digest()
        i += 1
    return bytes(a ^ b for a, b in zip(ct, stream, strict=False)).decode()


_LINE_WIDTH = 70


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


def _hint_build_failed():
    print()
    _wrap("Hint: the build failed because the standard is set too low.")
    print()
    _wrap(
        "For each failing symbol, search cppreference.com for it "
        "and look for the version marker on the page. cppreference "
        "uses this notation:"
    )
    print()
    print("    (since C++11)")
    print("    (since C++14)")
    print("    (since C++17)")
    print()
    _wrap(
        "That marker tells you the earliest standard that includes "
        "the feature. Find the newest marker across everything that "
        "fails -- that is the minimum CMAKE_CXX_STANDARD you need."
    )


def _hint_version_too_high():
    print()
    _wrap("Hint: the build succeeded, but the output is not correct.")
    _wrap(
        "If you set a standard higher than the minimum required, "
        "the validator will not unlock. Find the lowest standard "
        "version that still compiles the project."
    )


def _validate(repo_dir):
    cmake_lists = os.path.join(repo_dir, "CMakeLists.txt")
    build_dir = os.path.join(repo_dir, "build")

    _banner("cpp-standards-hunt -- Checking Your Work")
    print()

    if not os.path.isfile(cmake_lists):
        _wrap("CMakeLists.txt not found.")
        return False, None

    _wrap("Stage 1: cmake configure")
    r = subprocess.run(
        ["cmake", "-B", build_dir, "-DCMAKE_BUILD_TYPE=Release"],
        capture_output=True,
        text=True,
        cwd=repo_dir,
    )
    if r.returncode != 0:
        print("  FAIL")
        for line in r.stderr.strip().splitlines()[-15:]:
            print(f"    {line}")
        _hint_build_failed()
        return False, None
    print("  PASS")
    print()

    _wrap("Stage 2: cmake --build")
    r = subprocess.run(
        ["cmake", "--build", build_dir],
        capture_output=True,
        text=True,
        cwd=repo_dir,
    )
    if r.returncode != 0:
        print("  FAIL")
        for line in r.stderr.strip().splitlines()[-15:]:
            print(f"    {line}")
        _hint_build_failed()
        return False, None
    print("  PASS")
    print()

    _wrap("Stage 3: run ./build/hunt and check output")
    hunt_bin = os.path.join(build_dir, "hunt")
    if not os.path.isfile(hunt_bin):
        print("  FAIL  'hunt' binary not found in build/")
        return False, None
    try:
        run = subprocess.run(
            [hunt_bin],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except subprocess.TimeoutExpired:
        print("  FAIL  hunt timed out")
        return False, None
    got = run.stdout.strip()
    passphrase = _decrypt(got)
    if passphrase is None:
        print("  FAIL  output does not match")
        _hint_version_too_high()
        return False, None
    print("  PASS")
    return True, passphrase


def main():
    if not os.path.isfile(REPO_ZIP):
        die("repo.zip not found.")

    work_dir = tempfile.mkdtemp(prefix="cpp-standards-hunt-")
    atexit.register(lambda: shutil.rmtree(work_dir, ignore_errors=True))

    with zipfile.ZipFile(REPO_ZIP, "r") as zf:
        zf.extractall(work_dir)

    entries = [
        e for e in os.listdir(work_dir) if os.path.isdir(os.path.join(work_dir, e))
    ]
    if len(entries) != 1:
        die("unexpected zip structure")
    repo_dir = os.path.join(work_dir, entries[0])

    banner_text = textwrap.dedent("""\

      ============================================================
       cpp-standards-hunt
      ============================================================

       This project does not compile. The C++ standard is set too low.

       Identify every modern feature used in main.cpp.
       Look each one up at:
         https://en.cppreference.com/w/cpp/compiler_support

       Find the MINIMUM standard version that compiles the project.
       Edit CMakeLists.txt to set CMAKE_CXX_STANDARD to that version.

       Using a higher standard than necessary will not unlock
       the passphrase.

       A Makefile is provided. To build and run:
         make
         make run

       Type 'exit' when done.
      ============================================================

    """)

    rcfile = tempfile.NamedTemporaryFile(mode="w", suffix=".rc", delete=False)
    rcfile.write(
        f"PS1='\\u@cpp-standards-hunt:\\W\\$ '\n"
        f'cd "{repo_dir}"\n'
        "cat << 'BANNER'\n" + banner_text + "\nBANNER\n"
    )
    rcfile.close()

    shell = os.environ.get("SHELL", "/bin/bash")

    try:
        while True:
            subprocess.run([shell, "--rcfile", rcfile.name])
            print()
            ok, passphrase = _validate(repo_dir)
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
