#!/usr/bin/env python3
import os
import sys
import subprocess
import tempfile
import atexit
import textwrap

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE = os.path.join(SCRIPT_DIR, "myfs.img")


def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def main():
    if os.geteuid() != 0:
        die("this script must be run with sudo")

    if not os.path.isfile(IMAGE):
        die(f"image not found: {IMAGE}")

    mount_point = tempfile.mkdtemp(prefix="terminal-archeology-")
    rcfile = tempfile.NamedTemporaryFile(mode="w", suffix=".rc", delete=False)

    def cleanup():
        subprocess.run(["umount", mount_point], check=False)
        try:
            os.rmdir(mount_point)
        except OSError:
            pass
        try:
            os.remove(rcfile.name)
        except OSError:
            pass

    atexit.register(cleanup)

    result = subprocess.run(["mount", "-o", "loop", IMAGE, mount_point])
    if result.returncode != 0:
        die("failed to mount image")

    lost_and_found = os.path.join(mount_point, "lost+found")
    if os.path.isdir(lost_and_found):
        os.rmdir(lost_and_found)

    rcfile.write(textwrap.dedent(f"""\
        HOME="{mount_point}"
        HISTFILE=""
        PS1='\\u@archeology:$(pwd | sed "s|{mount_point}||;s|^$|/|")\\$ '
        cd "{mount_point}"
    """))
    rcfile.close()

    print("Type 'exit' or press Ctrl-D when done.\n")

    shell = os.environ.get("SHELL", "/bin/bash")
    env = os.environ.copy()
    env["HOME"] = mount_point
    subprocess.run([shell, "--rcfile", rcfile.name], cwd=mount_point, env=env)


if __name__ == "__main__":
    main()
