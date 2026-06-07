#!/usr/bin/env python3
"""
Complexity Clock activity launcher.
Shell drop: student builds and runs the benchmark, observes timing.
Quiz: two questions that require reasoning about the results.
"""
import json, os, sys, shutil, subprocess, tempfile, zipfile, textwrap
import hashlib as _hl, hmac as _hm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ZIP   = os.path.join(SCRIPT_DIR, "repo.zip")

_SALT      = bytes.fromhex("a3f1b2c4d5e6f7a8b9c0d1e2f3a4b5c6")
_KDF_ITERS = 100000
_BLOB      = "4cf10913a1ca95b16d67ba0c3b538e09b1e9fb8c8e9ab26b26ad5dda14d4c3244768c01ea38c018cf779d52fc4673c42b155b3e7"

def _derive_key(answers):
    return _hl.pbkdf2_hmac("sha256", "|".join(answers).encode(), _SALT, _KDF_ITERS)

def _stream(key, length):
    ks, i = b"", 0
    while len(ks) < length:
        ks += _hl.sha256(key + i.to_bytes(4, "little")).digest()
        i += 1
    return ks[:length]

def _decrypt(answers):
    key  = _derive_key(answers)
    blob = bytes.fromhex(_BLOB)
    ct, mac = blob[:-32], blob[-32:]
    if not _hm.compare_digest(mac, _hm.new(key, ct, _hl.sha256).digest()):
        return None
    return bytes(a ^ b for a, b in zip(ct, _stream(key, len(ct)))).decode()

_LINE_WIDTH = 70

def _banner(title):
    print("=" * _LINE_WIDTH)
    pad = (_LINE_WIDTH - len(title) - 2) // 2
    print(" " * pad + " " + title + " " * pad)
    print("=" * _LINE_WIDTH)

def _hr():
    print("-" * _LINE_WIDTH)

def _wrap(text):
    for line in textwrap.wrap(text, width=_LINE_WIDTH - 4,
                              initial_indent="  ",
                              subsequent_indent="    "):
        print(line)

def _show_passphrase(p):
    print()
    _hr()
    print(f"  Passphrase: {p}")
    _hr()
    print()

def _ask(prompt, hint, answer, wrong):
    while True:
        print()
        _wrap(prompt)
        print()
        try:
            raw = input("  > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit(0)
        if raw == answer:
            return raw
        if raw in wrong:
            print()
            _wrap(f"Not quite. {wrong[raw]}")
        else:
            print()
            _wrap(f"That is not right.")
        print()
        _wrap(f"Hint: {hint}")

def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)

QUESTIONS = [
    {
        "prompt": (
            "One of the seven functions took significantly more time than the "
            "others.  What is its name?  (lowercase, exactly as printed)"
        ),
        "hint": "Look at the Time column.  One entry stands out.  Read that function carefully -- all of it, including any helpers it calls.",
        "answer": "carol",
        "wrong": {
            "alice": "Alice uses a direct formula with no loops.  She is one of the fastest.",
            "bob":   "Bob has a nested loop -- but look at what the inner loop actually does.  Check the time column.",
            "dave":  "Dave uses a do-while loop.  Check the time column again.",
            "eve":   "Eve uses a while loop.  Check the time column again.",
            "frank": "Frank uses a switch inside a for loop.  Check the time column again.",
            "grace": "Grace counts down with if checks.  Check the time column again.",
        },
    },
    {
        "prompt": (
            "If N were doubled to 80000, approximately how many times longer "
            "would carol take compared to N=40000?  Enter a whole number."
        ),
        "hint": (
            "Think about how many total loop iterations carol performs for a "
            "given N.  If N doubles, what happens to that count?  "
            "Try writing it out: what is the total work for N=4?  For N=8?"
        ),
        "answer": "4",
        "wrong": {
            "2":  "That would be true if carol were O(N).  But carol is not O(N).",
            "8":  "That would be true for O(N^3).  Count carol's iterations more carefully.",
            "16": "That is too high.  Work out the iteration count for small N.",
        },
    },
]

def main():
    if not os.path.isfile(REPO_ZIP):
        die("repo.zip not found.")

    work_dir = tempfile.mkdtemp(prefix="complexity-clock-")

    def cleanup():
        shutil.rmtree(work_dir, ignore_errors=True)

    import atexit
    atexit.register(cleanup)

    with zipfile.ZipFile(REPO_ZIP, "r") as zf:
        zf.extractall(work_dir)

    entries = [e for e in os.listdir(work_dir)
               if os.path.isdir(os.path.join(work_dir, e))]
    if len(entries) != 1:
        die("unexpected zip structure")
    repo_dir = os.path.join(work_dir, entries[0])

    rcfile = tempfile.NamedTemporaryFile(mode="w", suffix=".rc", delete=False)
    banner_text = textwrap.dedent(f"""\

      ============================================================
       Complexity Clock
      ============================================================

       Seven functions all compute the same value.  Build the
       benchmark and run it:

         make && ./clock

       Read the output carefully.  Study the source code.
       Type 'exit' when you are ready to answer two questions.
      ============================================================

    """)
    rcfile.write(
        f'PS1=\'\\u@complexity-clock:\\W\\$ \'\n'
        f'cd "{repo_dir}"\n'
        "cat << 'BANNER'\n" + banner_text + "\nBANNER\n"
    )
    rcfile.close()

    shell = os.environ.get("SHELL", "/bin/bash")
    subprocess.run([shell, "--rcfile", rcfile.name])

    print()
    _banner("Complexity Clock -- Quiz")

    answers = []
    for q in QUESTIONS:
        a = _ask(q["prompt"], q["hint"], q["answer"], q["wrong"])
        answers.append(a)

    print()
    passphrase = _decrypt(answers)
    if passphrase:
        _wrap("Correct on both counts.")
        _show_passphrase(passphrase)
    else:
        _wrap("Answers did not match -- this should not happen.")


if __name__ == "__main__":
    main()
