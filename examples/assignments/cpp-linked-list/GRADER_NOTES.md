# Grader Notes  --  cpp-linked-list

> **Private bundle only.** Do not commit to `aprog-public`.

---

## Repository layout

```
aprog-public/examples/assignments/cpp-linked-list/   <- public
  assignment.toml
  README.md
  assets/
  visible-tests/
    CMakeLists.txt          <- for student local builds
    test_catch.cpp          <- visible Catch2 test source
  grader/
    CMakeLists.txt          <- builds all four CMake targets
    main.cpp                <- CLI driver (compiled twice: student + reference)
    pipeline.py             <- full lograder grader pipeline
  hidden-tests/
    linked_list.hpp         <- staff solution (used by reference CMake target)
    test_hidden.cpp         <- hidden Catch2 test source
    README.md               <- this assignment's hidden-tests documentation

aprog-staging/cpp-linked-list/                       <- private (never public)
  solution/
    linked_list.hpp         <- complete reference implementation (student sim)
  grader/                   <- symlink or copy of grader/ from public repo
  hidden-tests/             <- symlink or copy of hidden-tests/ from public repo
```

The aprog staging layout maps to the zip as:
```
grader/         <- grader/
hidden-tests/   <- hidden-tests/
visible-tests/  <- visible-tests/  (pulled from public repo at package time)
run_autograder.py
run_autograder
setup.sh
```

No pre-compiled binary is needed. The `reference` CMake target compiles
`grader/main.cpp` against `hidden-tests/linked_list.hpp` (the staff solution)
at grading time. `DifferentialTest(reference_artifact="reference")` resolves
the built binary directly from the CMakeBuild artifacts dict.

---

## Step 1  --  Set up staging directory

```bash
PRIVATE=~/aprog-staging/cpp-linked-list
PUBLIC=~/aprog-public        # or wherever aprog-public is cloned

mkdir -p "$PRIVATE/solution"

# Copy the solution (used as the student submission during verify)
cp "$PUBLIC/examples/assignments/cpp-linked-list/solution/linked_list.hpp" \
   "$PRIVATE/solution/"

# grader/ and hidden-tests/ are read directly from the public repo by aprog.
# If aprog requires copies rather than symlinks:
cp -r "$PUBLIC/examples/assignments/cpp-linked-list/grader"       "$PRIVATE/"
cp -r "$PUBLIC/examples/assignments/cpp-linked-list/hidden-tests"  "$PRIVATE/"
```

---

## Step 2  --  Sanity-check manual test cases

Build a local reference to verify expected outputs match what is hardcoded
in `_MANUAL_CASES` in `grader/pipeline.py`. This is optional but recommended
when you change `solution/linked_list.hpp` or `grader/main.cpp`.

```bash
PRIVATE=~/aprog-staging/cpp-linked-list
PUBLIC=~/aprog-public/examples/assignments/cpp-linked-list

# Build locally (not needed on Gradescope  --  CMake handles it there)
mkdir -p /tmp/ll-verify-build
cmake -S "$PUBLIC/grader" -B /tmp/ll-verify-build \
    -DCMAKE_BUILD_TYPE=Release
cmake --build /tmp/ll-verify-build --target reference

BIN=/tmp/ll-verify-build/reference

# manual_five_print -> "10 20 30 40 50\n"
$BIN push_back 10 push_back 20 push_back 30 push_back 40 push_back 50 print

# manual_interleave_print -> "-1 0 1 2\n"
$BIN push_back 1 push_front 0 push_back 2 push_front -1 print

# manual_pop_to_empty_repush -> "size=1\nfront=42\nback=42\n"
$BIN push_back 1 push_back 2 pop_front pop_front push_back 42 size front back

# manual_alternating_pop_remainder -> "size=2\nfront=2\nback=3\n"
$BIN push_back 1 push_back 2 push_back 3 push_back 4 pop_front pop_back size front back

# manual_push_front_order -> "1 2 3\n"
$BIN push_front 3 push_front 2 push_front 1 print

# diff_large_sequence -> "size=20\n1 2 3 ... 20\n"
$BIN $(for i in $(seq 1 20); do echo push_back $i; done) size print

# diff_stress_mixed -> "size=2\n1 2\n"
$BIN push_back 1 push_back 2 push_front 0 pop_front push_back 3 pop_back size print

# diff_copy_bonus -> "10 20 30\n10 20 30 99\n"
$BIN push_back 10 push_back 20 push_back 30 copy_push 99
```

If any output is wrong, fix `solution/linked_list.hpp` and re-run.

---

## Step 3  --  Run `aprog verify`

```bash
APROG=~/aprog-public/.venv/bin/aprog

$APROG verify cpp-linked-list \
  --public ~/aprog-public/examples \
  --private ~/aprog-staging
```

Expected output ends with:
```
Score: 150.0/150.0 + 20.0 extra credit
[OK] Verification passed for 'cpp-linked-list'
```

---

## Step 4  --  Generate config and package

```bash
$APROG generate-config cpp-linked-list --force

$APROG package-gradescope cpp-linked-list \
  --public ~/aprog-public/examples \
  --private ~/aprog-staging \
  --output-dir ~/Downloads
# -> ~/Downloads/cpp-linked-list-gradescope.zip
```

Upload the zip to Gradescope -> Assignment Settings -> Autograder.

---

## Pipeline design

