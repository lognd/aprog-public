# README Style Guide

Reference for all activity and assignment READMEs in this repo.
The env-setup activity series is the canonical example of the activity format.

## Audience: absolute beginners

Every README is written from the ground up for absolute beginners who do
not yet know the vocabulary. This is the highest-priority rule in this
guide and it overrides brevity.

- Define every technical term at first use, in plain language, in the
  sentence where it appears or in an inline `<details>` block. Never
  assume the reader knows a word because "everyone in CS knows it."
  Terms like invariant, sentinel, vtable, ADT, amortized, idempotent,
  duck typing, heap, buffer, and descriptor all count.
- Prefer plain language over the buzzword when the buzzword adds nothing.
  When the term IS the thing being taught, introduce it explicitly:
  name it, define it, then use it consistently.
- Expand every acronym at first use (RAII, ABC, POSIX, LSP, AoS/SoA).
- Concrete before abstract: show the two-line example before stating the
  general rule.
- Read the draft back as someone who has never programmed outside this
  course. Any sentence that requires outside knowledge to parse gets
  rewritten or gets an explanation next to it.

---

## Activities

### Title

```markdown
# Activity: <Name>
```

Every activity gets the `Activity:` prefix in the h1. No exceptions.

### Opening

One or two paragraphs of prose immediately under the title. No header.
Describe what the activity is about and why it matters. Avoid filler
phrases like "In this activity you will...".

### Section order

```
# Activity: <Name>

[opening prose -- no header]

## Background  (optional)

## Concepts covered

## How it works

## Getting started

## You will know you are done when...

## Hints  (optional)

## Going further  (optional)
```

`## Background` is only added when the opening prose would become too long
to read comfortably before getting to instructions. Limit to one background
section; do not split background across multiple sections.

`## Concepts covered` is a short bullet list of the specific C++ or CS
concepts the activity exercises. It appears before `## How it works` so
students and instructors can instantly see what this activity is for.
Write 3-6 bullets. Each should name a concrete skill or concept, not a
vague theme:

```markdown
## Concepts covered

- Null-terminated C strings and the sentinel pattern
- `strlen`, `strcpy`, `strcat` semantics
- Pointer arithmetic vs. array subscript notation
```

`## How it works` describes the mechanics of the activity: what questions
are asked, what the student must produce, how the launcher evaluates answers.

`## Getting started` contains the launch command and, for shell-based
activities (where a subshell opens and the student does work), numbered
walkthrough steps.

### Launch command

Always a fenced code block, never 4-space indented:

```markdown
## Getting started

    python3 launch.py        <-- wrong: 4-space indent

## Getting started

```bash
python3 launch.py
```
```

If the activity requires `sudo`, say so explicitly before the block:

```markdown
This activity requires root access to set up the sandbox environment.

```bash
sudo python3 launch.py
```
```

### Walkthrough steps (shell-based activities)

Shell-based activities (cmake-heist, scope-safari, string-methods, etc.)
open a subshell where the student does real work. Use numbered steps under
`## Getting started`:

```markdown
## Getting started

```bash
python3 launch.py
```

A shell opens inside a fresh copy of the project.

### Step 1 -- explore the starting state

...

### Step 2 -- build the program

...

### Step N -- exit

    exit

The launcher checks your work automatically.
```

Each step heading: `### Step N -- <imperative phrase>` (lowercase after `--`).
Steps use prose plus code blocks. Exit is always the last step.

### Completion line

```markdown
## You will know you are done when...

[One or two sentences describing the terminal success state.]
```

Always the full phrase "You will know you are done when..." -- not
"You'll know", not "You're done when".

### Hints

```markdown
## Hints

<details>
<summary>Hint 1 -- short phrase describing the hint</summary>

Hint body. Can be multiple paragraphs. No leading blank line after
`<summary>` closing tag, but there must be a blank line before the
closing `</details>` tag.

</details>

<details>
<summary>Hint 2 -- ...</summary>

...

</details>
```

Hint summary format: `Hint N -- <lowercase phrase>`. Use sentence-style
capitalization inside the body.

### Inline expandable blocks

Use `<details>` / `<summary>` freely for optional deep-dives embedded
inside a section (e.g., "What does this command do?"). The summary should
be a noun phrase or question, not an imperative:

```markdown
<details>
<summary>What is sudo?</summary>

...

</details>
```

### Going further (optional)

The last section of every activity README. 2-4 extension ideas for
students who finish early or want to dig deeper. Not graded. Frame each
as a concrete investigation or small experiment, not a vague suggestion:

