#!/usr/bin/env python3
"""
Activity: Virtual Environment Workshop

Hands-on, no quiz. Drops you into a shell inside a fresh temporary
working directory and asks you to build two virtual environments -- one
the classic way (`python3 -m venv` + `pip`), one the modern way (`uv`) --
and install a package into each. When you exit the shell, this script
inspects the directory to confirm you actually did it, then reveals the
passphrase.

Nothing here touches your real projects: everything happens in a throwaway
temp directory that is deleted when the script exits.

Usage: python3 launch.py
"""
import atexit
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap as _tw

_LINE_WIDTH = 70

# The package each environment must end up with. Tiny, pure-Python, and
# fun to see working -- installing it proves pip/uv reached PyPI and put a
# real dependency inside the environment.
_TARGET_PKG = "cowsay"

# Completion token. This activity is validated by inspecting the work you
# did on disk (both environments must exist and import the package), so the
# passphrase is only printed once those checks pass.
_PASSPHRASE = "one-venv-per-project-keeps-the-mess-away"


def _banner(title):
    print("=" * _LINE_WIDTH)
    pad = (_LINE_WIDTH - len(title) - 2) // 2
    print(" " * pad + " " + title + " " + " " * pad)
    print("=" * _LINE_WIDTH)


def _hr():
    print("-" * _LINE_WIDTH)


def _wrap(text):
    for line in _tw.wrap(text, width=_LINE_WIDTH - 4,
                         initial_indent="  ", subsequent_indent="  "):
        print(line)


def _show_passphrase(p):
    print()
    _hr()
    print(f"  Passphrase: {p}")
    _hr()
    print()


def _venv_python(venv_dir):
    """Path to the interpreter inside a virtual environment, or None.

    Handles both the POSIX layout (`bin/python`) and the Windows layout
    (`Scripts/python.exe`), so the check works wherever the student ran.
    """
    candidates = [
        os.path.join(venv_dir, "bin", "python"),
        os.path.join(venv_dir, "bin", "python3"),
        os.path.join(venv_dir, "Scripts", "python.exe"),
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    return None


def _is_venv(venv_dir):
    """True if venv_dir looks like a real virtual environment."""
    return (
        os.path.isfile(os.path.join(venv_dir, "pyvenv.cfg"))
        and _venv_python(venv_dir) is not None
    )


def _imports_target(venv_dir):
    """True if the environment's own interpreter can import the target package."""
    py = _venv_python(venv_dir)
    if py is None:
        return False
    try:
        r = subprocess.run(
            [py, "-c", f"import {_TARGET_PKG}"],
            capture_output=True, text=True, timeout=30,
        )
        return r.returncode == 0
    except Exception:
        return False


def _check(work_dir):
    """Validate both environments. Returns (ok, list_of_result_lines)."""
    venv_dir = os.path.join(work_dir, "venv")
    uvenv_dir = os.path.join(work_dir, "uvenv")

    results = []

    # Part 1: python3 -m venv + pip install
    venv_exists = _is_venv(venv_dir)
    results.append(("A virtual environment named 'venv' exists "
                    "(python3 -m venv venv)", venv_exists))
    venv_has_pkg = venv_exists and _imports_target(venv_dir)
    results.append((f"'venv' has {_TARGET_PKG} installed into it "
                    f"(pip install {_TARGET_PKG})", venv_has_pkg))

    # Part 2: uv venv + uv pip install
    uvenv_exists = _is_venv(uvenv_dir)
    results.append(("A virtual environment named 'uvenv' exists "
                    "(uv venv uvenv)", uvenv_exists))
    uvenv_has_pkg = uvenv_exists and _imports_target(uvenv_dir)
    results.append((f"'uvenv' has {_TARGET_PKG} installed into it "
                    f"(uv pip install --python uvenv {_TARGET_PKG})",
                    uvenv_has_pkg))

    ok = all(passed for _, passed in results)
    return ok, results


def _print_results(results):
    print()
    _hr()
    for label, passed in results:
        mark = "PASS" if passed else "TODO"
        print(f"  [{mark}] {label}")
    _hr()


def _instructions(work_dir):
    print()
    _wrap("You are now in a shell inside a fresh, throwaway directory:")
    print(f"    {work_dir}")
    print()
    _wrap("Complete BOTH parts below, then type 'exit' (or press Ctrl-D) "
          "to have your work checked.")
    print()
    print("  PART 1 -- the classic workflow (python3 -m venv + pip)")
    print()
    print("    python3 -m venv venv        # create an environment in ./venv")
    print("    source venv/bin/activate    # turn it on (your prompt shows (venv))")
    print(f"    pip install {_TARGET_PKG}            # install INTO the active venv")
    print(f"    {_TARGET_PKG} -t \"it works!\"       # see the package you installed run")
    print("    deactivate                  # turn the environment back off")
    print()
    print("  PART 2 -- the modern workflow (uv)")
    print()
    print("    uv venv uvenv                          # create an environment in ./uvenv")
    print(f"    uv pip install --python uvenv {_TARGET_PKG}    # install into that environment")
    print()
    _wrap("Tip: on Windows (not WSL) the activate command is instead "
          "'venv\\\\Scripts\\\\activate'. If 'uv' is not found, install it "
          "first -- see the README.")
    print()


def main():
    _banner("Activity: Virtual Environment Workshop")
    print()
    _wrap("A virtual environment is a private, per-project copy of Python's "
          "package folder, so each project's dependencies stay separate "
          "instead of piling up in one shared, system-wide install. In this "
          "activity you will build two of them -- one with the standard-"
          "library 'venv' module plus 'pip', and one with 'uv' -- and "
          "install a package into each.")

    if not shutil.which("python3"):
        _wrap("[error] python3 was not found. Complete the Python setup "
              "activity (env-setup-python) before this one.")
        sys.exit(1)

    work_dir = tempfile.mkdtemp(prefix="venv-workshop-")
    atexit.register(lambda: shutil.rmtree(work_dir, ignore_errors=True))

    _instructions(work_dir)

    rcfile = tempfile.NamedTemporaryFile(mode="w", suffix=".rc", delete=False)
    rcfile.write(_tw.dedent(f"""\
        PS1='venv-workshop:\\W\\$ '
        cd "{work_dir}"
        echo ""
        echo "  Working directory: {work_dir}"
        echo "  Do PART 1 and PART 2, then type 'exit' to be checked."
        echo ""
    """))
    rcfile.close()
    atexit.register(lambda: os.path.exists(rcfile.name) and os.remove(rcfile.name))

    shell = os.environ.get("SHELL", "/bin/bash")
    subprocess.run([shell, "--rcfile", rcfile.name])

    ok, results = _check(work_dir)
    _print_results(results)

    if not ok:
        print()
        _wrap("Not all checks passed yet. The environments and the package "
              "installs must all be present in the working directory at the "
              "moment you exit the shell. Re-run this activity and finish "
              "every step above. (If a 'pip install' or 'uv pip install' "
              "failed, check your internet connection -- both need to reach "
              "PyPI once to download the package.)")
        print()
        sys.exit(1)

    print()
    _wrap("Both environments exist and both have the package installed. "
          "You built a virtual environment two different ways and proved "
          "each one is isolated and populated. Well done.")
    _show_passphrase(_PASSPHRASE)


if __name__ == "__main__":
    main()
