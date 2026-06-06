# Template Demos

Each pair of directories here shows exactly what `aprog new` produces for a
given template, then filled in with a real implementation. The `-public`
directory is what lands in `aprog-public`; the `-staging` directory is what
goes to the contributor's private staging area.

## How these were generated

```bash
STAGING=/tmp/aprog-staging-demos

aprog new add-two-numbers  --template python-stdin-stdout --staging-dir $STAGING
aprog new binary-search    --template python-function     --staging-dir $STAGING
aprog new stack-adt        --template python-pytest       --staging-dir $STAGING
aprog new reverse-string   --template cpp-stdin-stdout    --staging-dir $STAGING
aprog new graph-search     --template cpp-cmake           --staging-dir $STAGING
aprog new cpp-bst          --template cpp-header-impl     --staging-dir $STAGING
aprog new matrix-class     --template cpp-class           --staging-dir $STAGING
aprog new word-count       --template cpp-makefile        --staging-dir $STAGING
aprog new caesar-cipher    --template c-stdin-stdout      --staging-dir $STAGING
```

## Template -> example mapping

| Template            | Example assignment  | What to note |
|---------------------|---------------------|--------------|
| `python-stdin-stdout` | `add-two-numbers`  | `PrebuiltArtifacts` registers the .py file; `OutputCompareTest` drives grading |
| `python-function`     | `binary-search`    | `PytestTest` runs hidden tests; visible/hidden both use `importlib.util` (avoids hyphen-in-name import error) |
| `python-pytest`       | `stack-adt`        | Same as python-function; starter file is a class skeleton |
| `cpp-stdin-stdout`    | `reverse-string`   | `InjectStudentIntoStaff` copies .cpp into grader dir; CMake builds it |
| `cpp-cmake`           | `graph-search`     | Student submits their own `CMakeLists.txt`; grader just calls `CMakeBuild` |
| `cpp-header-impl`     | `cpp-bst`          | Full pipeline: `InjectStudentIntoStaff` + `Catch2Test` (vis+hidden) + `ValgrindTest` + `DifferentialTest` EC |
| `cpp-class`           | `matrix-class`     | Student submits `.hpp` + `.cpp`; both injected for Catch2 builds |
| `cpp-makefile`        | `word-count`       | `MakefileBuild` + `PrebuiltArtifacts` (binary path injected manually) |
| `c-stdin-stdout`      | `caesar-cipher`    | Same inject pattern as cpp-stdin-stdout but C11; shift passed via argv |

## What was implemented

### add-two-numbers (python-stdin-stdout)

Read two integers from stdin (one per line) and print their sum.

- `assignment.toml`: difficulty=easy, topics=[math, stdin-stdout]
- `README.md`: problem statement with input/output format and two examples
- `expected/sample-input.txt`: `3\n7\n`; `sample-output.txt`: `10\n`
- `visible-tests/test_visible.py`: three subprocess tests (basic sum, negative, zeros)
- `solution/solution.py`: `print(int(readline()) + int(readline()))`
- `grader/pipeline.py`: 3 visible cases (30 pts) + 3 hidden cases (70 pts)
- `hidden-tests/test_hidden.py`: large values, negatives, both-positive

### binary-search (python-function)

Implement `binary_search(arr, target) -> int` returning the index or -1.

- `assignment.toml`: difficulty=easy, topics=[searching, algorithms]
- `README.md`: function signature, examples, O(log n) constraint
- `visible-tests/test_visible.py`: uses `importlib.util` to load `binary-search.py`
  (avoids the `from binary-search import` syntax error caused by the hyphen)
- `solution/solution.py`: standard iterative binary search
- `grader/pipeline.py`: 6 hidden pytest cases (100 pts)
- `hidden-tests/test_hidden.py`: also uses `importlib.util`; covers single element,
  large array, negative values, two-element edge cases

### stack-adt (python-pytest)

Implement a `Stack` class with push, pop, peek, is_empty, size.

