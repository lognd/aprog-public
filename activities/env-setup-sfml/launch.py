#!/usr/bin/env python3
"""Activity: Install SFML

Verifies that the SFML headers are present and that a small program
using sf::Image compiles, links, and runs, then reveals the passphrase.
"""
import sys, subprocess, tempfile, os, platform, textwrap as _tw
import hashlib as _hl, hmac as _hm

_SALT      = bytes.fromhex("a3f1b2c4d5e6f7a8b9c0d1e2f3a4b5c6")
_KDF_ITERS = 100000
# Encrypted with answers=["sfml-headers-verified", "sfml-links-verified"]
# Re-generate via aprog-private/activities/env-setup-shell/gen_blobs.py
_BLOB = "cb7316a13a4800055ab3871e7c0e20ded2ecdd11156ed2aac90c458657700e7db7ebbe778755e9fe786b2291ed6e6162d734b58002"

_LINE_WIDTH = 70

_INCLUDE_DIRS = ["/usr/include", "/usr/local/include", "/opt/homebrew/include"]

_SFML_PROGRAM = """\
#include <SFML/Graphics.hpp>
#include <cstdio>
int main() {
    sf::Image img;
    img.create(2, 2, sf::Color::Red);
    sf::Vector2u size = img.getSize();
    std::printf("%u %u\\n", size.x, size.y);
    return 0;
}
"""
_EXPECTED_OUTPUT = "2 2"


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

def _find_sfml_headers():
    """Return the include dir containing SFML/Graphics.hpp, or None."""
    for d in _INCLUDE_DIRS:
        if os.path.exists(os.path.join(d, "SFML", "Graphics.hpp")):
            return d
    return None

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
            print("    sudo apt update && sudo apt install -y libsfml-dev")
        elif "fedora" in text or "rhel" in text or "rocky" in text:
            _wrap("Fedora / RHEL / Rocky -- run:")
            print("    sudo dnf install SFML-devel")
        elif "arch" in text or "manjaro" in text:
            _wrap("Arch / Manjaro -- run:")
            print("    sudo pacman -S sfml")
        else:
            _wrap("Install the SFML development package using your "
                  "distribution's package manager.")
    elif os_name == "Darwin":
        _wrap("macOS -- run:")
        print("    brew install sfml")
    elif os_name == "Windows":
        _wrap("You appear to be running on Windows (not WSL). The "
              "recommended approach is to install SFML inside your WSL "
              "terminal (see the shell activity): sudo apt install -y "
              "libsfml-dev. For native Windows, see README.md.")
    else:
        _wrap("See README.md for installation instructions for your platform.")
    print()
    _wrap("After installing, open a new terminal and run this script again.")
    print()

def _compile_link_test(include_dir):
    """Compile, link, and run the sf::Image test program.

    Returns (ok, stage, message) where stage is one of
    "compile", "run", or "" (success).
    """
    with tempfile.NamedTemporaryFile(suffix=".cpp", mode="w", delete=False) as f:
        f.write(_SFML_PROGRAM)
        src_path = f.name
    out_path = src_path.replace(".cpp", "")

    cmd = ["g++", "-std=c++17", src_path, "-o", out_path,
           "-lsfml-graphics", "-lsfml-window", "-lsfml-system"]
    if include_dir not in ("/usr/include",):
        cmd.insert(1, f"-I{include_dir}")
    ok, msg = _run(cmd)

    if not ok:
        try:
            os.unlink(src_path)
        except OSError:
            pass
        return False, "compile", msg

    run_ok, run_out = False, ""
    try:
        r = subprocess.run([out_path], capture_output=True, text=True, timeout=10)
        run_out = r.stdout.strip()
        run_ok = r.returncode == 0 and run_out == _EXPECTED_OUTPUT
    except Exception as e:
        run_out = str(e)

    try:
        os.unlink(src_path)
        if os.path.exists(out_path):
            os.unlink(out_path)
    except OSError:
        pass

    if not run_ok:
        return False, "run", run_out
    return True, "", ""

def main():
    _banner("Activity: Install SFML")
    print()
    _wrap("Checking that the SFML headers are installed and that a small "
          "program using sf::Image compiles, links, and runs.")
    print()
    _hr()

    # g++ must exist first -- SFML verification depends on it.
    gxx_ok, gxx_ver = _run(["g++", "--version"])
    print(f"  {'g++':20s} {'FOUND    ' if gxx_ok else 'NOT FOUND'} {gxx_ver if gxx_ok else ''}")
    if not gxx_ok:
        _hr()
        print()
        _wrap("g++ was not found. Complete the compiler activity "
              "(env-setup-compiler) before this one.")
        sys.exit(1)

    # SFML headers
    include_dir = _find_sfml_headers()
    if include_dir:
        print(f"  {'SFML/Graphics.hpp':20s} FOUND     {include_dir}/SFML/Graphics.hpp")
    else:
        print(f"  {'SFML/Graphics.hpp':20s} NOT FOUND")
        _hr()
        print()
        _wrap("SFML headers were not found in any of the standard include "
              "paths checked: " + ", ".join(_INCLUDE_DIRS) + ".")
        _install_hint()
        sys.exit(1)

    headers_ok = True

    # Compile + link + run test
    ok, stage, msg = _compile_link_test(include_dir)
    if ok:
        print(f"  {'compile/link/run':20s} PASSED")
    else:
        print(f"  {'compile/link/run':20s} FAILED    ({stage}) {msg}")

    _hr()
    print()

    if not (headers_ok and ok):
        if stage == "compile":
            _wrap("Compilation or linking failed. This usually means the "
                  "SFML development libraries (not just headers) are "
                  "missing, or the linker cannot find -lsfml-graphics.")
        elif stage == "run":
            _wrap("The program compiled but produced unexpected output. "
                  "This can happen with a broken or partial SFML "
                  "installation.")
        _install_hint()
        sys.exit(1)

    _wrap("All checks passed.")
    passphrase = _decrypt(_BLOB, ["sfml-headers-verified", "sfml-links-verified"])
    if passphrase is None:
        _wrap("[error] Decryption failed -- contact your instructor.")
        sys.exit(1)
    _show_passphrase(passphrase)


if __name__ == "__main__":
    main()
