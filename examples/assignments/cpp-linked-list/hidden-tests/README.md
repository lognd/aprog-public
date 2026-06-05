# Hidden Tests  --  cpp-linked-list

> **Private bundle only.** This directory maps to
> `private_repo/hidden-tests/cpp-linked-list/` in the aprog staging layout
> and is bundled into the Gradescope zip as `hidden-tests/`.

---

## Contents

```
hidden-tests/
  linked_list.hpp   <- staff reference implementation
                       included by the `reference` CMake target at grading time
  test_hidden.cpp   <- hidden Catch2 test source (compiled by grader/CMakeLists.txt)
  README.md         <- this file
```

No pre-compiled binary is committed here. The `reference` CMake target in
`grader/CMakeLists.txt` compiles `grader/main.cpp` with `hidden-tests/`
on the include path, picking up `linked_list.hpp` as the staff implementation.
`DifferentialTest(reference_artifact="reference")` resolves the built binary
from the CMakeBuild artifacts dict at grading time.

---

## How the hidden tests are used

### 1  --  Hidden Catch2 (`linked_list_hidden_tests`)

`grader/CMakeLists.txt` compiles `test_hidden.cpp` as the
`linked_list_hidden_tests` target. `Catch2Test("linked_list_hidden_tests")`
in `pipeline.py` runs it with `--reporter junit` and maps test names to points.

Visibility: `after_due_date`. Scored as card 5.

### 2  --  Differential extra credit

`DifferentialTest("linked_list", reference_artifact="reference", _DIFF_CASES)`
runs the student `linked_list` binary and the `reference` binary on the same
`OracleInput` arguments, comparing stdout. The reference binary is compiled
fresh from `linked_list.hpp` (this file) each time the grader runs  --  no
expected output corpus is stored. All cases are extra credit.

Visibility: `after_due_date`. Scored as card 8.

---

## Hidden Catch2 test cases (`test_hidden.cpp`)

All test names use the `[hidden]` tag and are scored as
`linked_list_hidden_tests/<test name>` by `TestCaseScorer`.

### Size tracking (5 pts each)

| Test | What it checks |
|---|---|
| `size tracks push_back and pop_front correctly` | 10 push_backs -> 5 pop_fronts -> 5 pop_backs -> empty |
| `size tracks push_front and pop_back correctly` | 8 push_fronts -> 4 pop_backs -> size=4 |

### Order preservation (5 pts each)

| Test | What it checks |
|---|---|
| `pop_front restores expected front value` | after pop, front() updates correctly |
| `pop_back restores expected back value` | after pop, back() updates correctly |
| `push_back then push_front interleaved preserves order` | _(unscored -- verifies front/back/size only)_ |

### Copy constructor (5 pts each)

| Test | What it checks |
|---|---|
| `copy constructor produces same contents` | size, front, back match original |
| `mutating copy does not affect original` | push_back/pop_front on copy -> original unchanged |
| `mutating original does not affect copy` | pop_back/push_front on original -> copy unchanged |

### Print format (5 pts each)

| Test | What it checks | Expected stdout |
|---|---|---|
| `print on two-element list is space-separated with newline` | `{42} -> {7}` | `"42 7\n"` |
| `print on single-element list has no leading/trailing space` | `{99}` | `"99\n"` |

---

## Differential extra-credit cases (`_DIFF_CASES` in `pipeline.py`)

`DifferentialTest` runs both student and reference binaries on the same CLI
arguments. Expected output is whatever the reference binary produces at grading
time -- no stored corpus.

| Name | Arguments | Expected output |
|---|---|---|
| `diff_large_sequence` | `push_back 1..20 size print` | `size=20` + `1 2 3 ... 20` |
| `diff_stress_mixed` | `push_back 1 push_back 2 push_front 0 pop_front push_back 3 pop_back size print` | `size=2` + `1 2` |
| `diff_copy_bonus` | `push_back 10 push_back 20 push_back 30 copy_push 99` | `10 20 30` + `10 20 30 99` |
