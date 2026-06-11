#!/usr/bin/env python3
"""
project-docs activity launcher.
Student writes six documentation files for a minimal C++ project.
Validation: checks that required section headers are present in each file.
"""

import atexit, os, shutil, subprocess, sys, tempfile, textwrap  # noqa: E401, I001
import hashlib as _hl, hmac as _hm  # noqa: E401

_SALT = bytes.fromhex("a3f1b2c4d5e6f7a8b9c0d1e2f3a4b5c6")
_KDF_ITERS = 100000
_BLOB = "142fde76c0c59e94bf2b409220f4e794082e2ddcdf67de1dfc8af3b44aeee7f92be25f76e6a1f8b6725d2016ab119d81701e0367d5c24f1e1c"
_VALIDATION_KEY = "all-docs-present"


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

_CHECKS = [
    (
        "README.md",
        [
            "# ",
            "## Description",
            "## Installation",
            "## Usage",
            "## Contributing",
            "## License",
        ],
    ),
    ("LICENSE", []),
    (
        "CHANGELOG.md",
        [
            "## [Unreleased]",
            "### Added",
            "### Changed",
            "### Fixed",
        ],
    ),
    (
        "CONTRIBUTORS.md",
        [
            "## Contributors",
        ],
    ),
    (
        "CODE_OF_CONDUCT.md",
        [
            "## Our Pledge",
        ],
    ),
    (
        "SECURITY.md",
        [
            "## Reporting a Vulnerability",
        ],
    ),
]


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


def _setup_project(project_dir):
    os.makedirs(os.path.join(project_dir, "src"), exist_ok=True)
    cmake_content = (
        "cmake_minimum_required(VERSION 3.16)\n"
        "project(myproject)\n"
        "add_executable(myproject src/main.cpp)\n"
    )
    with open(os.path.join(project_dir, "CMakeLists.txt"), "w") as f:
        f.write(cmake_content)
    main_content = (
        "#include <iostream>\n"
        "int main() {\n"
        '    std::cout << "Hello from myproject\\n";\n'
        "    return 0;\n"
        "}\n"
    )
    with open(os.path.join(project_dir, "src", "main.cpp"), "w") as f:
        f.write(main_content)


def _validate(project_dir):
    _banner("project-docs -- Checking Your Work")
    print()
    print("  Checking your documentation...")
    print()

    all_pass = True
    results = []

    for filename, required_headers in _CHECKS:
        path = os.path.join(project_dir, filename)
        if not os.path.isfile(path):
            results.append((filename, False, "file not found"))
            all_pass = False
            continue
        content = open(path, encoding="utf-8", errors="replace").read()
        if not content.strip():
            results.append((filename, False, "file is empty"))
            all_pass = False
            continue
        missing = [h for h in required_headers if h not in content]
        if missing:
            results.append((filename, False, "missing: " + ", ".join(missing)))
            all_pass = False
        else:
            results.append((filename, True, ""))

    col = 22
    for filename, passed, detail in results:
        status = "PASS" if passed else "FAIL"
        if detail:
            print(f"  {filename:<{col}} {status}  ({detail})")
        else:
            print(f"  {filename:<{col}} {status}")

    return all_pass


def main():
    work_dir = tempfile.mkdtemp(prefix="project-docs-")
    atexit.register(lambda: shutil.rmtree(work_dir, ignore_errors=True))

    project_dir = os.path.join(work_dir, "myproject")
    os.makedirs(project_dir, exist_ok=True)
    _setup_project(project_dir)

    banner_text = textwrap.dedent("""\

      ============================================================
       project-docs
      ============================================================

       You have a small C++ project with no documentation.
       Create the following files in this directory:

       README.md -- must include these exact headers (your content):
         # <project name of your choice>
         ## Description
         ## Installation
         ## Usage
         ## Contributing
         ## License

       LICENSE -- any open-source license text (MIT, Apache, etc.)

       CHANGELOG.md -- must include these exact headers:
         ## [Unreleased]
         ### Added
         ### Changed
         ### Fixed

       CONTRIBUTORS.md -- must include:
         ## Contributors

       CODE_OF_CONDUCT.md -- must include:
         ## Our Pledge

       SECURITY.md -- must include:
         ## Reporting a Vulnerability

       Write something real under each header. The validator only
       checks that the headers are present, not what you write.

       Type 'exit' when done.
      ============================================================

    """)

    rcfile = tempfile.NamedTemporaryFile(mode="w", suffix=".rc", delete=False)
    rcfile.write(
        f"PS1='\\u@project-docs:\\W\\$ '\n"
        f'cd "{project_dir}"\n'
        "cat << 'BANNER'\n" + banner_text + "\nBANNER\n"
    )
    rcfile.close()

    shell = os.environ.get("SHELL", "/bin/bash")

    try:
        while True:
            subprocess.run([shell, "--rcfile", rcfile.name])
            print()
            ok = _validate(project_dir)
            if ok:
                passphrase = _decrypt(_VALIDATION_KEY)
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
