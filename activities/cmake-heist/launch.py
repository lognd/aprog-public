#!/usr/bin/env python3
"""
cmake-heist activity launcher.
Student writes CMakeLists.txt from the provided outline.
Validation: cmake configure + build + ctest + app output check.
"""
import os, sys, shutil, subprocess, tempfile, zipfile, textwrap
import hashlib as _hl, hmac as _hm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ZIP   = os.path.join(SCRIPT_DIR, "repo.zip")

_SALT      = bytes.fromhex("a3f1b2c4d5e6f7a8b9c0d1e2f3a4b5c6")
_KDF_ITERS = 100000
_BLOB      = "ad74e885761fe02298626aca318a92e555b857953331698717d138fbe145fa1bb66c4a2587baac712d1a54e3fbe7c424bc7aa76a5ca830668621"
_EXPECTED_APP = (
    "Prime counts\n"
    "--------------------------------\n"
    "  primes up to 10              4\n"
    "  primes up to 50             15\n"
    "  primes up to 100            25\n"
    "  primes up to 500            95\n"
    "  primes up to 1000          168\n"
    "--------------------------------\n"
    "  gcd(48, 18) = 6\n"
    "  digits in 10000 = 5"
)

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

def _validate(repo_dir):
    cmake_lists = os.path.join(repo_dir, "CMakeLists.txt")
    build_dir   = os.path.join(repo_dir, "build")

    _banner("cmake-heist -- Checking Your Work")
    print()

    if not os.path.isfile(cmake_lists):
        _wrap("CMakeLists.txt not found.")
        return False

    # Configure
    _wrap("Stage 1: cmake configure")
    r = subprocess.run(
        ["cmake", "-B", build_dir, "-DCMAKE_BUILD_TYPE=Release"],
        capture_output=True, text=True, cwd=repo_dir,
    )
    if r.returncode != 0:
        print("  FAIL")
        for line in r.stderr.strip().splitlines()[-15:]:
            print(f"    {line}")
        return False
    print("  PASS")
    print()

    # Build
    _wrap("Stage 2: cmake --build")
    r = subprocess.run(
        ["cmake", "--build", build_dir],
        capture_output=True, text=True, cwd=repo_dir,
    )
    if r.returncode != 0:
        print("  FAIL")
        for line in r.stderr.strip().splitlines()[-15:]:
            print(f"    {line}")
        return False
    print("  PASS")
    print()

    # ctest
    _wrap("Stage 3: ctest (both test suites must pass)")
    r = subprocess.run(
        ["ctest", "--test-dir", build_dir, "--output-on-failure"],
        capture_output=True, text=True, cwd=repo_dir,
    )
    if r.returncode != 0:
        print("  FAIL")
        for line in r.stdout.strip().splitlines():
            print(f"    {line}")
        return False
    print("  PASS")
    print()

    # App output
    _wrap("Stage 4: app output")
    app_bin = os.path.join(build_dir, "app")
    if not os.path.isfile(app_bin):
        print("  FAIL  'app' binary not found in build/")
        return False
    try:
        run = subprocess.run(
            [app_bin], capture_output=True, text=True, timeout=10, cwd=repo_dir,
        )
    except subprocess.TimeoutExpired:
        print("  FAIL  app timed out")
        return False
    got = run.stdout.strip()
    if got != _EXPECTED_APP:
        print("  FAIL  output does not match expected")
        print(f"    got:      {got!r}")
        print(f"    expected: {_EXPECTED_APP!r}")
        return False
    print("  PASS")
    return True

def main():
    if not os.path.isfile(REPO_ZIP):
        die("repo.zip not found.")

    work_dir = tempfile.mkdtemp(prefix="cmake-heist-")

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
       cmake-heist
      ============================================================

       You have a multi-module C++ project with no build system.
       Your job: write a CMakeLists.txt from scratch.

       A CMakeLists.txt with guiding comments is already in place.
       Read it carefully, then fill in each section.

       Project structure:
         lib_math/    -- static library target: math
         lib_text/    -- static library target: text (depends on math)
         app/         -- executable target: app
         lib_*/tests/ -- test executables: test_math, test_text

       Naming note: add_library(math STATIC ...) tells CMake to
       name the target "math".  The toolchain then produces the
       file: libmath.a on Linux/macOS, math.lib on Windows.
       You name the target; the "lib" prefix is added for you.

       When you think your CMakeLists.txt is ready, type 'exit'.
       The launcher will configure, build, run the tests, and
       check the app output.

       Useful commands:
         cmake -B build && cmake --build build
         ctest --test-dir build --output-on-failure
         ./build/app
      ============================================================

    """)
    rcfile.write(
        f'PS1=\'\\u@cmake-heist:\\W\\$ \'\n'
        f'cd "{repo_dir}"\n'
        "cat << 'BANNER'\n" + banner_text + "\nBANNER\n"
    )
    rcfile.close()

    shell = os.environ.get("SHELL", "/bin/bash")

    try:
        while True:
            subprocess.run([shell, "--rcfile", rcfile.name])
            print()
            ok = _validate(repo_dir)
            if ok:
                passphrase = _decrypt(_EXPECTED_APP)
                if passphrase:
                    _show_passphrase(passphrase)
                    break
                print("  Internal error: decryption failed.")
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
