#!/usr/bin/env python3
"""Activity: Set Up Git and GitHub

Verifies that git is installed and configured with a name and email,
that gh is installed, and that gh is authenticated to GitHub.
"""
import sys, subprocess, textwrap as _tw
import hashlib as _hl, hmac as _hm

_SALT      = bytes.fromhex("a3f1b2c4d5e6f7a8b9c0d1e2f3a4b5c6")
_KDF_ITERS = 100000
# Encrypted with answers=["git-verified", "gh-verified"]
# Re-generate via aprog-private/activities/gen_blobs.py
_BLOB = "01ba7fd1e509e3ae18bdff62a6bb1e578b777501479ddf250cc6455c070e725b899f12d873b38167ec8520b35a1baea9eb78634bfc"

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

def main():
    _banner("Activity: Set Up Git and GitHub")
    print()
    _wrap("Checking git installation, identity configuration, and gh authentication.")
    print()
    _hr()

    all_ok = True

    # git installed
    git_ok, git_ver = _run(["git", "--version"])
    print(f"  {'git':20s} {'FOUND    ' if git_ok else 'NOT FOUND'} {git_ver if git_ok else ''}")
    if not git_ok:
        all_ok = False

    # git user.name
    name_ok, name_val = _run(["git", "config", "--global", "user.name"])
    name_set = name_ok and bool(name_val.strip())
    print(f"  {'user.name':20s} {'SET      ' if name_set else 'NOT SET  '} {name_val.strip() if name_set else ''}")
    if not name_set:
        all_ok = False

    # git user.email
    email_ok, email_val = _run(["git", "config", "--global", "user.email"])
    email_set = email_ok and bool(email_val.strip())
    print(f"  {'user.email':20s} {'SET      ' if email_set else 'NOT SET  '} {email_val.strip() if email_set else ''}")
    if not email_set:
        all_ok = False

    # gh installed
    gh_ok, gh_ver = _run(["gh", "--version"])
    print(f"  {'gh':20s} {'FOUND    ' if gh_ok else 'NOT FOUND'} {gh_ver if gh_ok else ''}")
    if not gh_ok:
        all_ok = False

    # gh authenticated
    if gh_ok:
        auth_ok, auth_msg = _run(["gh", "auth", "status"])
        print(f"  {'gh auth':20s} {'OK       ' if auth_ok else 'NOT LOGGED IN'}")
        if not auth_ok:
            all_ok = False
    else:
        print(f"  {'gh auth':20s} skipped (gh not found)")

    _hr()
    print()

    if not all_ok:
        if not git_ok:
            _wrap("git is not installed. On Ubuntu/WSL:")
            print("    sudo apt install git")
            print()
        if not name_set or not email_set:
            _wrap("git identity is not configured. Run:")
            print('    git config --global user.name "Your Name"')
            print('    git config --global user.email "you@example.com"')
            print()
        if not gh_ok:
            _wrap("gh is not installed. On Ubuntu/WSL:")
            print("    sudo apt install gh")
            _wrap("See README.md if that does not work.")
            print()
        if gh_ok and not auth_ok:
            _wrap("gh is not authenticated. Run:")
            print("    gh auth login")
            _wrap("and complete the browser flow.")
            print()
        _wrap("See README.md for full setup instructions.")
        sys.exit(1)

    passphrase = _decrypt(_BLOB, ["git-verified", "gh-verified"])
    if passphrase is None:
        _wrap("[error] Decryption failed -- contact your instructor.")
        sys.exit(1)
    _show_passphrase(passphrase)


if __name__ == "__main__":
    main()
