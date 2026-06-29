#!/usr/bin/env python3
"""Activity: Write Your First Syscalls

Shell-drop: students fill in three open/read/close blanks in a partial
C++ program, compile it, and verify it prints a file's contents.  The
launcher verifies the compiled binary automatically when the shell exits.
"""
import atexit
import os
import shutil
import subprocess
import tempfile
import textwrap as _tw
import zipfile

# -- Passphrase (split-key XOR; not a cryptographic secret) --
_PP_A = "d721c0cacd9f74411a95f6076c1835681ae33af577"
_PP_B = "a544a1aee0e806286ef0db640077460d3787559b12"

def _passphrase():
    a = bytes.fromhex(_PP_A)
    b = bytes.fromhex(_PP_B)
    return bytes(x ^ y for x, y in zip(a, b, strict=False)).decode()

# -- Display helpers --
_LINE_WIDTH = 70

def _banner(title):
    print("=" * _LINE_WIDTH)
    pad = max(0, (_LINE_WIDTH - len(title) - 2) // 2)
    print(" " * pad + " " + title + " " + " " * pad)
    print("=" * _LINE_WIDTH)

def _hr():
    print("-" * _LINE_WIDTH)

def _wrap(text):
    return _tw.wrap(text, width=_LINE_WIDTH - 4,
                    initial_indent="  ", subsequent_indent="  ")

def _show_passphrase(passphrase):
    print()
    _hr()
    print(f"  Passphrase: {passphrase}")
    _hr()
    print()

# -- Verification --
_SAMPLE_CONTENT = (
    "Every file is a named, persistent sequence of bytes.\n"
    "When you call open(), the kernel gives you an integer called a file descriptor.\n"
    "When you call read(), bytes flow from the kernel into your buffer.\n"
    "When you call write() with fd 1, bytes flow from your buffer to the terminal.\n"
    "When you call close(), the kernel frees the descriptor slot.\n"
    "The three rules: check return values, loop on partial transfers, close every fd.\n"
)

def _verify(work_dir):
    binary = os.path.join(work_dir, "io_tour")
    sample = os.path.join(work_dir, "sample.txt")
    if not os.path.exists(binary):
        print("  [fail] io_tour binary not found.  Did you run 'make'?")
        return False
    result = subprocess.run(
        [binary, sample],
        capture_output=True, text=True, timeout=10,
    )
    if result.returncode != 0:
        print(f"  [fail] io_tour exited with code {result.returncode}.")
        if result.stderr:
            print(f"         stderr: {result.stderr.strip()}")
        return False
    if result.stdout != _SAMPLE_CONTENT:
        print("  [fail] Output does not match sample.txt.")
        print("         Expected first line:")
        print(f"           {_SAMPLE_CONTENT.splitlines()[0]!r}")
        print("         Got first line:")
        got = result.stdout.splitlines()
        print(f"           {got[0]!r}" if got else "           (empty)")
        return False
    return True


def main():
    _banner("Activity: Write Your First Syscalls")
    print()
    print("  You will fill in three blanks in a partial C++ program:")
    print()
    print("    FILL IN 1 -- open() to get an fd")
    print("    FILL IN 2 -- read() inside a loop")
    print("    FILL IN 3 -- close() when done")
    print()
    print("  The program should print the contents of a file to the terminal.")
    print("  Use only: open(), read(), write(), close(), perror().")
    print("  No printf, no cout, no fopen.")
    print()
    print("  Workflow:")
    print("    1. Edit io_tour.cpp -- fill in the three marked sections.")
    print("    2. Run 'make' to compile.")
    print("    3. Run './io_tour sample.txt' to test your output.")
    print("    4. Type 'exit' when the output matches sample.txt exactly.")
    print()
    input("  Press Enter to open the shell...")

    # Set up working directory
    work_dir = tempfile.mkdtemp(prefix="write-your-first-syscalls-")
    atexit.register(lambda: shutil.rmtree(work_dir, ignore_errors=True))

    zip_path = os.path.join(os.path.dirname(__file__), "repo.zip")
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(work_dir)

    shell = os.environ.get("SHELL", "/bin/bash")
    rcfile = tempfile.NamedTemporaryFile(mode="w", suffix=".rc", delete=False)
    atexit.register(lambda: os.unlink(rcfile.name))
    rcfile.write('PS1="[io-tour] \\w $ "\n')
    rcfile.write(f'cd "{work_dir}"\n')
    rcfile.write('echo ""\n')
    rcfile.write('echo "  Files: io_tour.cpp  Makefile  sample.txt"\n')
    rcfile.write('echo "  Edit io_tour.cpp, then: make && ./io_tour sample.txt"\n')
    rcfile.write('echo "  Type exit when your output matches sample.txt."\n')
    rcfile.write('echo ""\n')
    rcfile.close()

    while True:
        subprocess.run([shell, "--rcfile", rcfile.name])
        print()
        print("  Checking your work...")
        print()
        try:
            if _verify(work_dir):
                print("  All checks passed.")
                _show_passphrase(_passphrase())
                break
            else:
                print()
                print("  Re-entering the shell.  Fix the issues above, then type 'exit'.")
                print()
                input("  Press Enter to continue...")
        except subprocess.TimeoutExpired:
            print("  [fail] io_tour timed out (10 s).  Check for an infinite loop.")


if __name__ == "__main__":
    main()
