#!/usr/bin/env python3
"""Activity: File I/O Contracts

Ten questions covering the exact contracts of open(), read(), write(),
close(), errno, and perror().  Each question shows the permitted answer
choices explicitly.  All ten correct unlocks the passphrase.
"""
import json, sys, hashlib as _hl, hmac as _hm, textwrap as _tw

# -- Crypto --
_SALT      = bytes.fromhex("a3f1b2c4d5e6f7a8b9c0d1e2f3a4b5c6")
_KDF_ITERS = 100000

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

_BLOB = "3dc27a0a50f17280d6effb2e8cfb522c335f8aa1f41fd85c45eab0cbd3ab59b5c5d04a9c9af997a9ad8428f4f29dcfe7d85194663740"

QUESTIONS = json.loads(r"""
[
  {
    "cluster": "open() -- flags and errno",
    "prompt": "open(\"notes.txt\", O_RDONLY) is called.  The file does not exist and\nO_CREAT is not set.  What errno symbol is set?\n\n  Type exactly one of: ENOENT / EBADF / EMFILE / EACCES",
    "hint": "The failure reason is that the named file does not exist in the filesystem.",
    "answer": "ENOENT",
    "wrong": {
      "EBADF":  "EBADF means an invalid fd was passed to a syscall.  open() has not returned an fd yet.",
      "EMFILE": "EMFILE means the process has too many open files.  The file here does not exist at all.",
      "EACCES": "EACCES means permission denied.  The file is simply missing, not forbidden."
    },
    "explanation": "ENOENT (No such file or directory) is set when the named path does not exist and O_CREAT was not specified."
  },
  {
    "cluster": "open() -- flags and errno",
    "prompt": "open(\"notes.txt\", O_RDONLY) is called.  The file does not exist and\nO_CREAT is not set.  What does open() return?\n\n  Type a number.",
    "hint": "All POSIX I/O functions signal failure the same way.",
    "answer": "-1",
    "wrong": {
      "0":    "0 is what read() returns at EOF.  open() returns -1 on failure.",
      "NULL": "NULL is a pointer constant.  open() returns an integer."
    },
    "explanation": "open() returns -1 on any failure.  errno is then set to ENOENT because the file was not found and O_CREAT was absent."
  },
  {
    "cluster": "open() -- lowest available fd",
    "prompt": "A process has fds 0, 1, and 2 open and nothing else.  open() succeeds.\nWhat integer does it return?\n\n  Type a number.",
    "hint": "The kernel always assigns the lowest available fd slot.",
    "answer": "3",
    "wrong": {
      "0": "fd 0 is stdin -- already occupied.",
      "1": "fd 1 is stdout -- already occupied.",
      "2": "fd 2 is stderr -- already occupied."
    },
    "explanation": "open() returns the lowest available fd.  With 0, 1, and 2 taken, the next available slot is 3."
  },
  {
    "cluster": "read() -- return values",
    "prompt": "read() is called on a file.  There are no more bytes to deliver.\nWhat does read() return?\n\n  Type a number.",
    "hint": "This value is distinct from both success (> 0) and error (-1).",
    "answer": "0",
    "wrong": {
      "-1":  "-1 means an error occurred.  End-of-file is not an error.",
      "EOF": "EOF is a C macro equal to -1.  read() does not return it -- read() returns the integer 0 at end-of-file."
    },
    "explanation": "read() returning 0 means the kernel has no more bytes -- the file position is at the end.  This is how EOF is communicated at the POSIX level."
  },
  {
    "cluster": "read() -- partial reads",
    "prompt": "read(fd, buf, 1024) is called.  The file has exactly 300 bytes remaining\nbefore EOF.  What does read() return?\n\n  Type a number.",
    "hint": "read() returns the number of bytes actually transferred, never more than available.",
    "answer": "300",
    "wrong": {
      "1024": "1024 is the requested maximum, not the bytes available.",
      "0":    "0 would mean EOF; there are still 300 bytes remaining."
    },
    "explanation": "read() returns however many bytes it actually transferred.  A return value smaller than the count argument is a partial read -- normal, not an error.  The caller must loop to get all the data."
  },
  {
    "cluster": "write() -- partial writes",
    "prompt": "write(fd, buf, 512) returns 200.  What must the caller do next?\n\n  Type exactly one of: retry / abort / nothing",
    "hint": "200 bytes were written.  312 were not.",
    "answer": "retry",
    "wrong": {
      "abort":   "A partial write is not an error.  The kernel wrote as many bytes as it could.",
      "nothing": "Ignoring the partial write means the remaining 312 bytes are silently lost."
    },
    "explanation": "write() may write fewer bytes than requested.  The caller must advance the buffer pointer by the bytes written and call write() again for the remainder.  This is the write-loop pattern."
  },
  {
    "cluster": "errno -- EINTR",
    "prompt": "A syscall returns -1 and errno is EINTR.  What should the caller do?\n\n  Type exactly one of: retry / abort / ignore",
    "hint": "EINTR means the call was interrupted before it could do any work.",
    "answer": "retry",
    "wrong": {
      "abort":  "EINTR is recoverable.  The syscall was interrupted by a signal before transferring any bytes.",
      "ignore": "Ignoring EINTR leaves the operation incomplete with no data transferred."
    },
    "explanation": "EINTR means a signal arrived while the syscall was waiting.  No bytes were moved.  The correct response is to call the syscall again.  Many libc wrappers (like fread) handle this automatically."
  },
  {
    "cluster": "errno -- EBADF",
    "prompt": "read() returns -1.  errno is EBADF.  What does EBADF indicate?\n\n  Type exactly one of: invalid fd / file not found / permission denied",
    "hint": "EBADF describes a problem with the fd argument itself, not the file it points to.",
    "answer": "invalid fd",
    "wrong": {
      "file not found":   "File not found is ENOENT.  EBADF is about the fd number, not the path.",
      "permission denied": "Permission denied is EACCES.  EBADF means the fd was never opened or was already closed."
    },
    "explanation": "EBADF (Bad File Descriptor) means the fd argument is not a valid open file descriptor in this process -- it was never opened, has already been closed, or is out of range."
  },
  {
    "cluster": "perror()",
    "prompt": "perror(\"open\") is called after a failure.  Which output stream does\nit write to?\n\n  Type exactly one of: stdout / stderr / stdin",
    "hint": "Error messages should reach the user even when normal output is redirected.",
    "answer": "stderr",
    "wrong": {
      "stdout": "If perror() wrote to stdout and stdout were piped to another program, the error message would silently disappear.",
      "stdin":  "stdin is for input, not output."
    },
    "explanation": "perror() always writes to stderr (fd 2).  This ensures error messages are visible even when stdout is redirected to a file or piped."
  },
  {
    "cluster": "close() and fd limits",
    "prompt": "A long-running server opens a new file on every request but never calls\nclose().  Eventually open() starts returning -1.  What errno symbol is set?\n\n  Type exactly one of: EMFILE / ENOENT / EBADF / ENOSPC",
    "hint": "Every process has an upper bound on how many file descriptors it can hold open simultaneously.",
    "answer": "EMFILE",
    "wrong": {
      "ENOENT": "ENOENT is file not found.  The files exist; the process just cannot open them.",
      "EBADF":  "EBADF is an invalid fd passed to a call, not a limit on new opens.",
      "ENOSPC": "ENOSPC is no space left on the device -- a disk-full error."
    },
    "explanation": "EMFILE (Too many open files) is set when a process tries to open a new file but has already consumed all available fd slots.  The fix is to call close() on fds that are no longer needed."
  }
]
""")

