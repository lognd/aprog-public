#!/usr/bin/env python3
"""Activity: Install and Configure an IDE

Checks that at least one supported IDE (VS Code, CLion, Neovim) is
installed and has the required tooling, then reveals the passphrase.
"""
import sys, subprocess, os, platform, textwrap as _tw
import hashlib as _hl, hmac as _hm

_SALT      = bytes.fromhex("a3f1b2c4d5e6f7a8b9c0d1e2f3a4b5c6")
_KDF_ITERS = 100000
# Encrypted with answers=["ide-verified"]
# Re-generate via aprog-private/activities/env-setup-ide/gen_blob.py
_BLOB = "4c63dc9bdea244f1c874f970352a00477d02377e88e53af0b617b701e6ed0712f422845940201f9f99a4f5005c727ad400b5cb41d669"

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

def _check_vscode():
    """Return (found, version_string, issues)."""
    ok, ver = _run(["code", "--version"])
    if not ok:
        return False, "", []
    issues = []
    # Check for the C++ extension
    ok2, exts = _run(["code", "--list-extensions"])
    if ok2:
        ext_list = exts.lower()
        if "ms-vscode.cpptools" not in ext_list and "llvm-vs-code-extensions.vscode-clangd" not in ext_list:
            issues.append("C/C++ extension (ms-vscode.cpptools) is not installed.")
        if "ms-vscode.cmake-tools" not in ext_list:
            issues.append("CMake Tools extension (ms-vscode.cmake-tools) is not installed.")
    return True, ver.split()[0] if ver else "unknown", issues

def _check_clion():
    """Check for CLion via JetBrains Toolbox shell script or clion command."""
    for cmd in ["clion", "clion.sh"]:
        ok, ver = _run([cmd, "--version"])
        if ok:
            return True, ver, []
    # Check common install paths
    paths = [
        os.path.expanduser("~/.local/share/JetBrains/Toolbox/apps/CLion"),
        "/opt/clion",
        "/Applications/CLion.app",
        os.path.expandvars("%LOCALAPPDATA%\\JetBrains\\Toolbox\\apps\\CLion"),
    ]
    for p in paths:
        if os.path.exists(p):
            return True, "found at " + p, []
    return False, "", []

def _check_neovim():
    ok, ver = _run(["nvim", "--version"])
    if not ok:
        return False, "", []
    issues = []
    # Check version >= 0.10
    first = ver  # e.g. "NVIM v0.10.0"
    try:
        parts = first.split("v")[1].split(".")
        major, minor = int(parts[0]), int(parts[1])
        if (major, minor) < (0, 10):
            issues.append(f"Neovim {first} is too old; version 0.10 or later is recommended.")
    except (IndexError, ValueError):
        pass
    return True, first, issues

def main():
    _banner("Activity: Install and Configure an IDE")
    print()
    _wrap("This script checks for VS Code, CLion, or Neovim.")
    _wrap("You need at least one fully set up to pass.")
    print()
    _hr()

    found_ide = None
    all_issues = []

    # VS Code
    vsc_found, vsc_ver, vsc_issues = _check_vscode()
    label = "VS Code"
    if vsc_found:
        print(f"  {label:20s} FOUND     {vsc_ver}")
        for issue in vsc_issues:
            print(f"  {'':20s} WARN      {issue}")
        if not vsc_issues:
            found_ide = "vscode"
        else:
            all_issues.extend(vsc_issues)
    else:
        print(f"  {label:20s} not found")

    # CLion
    cl_found, cl_ver, cl_issues = _check_clion()
    label2 = "CLion"
    if cl_found:
        print(f"  {label2:20s} FOUND     {cl_ver}")
        if not cl_issues and found_ide is None:
            found_ide = "clion"
    else:
        print(f"  {label2:20s} not found")

    # Neovim
    nv_found, nv_ver, nv_issues = _check_neovim()
    label3 = "Neovim"
    if nv_found:
        print(f"  {label3:20s} FOUND     {nv_ver}")
        for issue in nv_issues:
            print(f"  {'':20s} WARN      {issue}")
        if not nv_issues and found_ide is None:
            found_ide = "neovim"
    else:
        print(f"  {label3:20s} not found")

    _hr()
    print()

    if found_ide is None and (vsc_found or cl_found or nv_found):
        # IDE found but has issues (e.g., missing extensions)
        _wrap("An IDE was found but is missing required configuration.")
        for issue in all_issues:
            _wrap("  - " + issue)
        print()
        _wrap("Fix the issues above, then run this script again.")
        print()
        if vsc_found and all_issues:
            _wrap("To install missing VS Code extensions:")
            print("    code --install-extension ms-vscode.cpptools")
            print("    code --install-extension ms-vscode.cmake-tools")
        sys.exit(1)
    elif found_ide is None:
        _wrap("No supported IDE was found. Install one of:")
        print("    VS Code:  https://code.visualstudio.com")
        print("    CLion:    https://www.jetbrains.com/clion (free for students)")
        print("    Neovim:   https://neovim.io")
        print()
        _wrap("See README.md for full setup instructions including required "
              "extensions and IDE configuration.")
        sys.exit(1)

    _wrap(f"IDE check passed ({found_ide}).")
    passphrase = _decrypt(_BLOB, ["ide-verified"])
    if passphrase is None:
        _wrap("[error] Decryption failed -- contact your instructor.")
        sys.exit(1)
    _show_passphrase(passphrase)


if __name__ == "__main__":
    main()