- `assignment.toml`: difficulty=easy, topics=[data-structures, stack]
- `README.md`: full interface with docstrings, O(1) constraint
- `visible-tests/test_visible.py`: importlib pattern; 6 tests covering all methods
  and error cases
- `solution/solution.py`: list-backed Stack with IndexError on pop/peek when empty
- `grader/pipeline.py`: 5 hidden tests (70 pts)
- `hidden-tests/test_hidden.py`: interleaved push/pop, size tracking, peek stability,
  mixed types, error after emptied

### reverse-string (cpp-stdin-stdout)

Read one line from stdin, print it reversed.

- `assignment.toml`: difficulty=easy, topics=[strings, stdin-stdout]
- `README.md`: problem statement with three examples (hello, palindrome, alpha)
- `expected/`: sample-input=`hello`, sample-output=`olleh`
- `visible-tests/test_visible.py`: compile+run tests for hello, palindrome, single char
- `solution/solution.cpp`: `std::getline` + `std::reverse` + `std::cout`
- `grader/pipeline.py`: 2 visible (20 pts) + 4 hidden (80 pts) + valgrind EC (+5)

### graph-search (cpp-cmake)

BFS on an undirected graph; print visited nodes in ascending-neighbor order.

Input format: `N M` / M edge pairs / source node. Output: space-separated BFS order.

- `assignment.toml`: difficulty=medium, topics=[graphs, bfs, algorithms]
- `README.md`: full input/output format, two examples (connected, disconnected)
- `visible-tests/test_visible.py`: tests connected and disconnected graphs
- `solution/main.cpp`: adjacency-list BFS using `std::queue`; neighbors sorted
- `grader/pipeline.py`: 2 visible (20 pts) + 3 hidden (60 pts) + valgrind (20 pts)

### cpp-bst (cpp-header-impl)

BST with insert (ignore duplicates), search, and inorder traversal.

- `assignment.toml`: difficulty=medium, topics=[data-structures, bst, trees]
- `README.md`: interface, no-STL requirement, full grading table
- `assets/starter.hpp`: real `BST` class declaration with private `Node` struct
- `visible-tests/test_catch.cpp`: 4 Catch2 cases (basic insert/search, sorted inorder,
  duplicates ignored, empty search)
- `solution/solution.hpp`: recursive insert, iterative search, recursive inorder,
  recursive destructor
- `hidden-tests/cpp-bst.hpp`: copy of solution used as `reference` binary target
- `hidden-tests/test_hidden.cpp`: 4 hidden cases (single element, descending insert,
  many-insert search, large tree inorder)
- `grader/main.cpp`: CLI driver dispatching `insert N`, `search N`, `inorder` from argv
- `grader/pipeline.py`: constraints (no STL containers), 4 visible Catch2 (60 pts),
  4 hidden Catch2 (45 pts), valgrind (20 pts), 5 manual I/O (25 pts), 2 diff EC (+15)

### matrix-class (cpp-class)

2D `Matrix` class: addition, multiplication, transpose, deep-copy.

- `assignment.toml`: difficulty=medium, topics=[linear-algebra, classes, memory-management]
- `README.md`: full interface with `operator+`, `operator*`, `transpose`, `print`
- `assets/starter.hpp`: real `Matrix` declaration with private `double *data_`
- `assets/starter.cpp`: skeleton with TODO comments for each method
- `visible-tests/test_catch.cpp`: 5 Catch2 cases (zero init, at, add, transpose, identity multiply)
- `solution/solution.hpp` + `solution.cpp`: complete implementation using `new double[]`
- `hidden-tests/test_hidden.cpp`: 4 hidden cases (copy ctor deep copy, copy assign deep copy,
  2x3 * 3x2 multiply, print output format)
- `grader/pipeline.py`: 5 visible Catch2 (60 pts) + 4 hidden Catch2 (40 pts)

### word-count (cpp-makefile)

Count words per line and print per-line and total counts.

Output format: `Line N: W word(s)` (singular when W=1) + `Total: W word(s)`.