# -- Display helpers --
_LINE_WIDTH = 70

def _banner(title):
    print("=" * _LINE_WIDTH)
    pad = max(0, (_LINE_WIDTH - len(title) - 2) // 2)
    print(" " * pad + " " + title + " " + " " * pad)
    print("=" * _LINE_WIDTH)

def _hr():
    print("-" * _LINE_WIDTH)

def _wrap(text):
    return _tw.wrap(text, width=_LINE_WIDTH - 4,
                    initial_indent="  ", subsequent_indent="    ")

def _show_wrong(raw, wrong_dict):
    exp = wrong_dict.get(raw)
    if exp:
        print()
        for ln in _wrap(f"[wrong]  {exp}"):
            print(ln)
    else:
        print(f"  [wrong] {raw!r} is not one of the listed options.")

def _show_passphrase(passphrase):
    print()
    _hr()
    print(f"  Passphrase: {passphrase}")
    _hr()
    print()


def _ask(q, index, total):
    _hr()
    print()
    cluster_label = f"  [{q['cluster']}]"
    print(cluster_label)
    print()
    print(f"  Q{index:02}/{total:02}  {q['prompt']}")
    print()
    print(f"  Hint: {q['hint']}")
    attempts = 0
    while True:
        print()
        try:
            raw = input("  Your answer: ").strip()
        except EOFError:
            print()
            sys.exit(0)
        if not raw:
            continue
        if raw == q["answer"]:
            print()
            if attempts == 0:
                for ln in _wrap("Correct.  " + q.get("explanation", "")):
                    print(ln)
            else:
                for ln in _wrap(q.get("explanation", "")):
                    print(ln)
            return raw
        attempts += 1
        _show_wrong(raw, q.get("wrong") or {})


def main():
    _banner("Activity: File I/O Contracts")
    print()
    print("  Ten questions on the contracts of open(), read(), write(),")
    print("  close(), errno, and perror().  Each question tells you exactly")
    print("  which answers are permitted -- type one of them precisely.")
    print()
    input("  Press Enter to begin...")

    answers = []
    total = len(QUESTIONS)
    for i, q in enumerate(QUESTIONS, 1):
        answers.append(_ask(q, i, total))

    print()
    _hr()
    print()
    print("  All correct.")
    passphrase = _decrypt(_BLOB, answers)
    if passphrase is None:
        print("  [error] Decryption failed -- contact your instructor.")
        sys.exit(1)
    _show_passphrase(passphrase)


if __name__ == "__main__":
    main()
