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

Private grader pattern: `CMakeBuild` or `MakefileBuild` + `OutputCompareTest`.
