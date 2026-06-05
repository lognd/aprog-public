# Tool Design: Discovery Commands

## `aprog list`

Lists known assignments.

```bash
aprog list
aprog list --language python
aprog list --difficulty medium
aprog list --topic data-structures
aprog list --status draft
aprog list --status public-valid
```

Output format (one line per assignment):

```text
linked-list-insertion    python  medium  [data-structures, linked-lists]  public-valid
matrix-multiplication    cpp     hard    [algorithms, matrices]           draft
```

Flags:

| Flag | Description |
|---|---|
| `--language <lang>` | Filter by language |
| `--difficulty <level>` | Filter by difficulty |
| `--topic <topic>` | Filter by topic (may repeat) |
| `--status <status>` | Filter by public assignment state |
| `--json` | Emit JSON array instead of table |

## `aprog info`

Shows detailed metadata for one assignment.

```bash
aprog info linked-list-insertion
```

Output:

```text
Slug:         linked-list-insertion
Name:         Linked List Insertion
Author:       github-handle
Description:  Insert values into a linked list.
Status:       public-valid

Classification:
  Language:   python
  Difficulty: medium
  Topics:     data-structures, linked-lists
  Concepts:   mutation

Template:     python-function (v0.1)

Paths:
  Root:         assignments/linked-list-insertion/
  README:       assignments/linked-list-insertion/README.md
  Visible tests: assignments/linked-list-insertion/visible-tests/

Generated:
  Manifest:     generated/assignments/linked-list-insertion/assignment-manifest.json
  Autograder:   generated/assignments/linked-list-insertion/run_autograder.py
  Hash status:  current
```

With `--private ../aprog-private`:

```text
Private:
  Solution:     solutions/linked-list-insertion/      present
  Hidden tests: hidden-tests/linked-list-insertion/   present
  Grader:       grader/linked-list-insertion/          present
  Verified:     yes
```

## `aprog templates list`

Lists available templates.

```bash
aprog templates list
aprog templates list --language python
```

Output:

```text
python-function        Python   Function implementation
python-stdin-stdout    Python   stdin/stdout programs
cpp-cmake              C++      CMake-based projects
...
```

## `aprog templates info`

Shows template details.

```bash
aprog templates info python-function
```

Output:

```text
Slug:        python-function
Name:        Python Function
Version:     0.1
Language:    python
Description: Python assignment where students implement one or more functions.

Public outputs:
  assignment.toml, README.md, visible-tests/, assets/

Private outputs:
  solution/, hidden-tests/, grader/pipeline.py
```
