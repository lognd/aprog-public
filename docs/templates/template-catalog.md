# Template Catalog

Available templates for `aprog new`. Each template generates both the public scaffold (`assignments/<slug>/`) and the private scaffold (`$APROG_STAGING_DIR/<slug>/grader/pipeline.py`).

**Before picking a template,** look at the corresponding demo in `examples/template-demos/`. Every template has a working demo with a complete `pipeline.py`, solution, and hidden tests. Reading it first is the fastest way to understand what you need to fill in.

For `pipeline.py` authoring, see the [lograder documentation](https://github.com/lognd/lograder).

```bash
aprog templates list
aprog templates list --language python
aprog templates info <template-slug>
```

---

## Python templates

### `python-function`

Students implement one or more functions in a `.py` file.

**Demo:** `examples/template-demos/binary-search-staging/`

Public files:
```text
assignment.toml
README.md
visible-tests/test_visible.py
assets/<slug>.py          starter file
```

Private grader pattern: `PytestTest` with hidden tests that import the student module via `importlib.util`.

---

### `python-stdin-stdout`

Classic stdin/stdout assignments. Students submit a `.py` script that reads from stdin and writes to stdout.

**Demo:** `examples/template-demos/add-two-numbers-staging/`

Public files:
```text
assignment.toml
README.md
visible-tests/test_visible.py
expected/sample-input.txt
expected/sample-output.txt
```

Private grader pattern: `PrebuiltArtifacts` + `OutputCompareTest`.

Note: the submitted `.py` file must have `#!/usr/bin/env python3` as its first line so the OS can execute it directly.

---

### `python-pytest`

Students submit a module tested by pytest (typically a class or set of functions).

**Demo:** `examples/template-demos/stack-adt-staging/`

Public files:
```text
assignment.toml
README.md
visible-tests/test_visible.py
assets/<slug>.py          starter file
```

Private grader pattern: `PytestTest` with hidden tests that import the student class via `importlib.util`.

---

## C/C++ templates

### `cpp-stdin-stdout`

Single-file C++ stdin/stdout assignments. Students submit a `.cpp` file.

**Demo:** `examples/template-demos/reverse-string-staging/`

Private grader pattern: `CMakeBuild` + `OutputCompareTest`.

---

### `cpp-cmake`

C++ assignments built with CMake. Students submit source files and a `CMakeLists.txt`.

**Demo:** `examples/template-demos/graph-search-staging/`

Private grader pattern: `CMakeBuild` + `OutputCompareTest` or `CTestTest`.

---

### `cpp-makefile`

C++ assignments built with a Makefile. Students submit source files and a `Makefile`.

**Demo:** `examples/template-demos/word-count-staging/`

Private grader pattern: `MakefileBuild` + `PrebuiltArtifacts` + `OutputCompareTest`.

Note: `MakefileBuild` returns an empty artifact dict. Use `PrebuiltArtifacts` with an absolute `Path` to register the produced binary.

---

### `cpp-header-impl`

C++ header-only or header+impl assignments. Students submit a `.hpp` (and optionally `.cpp`) file; the grader provides `main.cpp` and `CMakeLists.txt`.

**Demo:** `examples/template-demos/cpp-bst-staging/`

Private grader pattern: `InjectStudentIntoStaff` + `CMakeBuild` + `CatchTest`.

---

### `cpp-class`

C++ class implementation assignments. Students submit a `.hpp` + `.cpp` pair.

**Demo:** `examples/template-demos/matrix-class-staging/`

Private grader pattern: `InjectStudentIntoStaff` + `CMakeBuild` + `CatchTest`.

---

### `c-stdin-stdout`

Single-file C stdin/stdout assignments.

**Demo:** `examples/template-demos/caesar-cipher-staging/`

Private grader pattern: `InjectStudentIntoStaff` + `CMakeBuild` + `OutputCompareTest`.

---

## Systems templates

### `shell-script`

Shell scripting assignments. Students submit a `.sh` script.

Private grader pattern: `SourceCheck` + `PrebuiltArtifacts` (sets execute bit automatically) + `OutputCompareTest`.

Note: the submitted `.sh` file must have a valid shebang (e.g. `#!/bin/bash`) as its first line so the OS can execute it directly. No `chmod` needed in `setup.sh` -- `PrebuiltArtifacts` sets the execute bit.

---

## C++ no-CMake templates

These templates compile student code directly with `g++` via `GXXBuild`, without requiring a `CMakeLists.txt`. Use them when the submission is a small number of files and you do not need the CMake artifact discovery system.

### `cpp-single-file`

Students submit one `.cpp` file. Grader compiles it directly with `g++` and tests I/O correctness plus Valgrind memory safety.

Private grader pattern: `SourceCheck` + `GXXBuild` + `OutputCompareTest` + `ValgrindTest`.

Use when: the assignment is a standalone program (sorting, string manipulation, basic data structures without a separate header).

### `cpp-asan`

Students submit one `.cpp` file. Grader compiles with `-fsanitize=address,undefined` and uses `ASanTest` to detect memory errors at runtime.

Private grader pattern: `SourceCheck` + `GXXBuild(sanitizers=["address","undefined"])` + `OutputCompareTest` + `ASanTest`.

Use when: the assignment emphasizes memory management (manual dynamic allocation, pointer arithmetic, resource ownership). ASan provides more actionable error messages than Valgrind for heap-based errors.

Note: `ASanTest` requires the binary to be compiled with ASan. The grader's `setup.sh` only needs `g++` (ASan is built into GCC >= 4.8 on Linux).

### `cpp-compile-check`

Students submit a `.hpp` header. Grader tests both runtime correctness (via a grader-provided `main.cpp`) and compile-time rules using `CompileCheckTest`.

Private grader pattern: `SourceCheck` + `GXXBuild` + `OutputCompareTest` + `CompileCheckTest`.

Use when: the assignment has C++ language rules that must be enforced at compile time: const correctness, access specifiers, deleted constructors, template constraints, SFINAE, or C++20 concepts.
