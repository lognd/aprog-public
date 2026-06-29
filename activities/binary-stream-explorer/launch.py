#!/usr/bin/env python3
"""
Binary Stream Explorer activity launcher.

Shows a hex dump of a custom binary file, then drops the student into a
shell with reader.cpp -- a program with three blanks (BLANK_A, BLANK_B,
BLANK_C).  The student fills in the blanks, compiles, and runs the program.
When the output matches the expected values, the passphrase is revealed.
"""
import os, shutil, struct, subprocess, sys, tempfile, zipfile, textwrap
import hashlib as _hl, hmac as _hm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ZIP   = os.path.join(SCRIPT_DIR, "repo.zip")

# -- Crypto -------------------------------------------------------------------
# Blob is keyed on the stripped stdout of the correctly completed reader.

_SALT      = bytes.fromhex("a3f1b2c4d5e6f7a8b9c0d1e2f3a4b5c6")
_KDF_ITERS = 100000
_BLOB      = "211e894a79e0f1205c4d52c6a75b25a68b7534fd331ab86bfd7190c14c6bad858598e2745ec84474782ee4f3bc2193d3a62bff24"

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
_EXPECTED   = "Records: 3\nID: 2\nScore: 80\nName: Bob"

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

def _hex_dump(data):
    lines = []
    for i in range(0, len(data), 16):
        row = data[i:i+16]
        hex_part = " ".join(f"{b:02x}" for b in row)
        asc_part = "".join(chr(b) if 32 <= b < 127 else "." for b in row)
        lines.append(f"  {i:04x}  {hex_part:<47}  {asc_part}")
    return "\n".join(lines)

# -- Validation ---------------------------------------------------------------

def _validate(repo_dir, data_path):
    binary = os.path.join(repo_dir, "reader")
    src    = os.path.join(repo_dir, "reader.cpp")

    r = subprocess.run(
        ["g++", "-std=c++17", "-Wall", "-o", "reader", "reader.cpp"],
        capture_output=True, text=True, cwd=repo_dir,
    )
    if r.returncode != 0:
        print("  FAIL  reader.cpp did not compile:")
        for line in r.stderr.strip().splitlines():
            print(f"        {line}")
        return False, None

    try:
        r = subprocess.run(
            ["./reader"], capture_output=True, text=True,
            timeout=10, cwd=repo_dir,
        )
        out = r.stdout.strip()
    except subprocess.TimeoutExpired:
        print("  FAIL  reader timed out")
        return False, None

    if out == _EXPECTED:
        print("  PASS  Output matches expected:")
        for line in out.splitlines():
            print(f"        {line}")
        return True, out
    else:
        print("  FAIL  Output does not match.")
        print("        Got:")
        for line in (out or "(no output)").splitlines():
            print(f"          {line}")
        print("        Expected:")
        for line in _EXPECTED.splitlines():
            print(f"          {line}")
        return False, out

# -- Main ---------------------------------------------------------------------

def main():
    if not os.path.isfile(REPO_ZIP):
        die("repo.zip not found.")

    work_dir = tempfile.mkdtemp(prefix="binary-stream-explorer-")
    import atexit
    atexit.register(lambda: shutil.rmtree(work_dir, ignore_errors=True))

    with zipfile.ZipFile(REPO_ZIP, "r") as zf:
        zf.extractall(work_dir)

    entries = [e for e in os.listdir(work_dir)
               if os.path.isdir(os.path.join(work_dir, e))]
    if len(entries) != 1:
        die("unexpected zip structure")
    repo_dir  = os.path.join(work_dir, entries[0])
    data_path = os.path.join(repo_dir, "data.bin")

    # Read the binary file for the hex dump display.
    with open(data_path, "rb") as f:
        raw = f.read()

    hex_dump = _hex_dump(raw)

    banner_body = f"""
  ============================================================
   Binary Stream Explorer
  ============================================================

   A custom binary file format called APROG is shown below.
   Your job is to fill in three blanks in reader.cpp so that
   it reads the file correctly and prints the expected output.

   File format (little-endian, no padding between fields):
     [0..3]   "APRO"    magic bytes (4 bytes)
     [4..5]   count     uint16_t -- number of records (2 bytes)
     [6..]    records   each record is sizeof(Record) bytes:
                          id    int32_t  (4 bytes)
                          score int32_t  (4 bytes)
                          name  char[8]  (8 bytes, null-padded)

   Hex dump of data.bin ({len(raw)} bytes):
{hex_dump}

   The three blanks in reader.cpp:
     BLANK_A -- byte count for f.read() of count (uint16_t)
     BLANK_B -- seekg() offset of the record at index 1
     BLANK_C -- byte count for f.read() of one Record

   Expected output:
     Records: 3
     ID: 2
     Score: 80
     Name: Bob

   To compile and run:
     g++ -std=c++17 -o reader reader.cpp && ./reader

   Type 'exit' when the output matches.
  ============================================================

"""

    rcfile = tempfile.NamedTemporaryFile(mode="w", suffix=".rc", delete=False)
    atexit.register(lambda: os.unlink(rcfile.name))
    rcfile.write(
        "PS1='\\u@binary-stream-explorer:\\W\\$ '\n"
        f'cd "{repo_dir}"\n'
        "cat << 'BANNER'\n" + banner_body + "BANNER\n"
    )
    rcfile.close()

    shell = os.environ.get("SHELL", "/bin/bash")

    _banner("Binary Stream Explorer")
    print()
    _wrap("Fill in three blanks in reader.cpp using the hex dump and "
          "sizeof() to compute offsets.  Compile and run the program "
          "inside the shell until it prints the expected output.")
    print()

    while True:
        subprocess.run([shell, "--rcfile", rcfile.name])
        print()
        _banner("Checking Your Work")
        print()
        ok, out = _validate(repo_dir, data_path)
        if ok:
            passphrase = _decrypt(out)
            if passphrase:
                _show_passphrase(passphrase)
            else:
                print("  [internal error] Decryption failed -- contact your instructor.")
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
