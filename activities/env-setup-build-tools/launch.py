#!/usr/bin/env python3
"""Activity: Install CMake and Make

Verifies that cmake and make are installed and callable, then reveals
the passphrase.
"""
import sys, subprocess, platform, textwrap as _tw
import hashlib as _hl, hmac as _hm

_SALT      = bytes.fromhex("a3f1b2c4d5e6f7a8b9c0d1e2f3a4b5c6")
_KDF_ITERS = 100000
# Encrypted with answers=["cmake-verified","make-verified"]
# Re-generate via aprog-private/activities/env-setup-build-tools/gen_blob.py
_BLOB = "0f79a3b9791551581514a6b8aee7f6a5fcbe975c18ce3f7cef4dd786363a876501309671ab6e2003b5ae6c498adaf615bb648f8c5bae5087dc"

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

def _install_hint():
    os_name = platform.system()
    print()
    if os_name == "Linux":
        try:
            with open("/etc/os-release") as f:
                text = f.read().lower()
        except OSError:
            text = ""
        if "ubuntu" in text or "debian" in text:
            _wrap("Ubuntu / Debian / WSL -- run:")
            print("    sudo apt update && sudo apt install -y cmake make")
        elif "fedora" in text or "rhel" in text or "rocky" in text:
            _wrap("Fedora / RHEL / Rocky -- run:")
            print("    sudo dnf install cmake make")
        elif "arch" in text or "manjaro" in text:
            _wrap("Arch / Manjaro -- run:")
            print("    sudo pacman -S cmake make")
        else:
            _wrap("Install cmake and make using your distribution's package manager.")
    elif os_name == "Darwin":
        _wrap("macOS -- run:")
        print("    brew install cmake make")
    elif os_name == "Windows":
        _wrap("You appear to be running on Windows (not WSL). The recommended "
              "approach is to install cmake and make inside your WSL terminal "
              "(see the shell activity). For native Windows, see README.md.")
    else:
        _wrap("See README.md for installation instructions for your platform.")
    print()
    _wrap("After installing, open a new terminal and run this script again.")
    print()

def main():
    _banner("Activity: Install CMake and Make")
    print()
    _wrap("This script checks that cmake and make are installed and working.")
    print()
    _hr()

    all_ok = True

    ok, ver = _run(["cmake", "--version"])
    if ok:
        print(f"  {'cmake':20s} FOUND     {ver}")
    else:
        print(f"  {'cmake':20s} NOT FOUND")
        all_ok = False

    # On some systems 'make' may be 'gmake' (macOS Homebrew)
    make_cmd = "make"
    ok2, ver2 = _run(["make", "--version"])
    if not ok2:
        ok2, ver2 = _run(["gmake", "--version"])
        if ok2:
            make_cmd = "gmake"
    if ok2:
        print(f"  {'make / gmake':20s} FOUND     {ver2}")
    else:
        print(f"  {'make':20s} NOT FOUND")
        all_ok = False

    _hr()
    print()

    if not all_ok:
        _wrap("One or more checks failed. See README.md for installation "
              "instructions, or read the hints below.")
        _install_hint()
        sys.exit(1)

    _wrap("All checks passed.")
    passphrase = _decrypt(_BLOB, ["cmake-verified", "make-verified"])
    if passphrase is None:
        _wrap("[error] Decryption failed -- contact your instructor.")
        sys.exit(1)
    _show_passphrase(passphrase)


if __name__ == "__main__":
    main()
