#!/usr/bin/env python3
"""Activity: Install Python and Course Tools

Verifies Python 3.10+, uv, and all required course tools, then
reveals the passphrase.
"""
import sys, subprocess, platform, textwrap as _tw
import hashlib as _hl, hmac as _hm

_SALT      = bytes.fromhex("a3f1b2c4d5e6f7a8b9c0d1e2f3a4b5c6")
_KDF_ITERS = 100000
# Encrypted with answers=["python-verified", "pip-verified"]
# Re-generate via aprog-private/activities/env-setup-shell/gen_blobs.py
_BLOB = "df7096d14c47a1b87b7402a45b6ee3af058cace0fec3353efafb0d292cf67e819e7101e242286bc8babe0589f38e772f40"

_LINE_WIDTH = 70
_MIN_PYTHON = (3, 10)
_TOOLS = ["uv", "ruff", "ty", "pytest", "black", "mypy"]

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

def main():
    _banner("Activity: Install Python and Course Tools")
    print()
    _wrap("Checking Python version and required course tools.")
    print()
    _hr()

    all_ok = True

    # Python version (we are already running Python)
    v = sys.version_info
    ver_str = f"{v.major}.{v.minor}.{v.micro}"
    if (v.major, v.minor) >= _MIN_PYTHON:
        print(f"  {'python3':20s} FOUND     Python {ver_str}")
    else:
        print(f"  {'python3':20s} TOO OLD   Python {ver_str}  (need >= 3.10)")
        all_ok = False

    # pip (via this interpreter; students must know the classic installer too)
    ok_pip, ver_pip = _run([sys.executable, "-m", "pip", "--version"])
    if ok_pip:
        parts = ver_pip.split()
        print(f"  {'pip':20s} FOUND     {parts[0]} {parts[1]}")
    else:
        print(f"  {'pip':20s} NOT FOUND")
        all_ok = False

    # Course tools
    missing = []
    for tool in _TOOLS:
        ok, ver = _run([tool, "--version"])
        if ok:
            print(f"  {tool:20s} FOUND     {ver}")
        else:
            print(f"  {tool:20s} NOT FOUND")
            missing.append(tool)
            all_ok = False

    _hr()
    print()

    if not all_ok:
        if missing:
            _wrap("Missing tools: " + ", ".join(missing))
            print()
            if "uv" in missing:
                _wrap("Install uv first (see README.md Step 2):")
                print("    curl -LsSf https://astral.sh/uv/install.sh | sh")
                print()
            others = [t for t in missing if t != "uv"]
            if others:
                _wrap("Install the remaining tools with uv:")
                for tool in others:
                    print(f"    uv tool install {tool}")
                print()
            _wrap("After installing, open a new terminal and run this script "
                  "again if the commands are still not found. If they are "
                  "still missing, see Troubleshooting in README.md (PATH).")
        elif not ok_pip:
            _wrap("pip is missing for this Python. Install it with your "
                  "system package manager (e.g. sudo apt install python3-pip) "
                  "-- see README.md Step 4.")
        elif (v.major, v.minor) < _MIN_PYTHON:
            _wrap(f"Python {ver_str} is too old. Install Python 3.10 or later "
                  "and re-run this script with the newer version.")
        sys.exit(1)

    passphrase = _decrypt(_BLOB, ["python-verified", "pip-verified"])
    if passphrase is None:
        _wrap("[error] Decryption failed -- contact your instructor.")
        sys.exit(1)
    _show_passphrase(passphrase)


if __name__ == "__main__":
    main()