```
LocalDirectory(root=submission_dir)
  |  reads student submission
  v
SourceCheck("cpp", ["linked_list.hpp"], constraints=[...])          [card 1]
  |  BREAKS EARLY if linked_list.hpp is missing
  |  yields non-fatal Err per STL violation -> +5 EC if clean
  v
InjectStudentIntoStaff(grader_dir, student_files=["linked_list.hpp"])
  |  copies linked_list.hpp into grader/ so CMake can include it
  v
CMakeManifestCheck()                                                 [card 2]
  |  validates CMakeLists.txt present -> CMakeManifest type
  v
CMakeBuild()                                                         [card 3]
  |  cmake -S grader/ -B grader/build
  |  builds: linked_list_tests, linked_list_hidden_tests,
  |           linked_list (student), reference (staff)
  |  BREAKS EARLY on configure or build failure
  v
Catch2Test("linked_list_tests")                                      [card 4]  60 pts + 10 gimme
  |  visible-tests/test_catch.cpp  -- 12 TEST_CASEs x 5 pts
  |  gimme: +10 if >= 25% pass
  v
Catch2Test("linked_list_hidden_tests")                               [card 5]  45 pts + 5 gimme
  |  hidden-tests/test_hidden.cpp  -- 9 scored TEST_CASEs x 5 pts
  |  gimme: +5 if >= 25% pass
  |  visibility: after_due_date
  v
ValgrindTest("linked_list", cases)                                   [card 6]  20 pts
  |  4 cases x 5 pts, check_leaks=True
  v
OutputCompareTest("linked_list", manual_cases)                       [card 7]  25 pts
  |  5 manual cases x 5 pts, ComparisonMode.EXACT
  |  hardcoded expected_stdout in pipeline.py
  |  visibility: after_due_date
  v
DifferentialTest("linked_list", reference_artifact="reference", ...)  [card 8]  +15 EC
  |  3 extra-credit cases (0 base pts each)
  |  reference binary resolved from CMakeBuild artifacts at grading time
  |  no pre-compiled binary needed
  |  visibility: after_due_date
```

Steps 4-8 are all skipped (0/possible) if SourceCheck returns a fatal Err
(missing file) or CMakeBuild returns a fatal Err.

---

## Gradescope cards

| # | Label | Visibility | Points |
|---|---|---|---|
| 1 | No STL Containers | visible | +5 EC |
| 2 | CMake Setup | visible | 0 (gate) |
| 3 | Compilation | visible | 0 (gate) |
| 4 | Visible Correctness (Catch2) | visible | 60 + 10 gimme |
| 5 | Hidden Correctness (Catch2) | after_due_date | 45 + 5 gimme |
| 6 | Memory Safety (Valgrind) | visible | 20 |
| 7 | Hidden Manual Cases | after_due_date | 25 |
| 8 | Differential Extra Credit | after_due_date | +15 EC |

**Total: 150 pts + 20 extra credit**

---

## Manual test cases (card 7)

These are the `OutputCompareCase` objects in `_MANUAL_CASES` in `pipeline.py`.
Expected stdout is `ComparisonMode.EXACT` (trailing newline required).

| Name | Command | Expected stdout |
|---|---|---|
| `manual_five_print` | `push_back 10 ... push_back 50 print` | `10 20 30 40 50\n` |
| `manual_interleave_print` | `push_back 1 push_front 0 push_back 2 push_front -1 print` | `-1 0 1 2\n` |
| `manual_pop_to_empty_repush` | `push_back 1 push_back 2 pop_front pop_front push_back 42 size front back` | `size=1\nfront=42\nback=42\n` |
| `manual_alternating_pop_remainder` | `push_back 1..4 pop_front pop_back size front back` | `size=2\nfront=2\nback=3\n` |
| `manual_push_front_order` | `push_front 3 push_front 2 push_front 1 print` | `1 2 3\n` |

---

## Hidden Catch2 cases (card 5)

Source: `hidden-tests/test_hidden.cpp`

| Test name | Tag | Points |
|---|---|---|
| `size tracks push_back and pop_front correctly` | `[hidden][size]` | 5 |
| `size tracks push_front and pop_back correctly` | `[hidden][size]` | 5 |
| `pop_front restores expected front value` | `[hidden][order]` | 5 |
| `pop_back restores expected back value` | `[hidden][order]` | 5 |
| `copy constructor produces same contents` | `[hidden][copy]` | 5 |
| `mutating copy does not affect original` | `[hidden][copy]` | 5 |
| `mutating original does not affect copy` | `[hidden][copy]` | 5 |
| `print on two-element list is space-separated with newline` | `[hidden][print]` | 5 |
| `print on single-element list has no leading/trailing space` | `[hidden][print]` | 5 |
| `push_back then push_front interleaved preserves order` | `[hidden][order]` | _(unscored)_ |

---

## Differential extra credit (card 8)

The `reference` binary is compiled at grading time by the `reference` CMake
target in `grader/CMakeLists.txt`. It links `grader/main.cpp` against
`hidden-tests/linked_list.hpp` (the staff solution). No pre-built binary
needs to be committed or kept in sync with Gradescope's architecture.

| Name | Command | Points |
|---|---|---|
| `diff_large_sequence` | `push_back 1..20 size print` | +5 EC |
| `diff_stress_mixed` | interleaved push/pop -> `size print` | +5 EC |
| `diff_copy_bonus` | `push_back 10 20 30 copy_push 99` | +5 EC |