- `assignment.toml`: difficulty=easy, topics=[strings, stdin-stdout]
- `README.md`: full format spec and two examples
- `expected/`: three-line sample demonstrating singular "word" vs plural "words"
- `visible-tests/test_visible.py`: tests three-line input and single-line input
- `solution/solution.cpp`: `std::getline` + `std::istringstream` word count
- `solution/Makefile`: builds `word-count` from `solution.cpp`
- `grader/pipeline.py`: 2 visible (10 pts) + 3 hidden (80 pts); build worth 10 pts

### caesar-cipher (c-stdin-stdout)

Encrypt text with a Caesar cipher; shift passed as `argv[1]`.

Letters shift with wraparound; non-letters pass through unchanged.

- `assignment.toml`: difficulty=easy, topics=[strings, cryptography]
- `README.md`: usage, three examples (shift 3, ROT13, shift 0)
- `expected/`: sample-input=`Hello, World!`, sample-output=`Khoor, Zruog!` (shift 3)
- `visible-tests/test_visible.py`: compile+run tests for shift 3, ROT13, shift 0
- `solution/solution.c`: `getchar` loop shifting with `((shift%26)+26)%26`
- `grader/pipeline.py`: 3 visible (30 pts) + 5 hidden (70 pts) + valgrind EC (+5);
  hidden tests cover alphabet wrap, mixed case wrap, non-alpha passthrough, ROT13
  roundtrip, multiline

## Next steps after `aprog new`

1. Edit `assignments/<slug>/README.md` -- write the problem statement.
2. Fill in `assignments/<slug>/assignment.toml` -- set `author`, `description`, `topics`.
3. Add visible test cases to `assignments/<slug>/visible-tests/`.
4. Fill in the staging grader: `<staging>/<slug>/grader/pipeline.py` -- replace TODO cases with real ones.
5. Write the reference solution in `<staging>/<slug>/solution/`.
6. Add hidden tests in `<staging>/<slug>/hidden-tests/`.
7. Run `aprog validate <slug>` to check the public side.
8. Run `aprog verify <slug>` (with staging) to confirm the grader works end-to-end.

## After verification

Once `aprog verify` passes with staging, the private files need to land in `aprog-private`
before the Gradescope zip is built. `aprog-private` is the source of truth for all grader
material and must exist as a separate private repository.

### 9. Package and submit the private bundle (contributor step)

```bash
aprog submit <slug>
# produces dist/<slug>-private.tar.gz
# or, with encryption: aprog submit <slug> --encrypt
```

Send `dist/<slug>-private.tar.gz` to the maintainer (or set `APROG_INTAKE_URL` to upload
directly). The bundle contains the solution, hidden tests, and `grader/pipeline.py`.
These files must never be committed to `aprog-public`.

### 10. Intake the bundle into `aprog-private` (maintainer step)

```bash
aprog intake dist/<slug>-private.tar.gz \
  --public ../aprog-public \
  --private ../aprog-private
```

Intake unpacks the bundle into the correct paths under `aprog-private`:

```
aprog-private/
  solutions/<slug>/
  hidden-tests/<slug>/
  grader/<slug>/pipeline.py
```

Commit and push to `aprog-private`.

### 11. Re-verify from `aprog-private` (independent check)

Run verification again, this time sourcing private files from the real private repo
rather than the local staging directory. This catches any intake path mismatches.

```bash
aprog verify <slug> \
  --public ../aprog-public \
  --private ../aprog-private
```

### 12. Generate configs, build zip, upload

```bash
cd aprog-public
aprog generate-config <slug> --force
aprog package-gradescope <slug> --public . --private ../aprog-private
# Upload dist/<slug>-gradescope.zip:
# Gradescope > Assignment > Configure Autograder > Upload Autograder
```

### 13. Test on Gradescope with the reference solution

Use Gradescope's "Test Autograder" feature, uploading the solution file(s) from
`aprog-private/solutions/<slug>/`. Confirm the score matches the expected total.

### 14. Merge and publish

```bash
# In aprog-public:
# - set status = "published" in assignment.toml
# - commit generated/ changes
# - open PR, get review, merge
```
