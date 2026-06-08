#!/usr/bin/env python3
"""Activity: Install C/C++ Compilers

Verifies that gcc, g++, clang, and clang++ are installed and working,
then reveals the passphrase.
"""
import sys, subprocess, tempfile, os, platform, textwrap as _tw
import hashlib as _hl, hmac as _hm

_SALT      = bytes.fromhex("a3f1b2c4d5e6f7a8b9c0d1e2f3a4b5c6")
_KDF_ITERS = 100000
# Encrypted with answers=["gcc-verified", "gxx-verified"]
# Re-generate via aprog-private/activities/env-setup-shell/gen_blobs.py
_BLOB = "6023586f176d62b4e33626d720b2a1d59c02e6595cfd47faaf5fa1ef9a240a5d3bc134f4a11076659fa473b079cfe50caeb9"

_LINE_WIDTH = 70

def _banner(title):
    print("=" * _LINE_WIDTH)
    pad = (_LINE_WIDTH - len(title) - 2) // 2
    print(" " * pad + " " + title + " " + " " * pad)
    print("=" * _LINE_WIDTH)

def _hr():
    print("-" * _LINE_WIDTH)

def _wrap(text):
    for line in _tw.wrap(text, width=_LINE_WIDTH - 4,
                         initial_indent="  ",
                         subsequent_indent="    "):
        print(line)

def _show_passphrase(p):
    print()
    _hr()
    print(f"  Passphrase: {p}")
    _hr()
    print()

def _derive_key(answers):
    return _hl.pbkdf2_hmac("sha256", "|".join(answers).encode(), _SALT, _KDF_ITERS)

def _stream(key, length):
    ks, i = b"", 0
    while len(ks) < length:
        ks += _hl.sha256(key + i.to_bytes(4, "little")).digest()
        i += 1
    return ks[:length]

def _decrypt(blob_hex, answers):
    blob    = bytes.fromhex(blob_hex)
    key     = _derive_key(answers)
    ct, mac = blob[:-32], blob[-32:]
    if not _hm.compare_digest(mac, _hm.new(key, ct, _hl.sha256).digest()):
        return None
    return bytes(a ^ b for a, b in zip(ct, _stream(key, len(ct)))).decode()

def _run(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        out = (r.stdout + r.stderr).strip().splitlines()
        return r.returncode == 0, (out[0] if out else "")
    except FileNotFoundError:
        return False, "not found"
    except Exception as e:
        return False, str(e)

def _compile_test(compiler, src):
    """Compile a small C++ snippet; return (ok, error_message)."""
    with tempfile.NamedTemporaryFile(suffix=".cpp", mode="w", delete=False) as f:
        f.write(src)
        src_path = f.name
    out_path = src_path.replace(".cpp", "")
    ok, msg = _run([compiler, src_path, "-o", out_path, "-std=c++17"])
    try:
        os.unlink(src_path)
        if os.path.exists(out_path):
            os.unlink(out_path)
    except OSError:
        pass
    return ok, msg

_HELLO = '#include <iostream>\nint main(){std::cout<<"ok"<<std::endl;}\n'

def main():
    _banner("Activity: Install C/C++ Compilers")
    print()
    _wrap("Checking for gcc, g++, clang, and clang++.")
    print()
    _hr()

    gnu_ok   = True
    clang_ok = True

    # gcc
    ok, ver = _run(["gcc", "--version"])
    print(f"  {'gcc':20s} {'FOUND    ' if ok else 'NOT FOUND'} {ver if ok else ''}")
    if not ok:
        gnu_ok = False

    # g++
    ok2, ver2 = _run(["g++", "--version"])
    print(f"  {'g++':20s} {'FOUND    ' if ok2 else 'NOT FOUND'} {ver2 if ok2 else ''}")
    if not ok2:
        gnu_ok = False

    # g++ compile test
    if gnu_ok:
        ok3, msg3 = _compile_test("g++", _HELLO)
        print(f"  {'g++ compile test':20s} {'PASSED' if ok3 else 'FAILED    ' + msg3}")
        if not ok3:
            gnu_ok = False

    # clang
    ok4, ver4 = _run(["clang", "--version"])
    print(f"  {'clang':20s} {'FOUND    ' if ok4 else 'NOT FOUND'} {ver4 if ok4 else ''}")
    if not ok4:
        clang_ok = False

    # clang++
    ok5, ver5 = _run(["clang++", "--version"])
    print(f"  {'clang++':20s} {'FOUND    ' if ok5 else 'NOT FOUND'} {ver5 if ok5 else ''}")
    if not ok5:
        clang_ok = False

    # clang++ compile test
    if clang_ok:
        ok6, msg6 = _compile_test("clang++", _HELLO)
        print(f"  {'clang++ compile test':20s} {'PASSED' if ok6 else 'FAILED    ' + msg6}")
        if not ok6:
            clang_ok = False

    _hr()
    print()

    all_ok = gnu_ok and clang_ok

    if not all_ok:
        os_name = platform.system()
        if not gnu_ok:
            _wrap("GCC/G++ was not found or failed to compile.")
            if os_name == "Linux":
                _wrap("Install with:")
                print("    sudo apt install build-essential")
            elif os_name == "Darwin":
                _wrap("Install with:")
                print("    xcode-select --install")
            print()
        if not clang_ok:
            _wrap("Clang/Clang++ was not found or failed to compile.")
            if os_name == "Linux":
                _wrap("Install with:")
                print("    sudo apt install clang clangd clang-format clang-tidy")
            elif os_name == "Darwin":
                _wrap("Clang is installed by the Xcode Command Line Tools:")
                print("    xcode-select --install")
            print()
        _wrap("See README.md for full installation instructions.")
        sys.exit(1)

    passphrase = _decrypt(_BLOB, ["gcc-verified", "gxx-verified"])
    if passphrase is None:
        _wrap("[error] Decryption failed -- contact your instructor.")
        sys.exit(1)
    _show_passphrase(passphrase)


if __name__ == "__main__":
    main()
