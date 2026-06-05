# Classification Model

The classification model separates structured fields (language, difficulty, topics) from freeform labels.

## Root config

File: `aprog-public/aprog.toml`

This file is the source of truth for all valid classification values and organizational settings.

```toml
[classification.languages.python]
name = "Python"

[classification.languages.cpp]
name = "C++"

[classification.languages.c]
name = "C"

[classification.languages.java]
name = "Java"

[classification.difficulties.easy]
name = "Easy"
rank = 1

[classification.difficulties.medium]
name = "Medium"
rank = 2

[classification.difficulties.hard]
name = "Hard"
rank = 3

[classification.topics.data-structures]
name = "Data Structures"

[classification.topics.linked-lists]
name = "Linked Lists"

[classification.concepts.recursion]
name = "Recursion"

[classification.concepts.pointers]
name = "Pointers"

[labels.requires-filesystem]
name = "Requires filesystem access"
description = "Assignment expects student code to read or write files."

[labels.performance]
name = "Performance-sensitive"
description = "Assignment includes timing or complexity expectations."

[organization]
require_encryption = false
require_hidden_tests = true
default_grader_visibility = "after_due_date"
```

## Assignment use

```toml
[assignment]
slug = "linked-list-insertion"
name = "Linked List Insertion"
author = "github-handle"
description = "Insert values into a linked list."

[classification]
language = "python"
difficulty = "medium"
topics = ["data-structures", "linked-lists"]
concepts = ["mutation"]
labels = ["unit-tests"]
```

## Required classification fields

- `language` — required
- `difficulty` — required
- `topics` — required, non-empty

## Optional classification fields

- `concepts`
- `labels`
- `course`
- `module`

## Adding new classification values

Only maintainers may add new values. The process:

1. Open a PR against `aprog-public` that edits `aprog.toml`.
2. Add the new entry under the appropriate `[classification.*]` or `[labels.*]` table.
3. CI validates the TOML structure.
4. A maintainer merges the PR.

Contributors may request new values by opening an issue. Do not add classification values in a PR alongside an assignment — they must be merged to `aprog.toml` first.

## Freeform labels

Labels are optional properties that do not fit a structured field.

Recommended labels:

- `requires-filesystem`
- `performance`
- `interactive`
- `uses-randomness`
- `requires-network-disabled`
- `starter-code`
- `multi-file`
- `unit-tests`

All labels used in assignments must be declared in `aprog.toml [labels]`.

## Reserved names

These may not be used as classification keys or label slugs:

```text
private  hidden  solution  solutions  answer  answers
key      generated  secret  grader  pipeline
```

## Why structured fields instead of labels-only

Labels-only forces the validator to infer meaning:

```toml
labels = ["python", "linked-list", "medium"]
```

The validator cannot reliably distinguish a language label from a topic label from a difficulty label. Structured fields are explicit and independently validated:

```toml
language = "python"
difficulty = "medium"
topics = ["linked-lists"]
```

## Validation rules

Validation fails if:

- `language` is missing or unknown
- `difficulty` is missing or unknown
- `topics` is empty or contains unknown values
- any `concepts` value is unknown
- any `labels` value is unknown (not declared in `aprog.toml`)
- a reserved name is used as a key or label slug