```markdown
## Going further

- What happens if you call `strcat` on a buffer that is exactly the right
  size? Try it and read the output under AddressSanitizer.
- Write your own `strlen` using a pointer instead of an index variable and
  compare the assembly output with `g++ -S -O2`.
- Look up the C standard definition of undefined behavior for out-of-bounds
  reads. What does the compiler actually do on your machine?
```

For shell-based activities, extensions can suggest modifying the code,
trying a harder variant, or researching a related tool.

### Things to avoid

- `**Type:** ...` metadata lines -- drop them
- `## Requirements` sections listing "Python 3.8 or later" -- unnecessary
- `## Commands you will need` sections -- weave the command list into prose
- `## Your objectives` -- use `## How it works` instead
- `## Overview` as an extra wrapper around the opening prose
- `## Rules` as a top-level section -- weave into `## How it works`
- Bullet lists of "The concepts covered:" before explaining anything
- Trailing whitespace on lines

---

## Assignments

### Title

```markdown
# <Name>
```

No prefix. Assignment names are title-case noun phrases.

### Section order

```
# <Name>

[opening prose or ## Overview]

## Learning goals

## Task  (or ## Background + ## Task for longer assignments)

## Files  (table)

## Compilation and Testing

## Constraints

## Grading  (table)

## Submission

## Going further  (optional)
```

Short assignments (one file, simple task) may omit `## Overview` and open
directly with prose. Longer assignments with substantial background should
use `## Overview` explicitly.

`## Background` between `## Overview` and `## Task` is acceptable when
students need material that would not fit in the overview paragraph.

`## Learning goals` appears right after the overview (or opening prose) and
before the task. It is a short bullet list of what the assignment is designed
to teach -- the skills a student should have after completing it. Write 3-5
bullets. Be specific about the CS concept, not just the feature used:

```markdown
## Learning goals

- Understand row-major storage and why dense matrices use a flat array
- Practice pointer arithmetic as an alternative to subscript notation
- Distinguish `const int*`, `int* const`, and `const int* const`
- Write functions that receive read-only data correctly (`const T*`)
```

`## Going further` (at the very end, after `## Submission`) offers 2-4
optional extension challenges. Not graded. Framed as small experiments or
additions to the submitted code:

```markdown
## Going further

- Add a `mat_multiply` function and benchmark it against a naive `int[][]`
  version to see the cache behavior difference.
- Implement the same matrix operations using `std::vector<int>` and compare
  the code. What does the subscript operator actually buy you?
- Try compiling with `-fsanitize=address` and deliberately access an
  out-of-bounds element. Read the ASan report.
```

### Files table

```markdown
## Files

| File | Purpose |
|------|---------|
| `foo.hpp` | Declarations -- do not modify |
| `foo.cpp` | Write your implementation here |
```

Always use the two-column "File / Purpose" format.

### Compilation and Testing

Section name is always `## Compilation and Testing` -- not
"Building and testing", not "Compilation & Testing".

### Constraints

```markdown
## Constraints

- Do not modify `foo.hpp`.
- Do not use `std::vector`.
- Every function must throw `std::invalid_argument` on empty input.
```

Bullet list. Each item is one constraint. No sub-bullets.

### Grading table

```markdown
## Grading

| Component | Points |
|-----------|--------|
| ...       | ...    |
| **Total** | **100** |
```

Bold the Total row. If there is extra credit, add it below Total:

```markdown
| Extra credit -- Euclidean GCD | +5 |
```

### Submission

```markdown
## Submission

Submit a single file named `foo.cpp`. Do not rename it.
```

One sentence or two. If multiple files, bullet list them.

### Horizontal rules

Use `---` to separate the major sections of longer assignments:
after `## Overview`, before `## Grading`, and wherever two adjacent
sections feel too packed. Do not use `---` in short assignments.

### Things to avoid

- `## Problem Statement` -- just write the problem directly under `## Task`
- `## Input Format` / `## Output Format` as separate sections for
  non-stdin-stdout assignments -- fold into `## Task`
- `## Notes` as a catch-all at the end -- move content into the
  appropriate section
- Inconsistent section names across assignments

---

## Shared conventions

### Code blocks

Always fenced with triple backticks. Specify the language when the block
contains a specific language:

```
```bash
```
```cpp
```makefile
```

Use plain triple backticks (no language) for program output or
mixed/ambiguous content.

### Tables

Pipe tables. Header row required. Alignment colons optional.

### Inline code

Backtick-wrap: file names, function names, flags, variable names,
command names, literals. Do not backtick-wrap section references or
conceptual terms.

### Emphasis

Use `**bold**` for truly important warnings or key terms on first use.
Do not bold section headers or routine instructions.

### Sentences

One space after a period. No Oxford comma required but be consistent
within a document.

### Non-ASCII

Never use non-ASCII characters. Use `--` for em-dash, `->` for arrows.
