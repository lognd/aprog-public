#!/usr/bin/env python3
"""
project-layout activity launcher.
Student reads a locked CMakeLists.txt to discover the required directory
structure, then organizes the flat source files accordingly.
Validation: cmake configure + build + gradeapp output check.
"""

import atexit, os, shutil, subprocess, sys, tempfile, textwrap, zipfile  # noqa: E401, I001
import hashlib as _hl, hmac as _hm  # noqa: E401

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ZIP = os.path.join(SCRIPT_DIR, "repo.zip")

_SALT = bytes.fromhex("a3f1b2c4d5e6f7a8b9c0d1e2f3a4b5c6")
_KDF_ITERS = 100000
_BLOB = "319589144664382bcc010651dcaa9378ca878927ce3249a318e7329ac1d62d4577a1db7b5a6542e22523801903cd180ae5c672a4d7"
_EXPECTED = "Average: 80\nGrade: B"


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


def _validate(repo_dir):
    cmake_lists = os.path.join(repo_dir, "CMakeLists.txt")
    build_dir = os.path.join(repo_dir, "build")

    _banner("project-layout -- Checking Your Work")
    print()

    if not os.path.isfile(cmake_lists):
        _wrap("CMakeLists.txt not found.")
        return False

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
        _wrap(
            "Hint: check that each source file is in the directory "
            "the CMakeLists.txt expects."
        )
        return False
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
        return False
    print("  PASS")
    print()

    _wrap("Stage 3: run ./build/gradeapp and check output")
    app_bin = os.path.join(build_dir, "gradeapp")
    if not os.path.isfile(app_bin):
        print("  FAIL  'gradeapp' binary not found in build/")
        return False
    try:
        run = subprocess.run(
            [app_bin],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except subprocess.TimeoutExpired:
        print("  FAIL  gradeapp timed out")
        return False
    got = run.stdout.strip()
    if got != _EXPECTED:
        print("  FAIL  output does not match expected")
        print(f"    got:      {got!r}")
        print(f"    expected: {_EXPECTED!r}")
        return False
    print("  PASS")
    return True


def main():
    if not os.path.isfile(REPO_ZIP):
        die("repo.zip not found.")

    work_dir = tempfile.mkdtemp(prefix="project-layout-")
    atexit.register(lambda: shutil.rmtree(work_dir, ignore_errors=True))

    # The zip is flat -- extract directly into work_dir (no subdirectory).
    with zipfile.ZipFile(REPO_ZIP, "r") as zf:
        zf.extractall(work_dir)

    repo_dir = work_dir

    banner_text = textwrap.dedent("""\

      ============================================================
       project-layout
      ============================================================

       The source files are all here, but nothing compiles.

       Read CMakeLists.txt carefully. It describes the exact
       directory structure this project expects.

       Create the necessary directories and move each file to
       its correct location.

       Do NOT modify CMakeLists.txt.

       Then build:
         make
         make run

       Type 'exit' when done.
      ============================================================

    """)

    rcfile = tempfile.NamedTemporaryFile(mode="w", suffix=".rc", delete=False)
    rcfile.write(
        f"PS1='\\u@project-layout:\\W\\$ '\n"
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
                passphrase = _decrypt(_EXPECTED)
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
