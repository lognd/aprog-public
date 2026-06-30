# Activities

Self-contained interactive activities. Students run `python3 launch.py` locally, answer questions or complete tasks, and receive an encrypted passphrase on success. No Gradescope needed.
There is a quiz-generator in `../aprog-private/scripts/generate_activities.py` and `../aprog-private/activities/data/*.json`
WHEREVER POSSIBLE, try and make the activity INTERACTIVE and *try* and stay away from only quizzes.

## Directory layout

```
activities/<slug>/
    launch.py          required; self-contained
    README.md          required; describes what students should do.
    <assets>           optional: repo.zip, myfs.img, data files, etc.
```

## Passphrase crypto (all Q&A activities)

The passphrase is encrypted into `_BLOB` using XOR stream cipher + HMAC-SHA256 MAC. The key is derived from the correct answers via PBKDF2-HMAC-SHA256. Wrong answers produce an HMAC mismatch -- no decryption.

```python
_SALT      = bytes.fromhex("a3f1b2c4d5e6f7a8b9c0d1e2f3a4b5c6")
_KDF_ITERS = 100000

def _derive_key(answers):        # answers: list[str] of exact correct strings
    return _hl.pbkdf2_hmac("sha256", "|".join(answers).encode(), _SALT, _KDF_ITERS)

def _stream(key, length): ...    # SHA256-based keystream

def _decrypt(blob_hex, answers): # returns plaintext or None
    blob    = bytes.fromhex(blob_hex)
    key     = _derive_key(answers)
    ct, mac = blob[:-32], blob[-32:]
    if not _hm.compare_digest(mac, _hm.new(key, ct, _hl.sha256).digest()):
        return None
    return bytes(a ^ b for a, b in zip(ct, _stream(key, len(ct)))).decode()
```

To generate a new `_BLOB`, run the encrypt utility with the correct answers and desired passphrase (see `aprog-private/activities/generate_activities.py`).

## Q&A activity structure (sizeof-bingo, bit-manipulation-re style)

```python
QUESTIONS = json.loads(r"""
[
  {
    "prompt": "What does f(24) return?",
    "hint":   "Trace step by step.",
    "answer": "8",           # exact string match
    "wrong": {               # optional: keyed wrong answers with explanations
      "24": "That is the input, not the output.",
      "4":  "Check your arithmetic."
    },
    "explanation": "Full explanation shown after correct answer."
  }, ...
]
""")
```

`_ask()` loops until the student types the exact answer string. Wrong attempts show `wrong[raw]` if present, else a generic message, then re-prompt. Explanation is shown inline on first-try correct, or after re-prompting on retries.

`main()` collects all answers, calls `_decrypt(_BLOB, answers)`, prints the passphrase.

## Snippet-prediction activity (implicit-conversion-minefield style)

Same crypto, but:

- Compiles and runs each snippet via subprocess at startup to get actual output
- `_ask()` requires typing the exact actual output string; `wrong` dict keys are common wrong guesses
- Useful when the "correct" answer is definitionally the compiler's output

## Creative / shell-drop activity (git-heist, terminal-archeology style)

No Q&A loop. `launch.py` sets up an environment and drops the student into a shell:

- **git-heist**: extracts `repo.zip` to a temp dir, opens bash with a custom `PS1` and `cd` into the repo. Student navigates git history to find the answer.
- **terminal-archeology**: mounts `myfs.img` as a loopback filesystem (requires `sudo`), drops into a shell with the mount as `HOME`. Student explores the filesystem.

These activities do NOT generate a passphrase via the crypto scheme. The answer/passphrase is embedded inside the asset (the zip or the image).

Pattern:

```python
work_dir = tempfile.mkdtemp(prefix="<slug>-")
atexit.register(lambda: shutil.rmtree(work_dir, ignore_errors=True))
# set up environment
rcfile.write(f'PS1=...\ncd "{repo_dir}"\necho "instructions"\n')
subprocess.run([shell, "--rcfile", rcfile.name])
```

## Style conventions

- `_LINE_WIDTH = 70`
- `_banner(title)` prints `=`-bordered header
- `_hr()` prints `-` divider
- `_wrap(text)` wraps with 2-space indent, 4-space continuation
- `_show_wrong(raw, wrong_dict)` handles known vs unknown wrong answers
- `_show_passphrase(passphrase)` prints passphrase between `_hr()` lines
- No emoji, no non-ASCII characters
- Imports: `json, sys, hashlib as _hl, hmac as _hm, textwrap as _tw`

## Existing activities

| Slug | Type | Topic |
|------|------|-------|
| `sizeof-bingo` | Q&A | sizeof values across platforms |
| `implicit-conversion-minefield` | snippet-predict | C++ implicit conversions |
| `bit-manipulation-re` | Q&A | bitwise function tracing |
| `git-heist` | shell-drop (zip) | git history navigation |
| `terminal-archeology` | shell-drop (img, sudo) | filesystem exploration |
| `cpp-standards-hunt` | shell-drop (cmake) | C++ standard versions and feature lookup |
| `project-layout` | shell-drop (cmake) | CMake project directory structure |
| `project-docs` | shell-drop (file check) | Writing project documentation files |
| `stack-heap-bingo` | bingo (custom) | stack vs heap, variable lifetimes |
| `recursion-unwind` | Q&A with code | call counts and stack depth for three fib implementations |
| `call-stack-autopsy` | Q&A with code | reading a real stack trace, diagnosing infinite recursion |
| `char-by-char` | snippet-predict | C-style string sentinel loops, pointer arithmetic, two-pointer reverse |
| `cstring-whodunit` | Q&A | C-string bugs: buffer overflow, pointer comparison, literal mutation, sizeof vs strlen, strncpy |
| `cstring-vs-stdstring` | snippet-predict | C-string vs std::string: length, concatenation, comparison, mutation, bounds, c_str() |
| `posix-file-tour` | paginated walkthrough (novel) | POSIX file I/O stack: open/read/write/close contracts, errno, fd table |
| `file-io-contracts` | Q&A | open/read/write/close return values, errno codes, partial transfers, perror |
| `write-your-first-syscalls` | shell-drop (zip, code completion) | writing open/read/write/close calls in C++; read loop; error handling |
| `iostream-interceptor` | snippet-prediction | operator<< chaining, >> vs getline whitespace rules, stream state flags, clear() |
| `sstream-formatter` | snippet-prediction | ostringstream, iomanip manipulators (setw/setfill/left/fixed/hex), sticky vs. one-shot behavior |
| `text-stream-surgery` | shell-drop (debugging) | ifstream eof-loop bug, is_open() check, >> vs getline leftover-newline bug in file context |
| `binary-stream-explorer` | shell-drop (fill-in-blanks) | ifstream binary mode, read() + reinterpret_cast, seekg() offset computation, sizeof for struct layout |
| `enum-field-day` | snippet-predict | enum vs enum class: default numbering, explicit values, sizeof, implicit conversion, typedef idiom, switch exhaustiveness |
| `union-dissector` | shell-drop (program-output) | union memory layout, sizeof union, type punning, hex byte inspection with %02x, IEEE 754 float bit patterns |
| `dod-hot-cold` | shell-drop (benchmark + rewrite) | Array of Structs vs Struct of Arrays, spatial locality, CPU cache motivation, hot-cold split |
| `struct-layout-bingo` | shell-drop (program-output) | struct alignment, padding, offsetof, sizeof, #pragma pack(push,1), #pragma pack(pop), field reordering |
